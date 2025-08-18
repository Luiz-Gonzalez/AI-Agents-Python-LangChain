import requests
import datetime
from langchain.agents import tool
from pydantic import BaseModel, Field #Importação atualizada
import wikipedia
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from dotenv import load_dotenv
from pprint import pprint
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.schema.agent import AgentFinish
from langchain.schema.runnable import RunnablePassthrough

load_dotenv()

# TOOLS
wikipedia.set_lang('pt')

class RetornTempArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=RetornTempArgs)
def retorna_temperatura_atual(latitude: float, longitude: float):
    '''Retorna a temperatura atual para uma dada coordenada'''

    URL = 'https://api.open-meteo.com/v1/forecast'

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    resposta = requests.get(URL, params=params)
    if resposta.status_code == 200:
        resultado = resposta.json()
        
        hora_agora = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        lista_horas = [datetime.datetime.fromisoformat(temp_str) for temp_str in resultado['hourly']['time']]
        index_mais_prox = min(range(len(lista_horas)), key=lambda x: abs(lista_horas[x] - hora_agora))

        temp_atual = resultado['hourly']['temperature_2m'][index_mais_prox]
        return f'{temp_atual}ºC'
    else:
        raise Exception(f'Request para API {URL} falhou: {resposta.status_code}')

@tool
def busca_wikipedia(query: str):
    """Faz busca no wikipedia e retorna resumos de páginas para a query"""
    titulos_paginas = wikipedia.search(query)
    resumos = []
    for titulo in titulos_paginas[:3]:
        try:
            wiki_page = wikipedia.page(title=titulo, auto_suggest=True)
            resumos.append(f'Título da página: {titulo}\nResumo: {wiki_page.summary}')
        except:
            pass
    if not resumos:
        return 'Busca não teve retorno'
    else:
        return '\n\n'.join(resumos)

# MODEL
chat = ChatOpenAI()

# ORGANIZAÇÃO E INICIALIZAÇÃO DAS TOOLS
tools = [busca_wikipedia, retorna_temperatura_atual]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

#PROMPT + PASS THROUGH + CHAIN É O AGENT NO LANGCHAIN
prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado Isaac'),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad') ## Adicionando o racicínio do agent as mensagens (agent_scretchpad)
])

pass_through = RunnablePassthrough.assign(
    agent_scratchpad=lambda x:format_to_openai_function_messages(x['intermediate_steps'])
)
chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

# inicio sem nada ainda no histórico
# resposta_inicial = chain.invoke({
#     'input' : 'Qual a temperatura em Flirianópolis?',
#     'agent_scratchpad' : []
# })

# # chamar a funcao e obter o resultado
# observacao = tool_run[resposta_inicial.tool].run(resposta_inicial.tool_input)

# # roda novamente, porém agora com o histórico de chamada de funcao e a resposta
# resposta_final = chain.invoke({
#     'input' : 'Qual a temperatura em Flirianópolis?',
#     'agent_scratchpad' : format_to_openai_function_messages([(resposta_inicial, observacao)]) # lista de tuplas
# })

# pprint(resposta_final.return_values['output'])

# Loop de raciocínio: substitui todo os passos acima que estao comentados (resposta inicial e final) e deixa tudo em um loop, pois nao se sabe quantas vezes a LLM vai chamar uma funcao
# ISSO AQUI O LANGCHAIN CHAMA DE AGENT EXECUTOR
def run_agent(input):
    passos_intermediarios = []
    while True:
        resposta = chain.invoke({
            'input' : input,
            'intermediate_steps': passos_intermediarios
        })
        if isinstance(resposta, AgentFinish):
            return resposta
        observacao = tool_run[resposta.tool].run(resposta.tool_input)
        passos_intermediarios.append((resposta, observacao))

retorno = run_agent('Qual é a temperatura de Florianópolis?')
pprint(retorno)