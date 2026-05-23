from typing import Literal, Type, TypeVar, overload, Union, Optional
import json
from pydantic import BaseModel
import os


def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar():
    input("\nPressione Enter para continuar")
    limpar()

type JSONS = Literal["data/attack_dataset.json", "data/test_dataset.json", "data/db.json"]

type TEXTOS = Literal["prompts/system_prompt.txt", "prompts/classificacao/system_prompt.txt"]

T = TypeVar("T")

@overload
def ler_arquivo(value: JSONS, schema: Type[T]) -> T: ...

@overload
def ler_arquivo(value: TEXTOS) -> str: ...


def ler_arquivo(value: Union[TEXTOS, JSONS], schema: Optional[Type[T]] = None):
    conteudo: str

    with open(value, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    if value.endswith(".json"):
        if schema is None:
            raise ValueError
        dic = json.loads(conteudo)

        instancia = schema(**dic)

        return instancia

    return conteudo

@overload
def escrever_arquivo(valor: JSONS, conteudo: BaseModel) -> None: ...

@overload
def escrever_arquivo(valor: TEXTOS, conteudo: str) -> None: ...

def escrever_arquivo(valor: Union[TEXTOS, JSONS], conteudo: BaseModel|str) -> None:
    with open(valor, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo.model_dump_json() if isinstance(conteudo, BaseModel) else conteudo)