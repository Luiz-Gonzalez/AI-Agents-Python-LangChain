import requests
import datetime
from langchain.agents import tool
from pydantic import BaseModel, Field #Importação atualizada
import wikipedia
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.agent import AgentFinish
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents import AgentExecutor
from pprint import pprint
from langchain.memory import ConversationBufferMemory

load_dotenv()

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
    
chat = ChatOpenAI(model='gpt-4.1-mini')

tools = [busca_wikipedia, retorna_temperatura_atual]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

# AGENT
prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado Isaac'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
)
agent_chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

## memória
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key='chat_history'
)

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=tools,
    memory=memory,
    verbose=True
)

# precisa fazer assim em sequência para a memória funcionar
resposta = agent_executor.invoke({'input' : 'Olá, meu nome é Luiz'})
pprint(resposta)
resposta = agent_executor.invoke({'input' : 'Qual o meu nome?'})
pprint(resposta)
resposta = agent_executor.invoke({'input' : 'Estou passando muito frio aqui em Curitiba. Veja pra mim uma cidade gostosa no nordeste do Brasil e a sua temperatura agora'})
pprint(resposta)