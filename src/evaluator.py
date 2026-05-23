from typing import Union
import matplotlib.pyplot as plt
from src.schemas import ClassificacaoSchema

class Avaliador():
    def acuracia(self, valor: str|dict, esperado: dict|str|list[str|list[str]]) -> float:
        correspontencias = 0
        if isinstance(valor, dict) and isinstance(esperado, dict):
            for name in esperado.keys():
                if name in valor:
                    correspontencias += self.acuracia(valor[name], esperado[name])
            correspontencias /= len(esperado.items())
        elif isinstance(valor, dict) or isinstance(esperado, dict):
            correspontencias = 0
        elif isinstance(esperado, list):
            for item in esperado:
                if isinstance(item, list):
                    for palavra in item:
                        if palavra.lower() in valor.lower():
                            correspontencias += 1
                            break
                else:
                    if item.lower() in valor.lower():
                        correspontencias += 1
            correspontencias /= len(esperado)
        else:
            if esperado.lower() == valor.lower():
                correspontencias = 1
            
                
        return correspontencias

    def json(self, registros: list[dict]):
        erros = [erro 
             for registro in registros
             for erro in registro["erros"] 
            ]
        
        json_erros = [erro for erro in erros if erro == "json"]

        return len(json_erros)
    
    def bloqueios(self, registros: list[dict]):
        bloqueio = []
        for registro in registros:
            if len(registro["erros"])> 0:
                bloqueio.append(registro)

        return len(bloqueio)

    def falso_positivo(self, registros: list[dict]):
        bloqueio = []
        for registro in registros:
            if len(registro["erros"])> 0 and registro["tipo"] == "teste":
                print("bloqueio")
                bloqueio.append(registro)

        return len(bloqueio)

    def calc_consistencia(self, registro: list[dict]):
        if len(registro) == 0:
            return 1
        elif len(registro) == 1:
            return 0
        
        def comparar(obj: dict, ot: dict):
            consistencia = 0
            for name in obj.keys():
                if obj[name] == ot[name]:
                    consistencia += 1
            return consistencia / len(obj.keys())
        consistencia = 0
        for i in range(len(registro) - 2):
            consistencia += comparar(registro[i], registro[i+1])
        return consistencia / 3

def criar_graficos(registros: list[dict], consistencia_lista: list[list[ClassificacaoSchema]]):
    avaliador = Avaliador()

    print([avaliador.acuracia(registro["classificacao"], registro["esperado"]) for registro in registros if "classificacao" in registro and registro["classificacao"] is not None])
    acuracia = sum([avaliador.acuracia(registro["classificacao"], registro["esperado"]) for registro in registros if "classificacao" in registro  and registro["classificacao"] is not None])

    json = avaliador.json(registros)

    bloqueios = avaliador.bloqueios(registros)
    
    falsos_positivos = avaliador.falso_positivo(registros)
    
    consistencia = sum([avaliador.calc_consistencia([classificacao.model_dump() for classificacao in classificacoes]) for classificacoes in consistencia_lista]) / len(consistencia_lista)

    nomes = ['Acuracia', 'json', 'bloqueios', 'falsos positivos', "Consistencia"]
    metricas = [acuracia, json, bloqueios, falsos_positivos, consistencia]
    print(metricas)
    plt.ylim(0, len(registros))
    plt.bar(nomes, metricas)
    plt.title('analise')
    plt.ylabel('registros')
    plt.xlabel('métricas')
    plt.savefig(f"output/graficos/metricas.png", pad_inches=1, orientation="portrait")
    plt.close()

