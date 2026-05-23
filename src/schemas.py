
from pydantic import BaseModel
from typing import Union, Literal, Optional

type ClassificacaoTipos = Literal["reclamacao", "duvida", "elogio", "sugestao"]

type UrgenciaTipos = Literal["alta", "media", "baixa"]

class ClassificacaoSchema(BaseModel):
    tipo: ClassificacaoTipos
    urgencia: UrgenciaTipos
    tema: str


class ProcessamentoSchema[T](BaseModel):
    dados_extraidos: T
    analise: str
    sentimento: Optional[str]

class DadosExtraidosReclamacaoSchena(BaseModel):
    problema: str


class DadosExtraidosSugestaoSchena(BaseModel):
    aspecto: str
    resolucao: str

class DadosExtraidosElogioSchena(BaseModel):
    nivel: Literal["alto","medio","baixo"]
    aspect: str
    
class DadosExtraidosDuvidaSchena(BaseModel):
    resolucao: str  
    duvida_central: str


class ProcessamentoElogioSchema(ProcessamentoSchema[DadosExtraidosElogioSchena]):
    pass   


class ProcessamentoDuvidaSchema(ProcessamentoSchema[DadosExtraidosDuvidaSchena]):
    pass   


class ProcessamentoSugestaoSchema(ProcessamentoSchema[DadosExtraidosSugestaoSchena]):
    pass   


class ProcessamentoReclamacaoSchema(ProcessamentoSchema[DadosExtraidosReclamacaoSchena]):
    pass   

class RespostaSchema(BaseModel):
    total_duration: int
    response: str
    thinking: Optional[str] =None
    done: bool

class TestCasoSchema(BaseModel):
    input: str
    tipo: ClassificacaoTipos
    urgencia: UrgenciaTipos
    palavras_chaves: list[Union[str, list[str]]]

class TestDatasetSchema(BaseModel):
    casos: list[TestCasoSchema]

class AttackDatasetSchema(BaseModel):
    pass


class ConfigSchema(BaseModel):
    temperatura: float
    think: bool
    stream: bool
    
class RegistroSchema(BaseModel):
    resposta: str
    duracao: int
    classificacao: Optional[ClassificacaoSchema]
    processamento: Optional[ProcessamentoSchema]
    esperado: dict
    palavras_esperadas: list[str|list[str]]
    