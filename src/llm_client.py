import requests
import os
import json
from typing import Optional, Callable, Union

from src.schemas import RespostaSchema

class LLM_Client:
    sistema: Optional[str]
    max_tokens: int
    temperatura: float
    think: bool
    stream: bool
    formato: Optional[str|dict]

    def __init__(self, sistema: Optional[str] = None , max_tokens: int = 250, temperatura: float = 0.5, think: bool = False, stream: bool = False, format:Optional[str|dict] = None) -> None:
        self.sistema = sistema
        self.max_tokens = max_tokens
        self.stream = stream
        self.think = think
        self.temperatura = temperatura
        self.formato = format

    def chamar(self, prompt: str, system: Optional[str] = None,  max_tokens: Optional[int] = None, temperatura: Optional[float] = None) -> Union[RespostaSchema, Callable[[Callable[[str], None]], None]]:
        persona = system or self.sistema
        max = max_tokens or self.max_tokens
        temp = temperatura or self.temperatura
        host = os.getenv("HOST", "http://localhost:11434/")
        model = os.getenv("MODEL", "qwen3.5:0.8b")
     
        resposta = requests.post(f"{host}api/generate", stream=self.stream, json= {
            "model": model,
            "prompt": prompt,
            "system": persona,
            "stream": self.stream,
            "think": self.think,
            "format": self.formato,
            "options": {
                "temperature": temp,
                "num_predict": max
            }
        })
        if self.stream:
            resposta.raise_for_status()
            def observador(callback: Callable[[str], None]):
                for parte in resposta.iter_lines():
                    if not parte:
                        continue

                    conteudo = json.loads(parte)

                    callback(conteudo["response"])    
                    if conteudo["done"]:
                        break

            return observador
        conteudo = resposta.json()

        dados = RespostaSchema(**conteudo)

        return dados