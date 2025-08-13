import requests
import datetime
from langchain.agents import tool
from pydantic import BaseModel, Field
import wikipedia
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from dotenv import load_dotenv
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.agent import AgentFinish

load_dotenv()

# definir os argumentos de entrada da funcao (argumentos)
class RetornaTempsArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=RetornaTempsArgs)
def retorna_temperatura_atual(latitude: float, longitude: float):
    '''Retorna a temperatura atual para uma dada coordenada'''

    URL = 'https://api.open-meteo.com/v1/forecast'

    params = {
        'latitude' : latitude,
        'longitude' : longitude,
        'hourly' : 'temperature_2m',
        'forecast_days' : 1, 
    }

    resposta = requests.get(URL, params=params)
    if resposta.status_code == 200:
        resultado = resposta.json()
        #pega o horário atual do dispositivo
        hora_agora = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        # pega a lista de horas da resposta da api
        lista_horas = [datetime.datetime.fromisoformat(temp_str) for temp_str in resultado['hourly']['time']]
        # index da lista_horas mais próximo a hora atual
        index_mais_prox = min(range(len(lista_horas)), key=lambda x: abs(lista_horas[x] - hora_agora))
        # pega a temperatura através do indice relativo ao resultado acima que é o horário mais próximo do horário atual
        temp_atual = resultado['hourly']['temperature_2m'][index_mais_prox]
        return temp_atual
    else:
        raise Exception(f'Request para API {URL} falhou: {resposta.status_code}')

wikipedia.set_lang('pt')

@tool
def busca_wikipedia(query: str):
    '''Faz busca na Wikipedia e retorna resumos de páginas para a query'''
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
    
prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado Isaac.'),
    ('user', '{input}')
])

chat = ChatOpenAI(model='gpt-4.1-nano')

tools = [busca_wikipedia, retorna_temperatura_atual]
#converter para o formato json de function da openai
tools_json = [convert_to_openai_function(tool) for tool in tools]
# transformar as tools em um dicionário
tool_run = {tool.name: tool for tool in tools}

def roteamento(resultado):
    if isinstance(resultado, AgentFinish): # verifica se resultado é uma instancia AgentFinish
        return resultado.return_values['output']
    else:
        return tool_run[resultado.tool].run(resultado.tool_input)

#OpenAIFunctionsAgentOutputParser: checa se veio uma resposta ou se o modelo solicitou para chamar uma função
chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | roteamento

# objetivo: usar mostrar se o modelo vai solicitar a tool ou vai mostrar a resposta
resultado = chain.invoke({'input' : 'Quem foi Isaac Asimov?'})
print(resultado)