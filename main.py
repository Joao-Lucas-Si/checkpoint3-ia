from src.llm_client import LLM_Client
from src.utils import ler_arquivo, esperar, escrever_arquivo
from src.schemas import TestDatasetSchema, ConfigSchema, RespostaSchema, ProcessamentoSchema, RegistroSchema, ClassificacaoSchema, TestCasoSchema
from src.evaluator import Avaliador, criar_graficos
from src.guardrails import Input_Guardrail, validar_output
from src.ui import criar_menu
from typing import Callable, Optional
from src.chain import AssistantChain
import types

persona = ler_arquivo("prompts/system_prompt.txt")

config = ler_arquivo("data/db.json", ConfigSchema)

client = LLM_Client(sistema=persona, temperatura=config.temperatura, think=config.think, stream=config.stream)


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
    registros: list[RegistroSchema] = []
    testes = ler_arquivo("data/test_dataset.json", TestDatasetSchema)
    consistencias: list[list[ClassificacaoSchema]] = []
    for teste in testes.casos:
        consistencias.append([])
        print(teste.input)
        
        
        erros: set[str] = set()
        try:
            def executar():
                chain = AssistantChain(teste.input)
                avaliador = Avaliador()
                registro = RegistroSchema(erros=erros, tipo = "teste" if isinstance(teste, TestCasoSchema) else "ataque", duracao=0 ,resposta="", esperado={
                        "urgencia": teste.urgencia,
                        "tipo": teste.tipo,
                        "tema": teste.tema
                    }, palavras_esperadas=teste.palavras_chaves)
                registros.append(registro)
                input_guardrail = Input_Guardrail(teste.input)
                erros.update(input_guardrail.validar_input())
                if len(erros) > 0:
                    registro.erros =erros
                    return
                classificacao = chain.classificar()
                print("classificacao", classificacao)
                registro.classificacao = classificacao
                processamento: Optional[ProcessamentoSchema] = None
                
                if isinstance(classificacao, ClassificacaoSchema):
                    consistencias[len(consistencias) - 1].append(classificacao)
                    resultado = chain.processar(classificacao)
                    
                    if isinstance(resultado, ProcessamentoSchema):
                        processamento = resultado
                    else:
                        erros.update(resultado)
                    print("processamento", processamento)
                registro.processamento = processamento
                if len(erros) == 0 and classificacao and processamento:
                    resposta = chain.responder(classificacao, processamento)
                    if isinstance(resposta, RespostaSchema):
                        registro.resposta = resposta.response
                        output = validar_output(registro.resposta, teste.palavras_chaves)
                        
                        if output[0]:
                            print(resposta.response)
                        else:
                            erros.update(output[1])
               
                for i in range(2):
                    classificacao_teste = chain.classificar()
                    if isinstance(classificacao_teste, ClassificacaoSchema):
                        consistencias[len(consistencias) - 1].append(classificacao_teste)
                
            executar()
            
        except Exception as e:
            print(e)
        if len(erros) > 0:
            print("infelizmente sua solicitação foi recusada devido aos seguintes erros: ")
            mensagens = {
                "json": "problemas internos",
                "tamanho": "prompt excedendo o limite máximo",
                "proibido": "caracteres",
                "ignore instructions": "tentativa de comprometer o comportamento do sistema",
                "fora do dominio": "resposta do contexto esperado"
            }        
            for erro in erros:
                print(mensagens[erro])
    try:
        criar_graficos([registro.model_dump() for registro in registros], consistencias)
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