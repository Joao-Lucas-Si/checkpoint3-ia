import re
from src.evaluator import Avaliador

def validar_output(resposta: str, palavras_chaves: list[str|list[str]]):
    avaliador = Avaliador()
    
    return [True, []] if avaliador.acuracia(resposta, palavras_chaves) > 0.3 else [False, "fora do dominio"]

class Input_Guardrail:
    prompt: str

    def __init__(self, prompt):
        self.prompt = prompt
    def proibidos(self) -> list[str]:
        characteres = ["{", "}", "<", ">", "[", "]"]
        
        for charactere in characteres:
            if charactere in self.prompt:
                return ["proibido"]
        return []; 
    def padroes(self) -> list[str]:
        palavras_chaves = [{"padrao": re.compile("ignore.+instruções"), "ataque": "ignore instructions" }, ]
        ataques = []
        for palavra in palavras_chaves:
            if palavra["padrao"].search(self.prompt):
                ataques.append(palavra["ataque"])

        return ataques
    def tamanho(self) -> list[str]:
        return ["tamanho"] if len(self.prompt) > 500 else [] 

    def validar_input(self):
        validacoes = [self.proibidos, self.padroes, self.tamanho]
        ataques = []
        for validacao in validacoes:
            ataques.extend(validacao())
        return ataques