from src.llm_client import LLM_Client
from src.schemas import RespostaSchema, ClassificacaoSchema, ProcessamentoSchema, ProcessamentoElogioSchema, ProcessamentoDuvidaSchema, ProcessamentoReclamacaoSchema, ProcessamentoSugestaoSchema
from src.utils import ler_arquivo
from src.prompts import montar_prompt
import json

cliente_classificador = LLM_Client(ler_arquivo("prompts/classificacao/system_prompt.txt"), format=ClassificacaoSchema.model_json_schema())

class AssistantChain:
    prompt: str

    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
    def classificar(self):
        resposta = cliente_classificador.chamar(self.prompt)
        if isinstance(resposta, RespostaSchema):
            js = json.loads(resposta.response)
            classificacao = ClassificacaoSchema(**js)

            return classificacao
        
    def processar(self, classificacao: ClassificacaoSchema) -> ProcessamentoSchema|list[str]:
        erros: list[str] = []
        try:
            schema: dict
            sistema: str
            match classificacao.tipo:
                case "duvida":
                    sistema = "você receberá uma dúvida de um usuário e deve gerar uma resposta direta(resolucao) e uma breve analise, além de captar opcionalmente o sentimento presente"
                    schema = ProcessamentoDuvidaSchema.model_json_schema()
                case "elogio":
                    sistema = "você receberá um elogio de um usuário, você deve classificar o elogio em niveis de alto, medio e baixo, além de identificar o que foi elogiado"
                    schema = ProcessamentoElogioSchema.model_json_schema()
                case "reclamacao":
                    sistema = "você receberá uma reclamação de um usuário e deve extrair o problema central e fazer uma breve analise, além de captar opcionalmente o sentimento presente"
                    schema = ProcessamentoReclamacaoSchema.model_json_schema()
                case "sugestao":
                    sistema = ""
                    schema = ProcessamentoSugestaoSchema.model_json_schema()
            
            client = LLM_Client(sistema, format=schema)
            
            resposta = client.chamar(self.prompt)
            if isinstance(resposta, RespostaSchema):
                js = json.loads(resposta.response)
                processamento = ProcessamentoSchema(**js)

                return processamento
        except Exception as e:
            erros.append("json")
        return erros


    def responder(self, classificacao: ClassificacaoSchema, processamento: ProcessamentoSchema):
        prompt = montar_prompt(classificacao, processamento, self.prompt)
        client = LLM_Client(sistema= ler_arquivo("prompts/system_prompt.txt"))

        resposta = client.chamar(prompt)
        
        return resposta
   