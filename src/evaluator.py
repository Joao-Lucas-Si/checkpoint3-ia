from typing import Union

class Avaliador():
    def acuracia(self, valor: str|dict, esperado: dict|str|list[str|list[str]]) -> float:
        correspontencias = 0
        if isinstance(valor, dict) and isinstance(esperado, dict):
            for (name, valor) in esperado.items():
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
            print(correspontencias)
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
    
    def bloqueios(self):
        pass

    def falso_positivo(self):
        pass

    def consistencia(self):
        pass
