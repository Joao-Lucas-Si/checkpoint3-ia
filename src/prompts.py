from src.schemas import ClassificacaoSchema, ProcessamentoSchema

def montar_prompt(classificacao: ClassificacaoSchema, processamento: ProcessamentoSchema, input: str):
    prompt = f"""[classificação]
    {classificacao.model_dump_json()}
    
    [processamento]
    {processamento.model_dump_json()}
    
    [input do aluno]
    {input}
    """
    
    return prompt
    