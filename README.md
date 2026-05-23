
# CP03 IA EQUIPE101 Smart Assistant

## Estruturas de pastas

```
── 📁checkpoint3
    └── 📁data
        ├── attack_dataset.json # teste para 
        ├── db.json # pequeno arquivo de banco de dados para salvar as configurações
        ├── test_dataset.json # testes de uso comum
    └── 📁docs
        ├── .gitkeep
    └── 📁output
        └── 📁graficos
            ├── .gitkeep
        ├── .gitkeep
        ├── eval_results.csv
    └── 📁prompts
        └── 📁classificacao
            └── 📁versions
                ├── v1.txt
                ├── v2.txt
            ├── system_prompt.txt
        └── 📁versions
            ├── v1.txt
            ├── v2.txt
            ├── v3.txt
        ├── system_prompt.txt
    └── 📁src
        └── 📁__pycache__
        ├── __init__.py
        ├── chain.py 
        ├── evaluator.py
        ├── guardrails.py
        ├── llm_client.py
        ├── prompts.py
        ├── schemas.py
        ├── ui.py # funções para interface de terminal
        ├── utils.py # funções utilitarias
    ├── .env.example
    ├── main.py
    ├── README.md
    └── requirements.txt

```



## baixando projeto

com as dependências instaladas, clone o repositorio do projeto em seu computador e depois entre na pasta


```base

git clone https://github.com/Joao-Lucas-Si/checkpoint3-ia.git


cd CP02_IA_EQUIPE101_prompt-toolkit
```

## instalação de dependências


### python e pip

instale as dependências referentes ao python a partir do arquivo requirements.txt

```base
pip install -r requirements.txt
```

### ollama


para instalação, primeiro é necessário ter o ollama em sua maquina, siga as instruções do [site oficial](https://ollama.com/download), ou copie esses comandos em sua respectiva maquina:


#### Windows


```bash

irm https://ollama.com/install.ps1 | iex

```
 

#### Linux


```bash

curl -fsSL https://ollama.com/install.sh | sh

```


#### MacOS
 

```base

curl -fsSL https://ollama.com/install.sh | sh

```




### Execusão do modelo
 
após ter o ollama em sua maquina, rode com o modelo preferido


```base

ollama run gpt-oss:120b

```

## Configuração

caso seja necessário mudar o endereço do localhost ou o modelo utilizado, personalize o arquivo .env.example e coloque os valores desejados

```env
HOST=http://localhost:11434
MODEL=gpt-oss:120b
```

## Excusão

dentro do diretório do projeto, rode o arquivo main.py


```bash

python main.py

``` 
