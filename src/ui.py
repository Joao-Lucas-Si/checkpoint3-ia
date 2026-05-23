from typing import Callable
from src.utils import limpar

def criar_menu(titulo: str, pegar_opcoes: list[dict]|Callable[[], list[dict]]):
    while True:
        opcoes = pegar_opcoes if isinstance(pegar_opcoes, list) else pegar_opcoes()
        print(f"----- {titulo} -----")
        print("escolha o que deseja fazer")
        print("0 - fechar")
        for index, opcao in enumerate(opcoes):
            print(f"{index + 1} - {opcao["texto"]}")

        try:
            escolha = int(input("escolha: "))
            limpar()
            if (escolha == 0):
                break

            escolha -= 1

            if escolha < 0 or escolha > len(opcoes):
                print("opcao invalida")
                continue

            opcoes[escolha]["codigo"]()
        except:
            print("valor invalido")