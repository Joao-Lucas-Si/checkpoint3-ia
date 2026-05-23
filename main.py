from src.llm_client import LLM_Client
from src.utils import ler_arquivo, esperar, escrever_arquivo
from src.schemas import TestDatasetSchema, ConfigSchema, RespostaSchema, ProcessamentoSchema, RegistroSchema, ClassificacaoSchema
from src.evaluator import Avaliador
from src.guardrails import Input_Guardrail
from src.ui import criar_menu
from typing import Callable, Optional
from src.chain import AssistantChain
import types

persona = ler_arquivo("prompts/system_prompt.txt")

config = ler_arquivo("data/db.json", ConfigSchema)

client = LLM_Client(sistema=persona, temperatura=config.temperatura, think=config.think, stream=config.stream)


registros: list[RegistroSchema] = []

def conversacao():
    entrada = input("digite sua mensagem: ")

    resposta = client.chamar(entrada)

    if isinstance(resposta, RespostaSchema):
        print(resposta.response)
    else:
        def ler(parte: str):
            print(parte, end="", flush=True)
        resposta(ler)

        print()
    esperar()

def avaliacao():
    testes = ler_arquivo("data/test_dataset.json", TestDatasetSchema)

    for teste in testes.casos:
        print(teste.input)
        
        
        try:
            erros: set[str] = set()
            def executar():
                chain = AssistantChain(teste.input)
                avaliador = Avaliador()
                input_guardrail = Input_Guardrail(teste.input)
                erros.update(input_guardrail.validar_input())
                if len(erros) > 0:
                    return
                classificacao = chain.classificar()
                print("classificacao", classificacao)
                processamento: Optional[ProcessamentoSchema] = None
                
                if isinstance(classificacao, ClassificacaoSchema):
                    resultado = chain.processar(classificacao)
                    
                    if isinstance(resultado, ProcessamentoSchema):
                        processamento = resultado
                    else:
                        erros.update(resultado)
                    print("processamento", processamento)
                
                if len(erros) == 0 and classificacao and processamento:
                    resposta = chain.responder(classificacao, processamento)
                    
                    if isinstance(resposta, RespostaSchema):
                        registros.append(RegistroSchema(classificacao=classificacao, duracao=0,  processamento=processamento, resposta=resposta.response, esperado={
                            "urgencia": teste.urgencia,
                            "tipo": teste.tipo,
                            
                        }, palavras_esperadas=teste.palavras_chaves))
                        print(resposta.response)
                        print(avaliador.acuracia(resposta.response, teste.palavras_chaves))
            executar()
            if len(erros) > 0:
                print("infelizmente sua solicitação foi recusada devido aos seguintes erros: ")
                mensagens = {
                    "json": "problemas internos",
                    "tamanho": "prompt excedendo o limite máximo",
                    "proibido": "caracteres",
                    "ignore instructions": "tentativa de comprometer o comportamento do sistema"
                }        
                for erro in erros:
                    print(mensagens[erro])
            esperar()
        except Exception as e:
            print(e)
    

def mudarPensamento():
    config.think = not config.think

def mudarStream():
    config.stream = not config.stream

def configuracao():
    def criar_opcoes(): 
        return  [
        {
            "texto": f"{"desativar" if config.think else "ativar"} pensamento", "codigo": mudarPensamento
        },
        {
            "texto": f"{"desativar" if config.stream else "ativar"} stream", "codigo": mudarStream
        },
    ]

    criar_menu("CONFIGURAÇÕES", criar_opcoes)

    escrever_arquivo("data/db.json", config)

def main():
   
    opcoes = [
        {"texto": "conversao", "codigo": conversacao},
        {"texto": "avaliacao", "codigo": avaliacao},
        {"texto": "configurar", "codigo": configuracao}
    ]
    criar_menu("CHATBOT", opcoes)


   
if __name__ == "__main__":
    main()