from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# criar uma classe to tipo Enum
class UnidadeEnum(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'

# criar um padrão de dados com pydantic
class ObterTemperaturaAtual(BaseModel):
    '''Obtém a temperatura atual de uma determinada localidade'''
    local: str = Field(description='O nome da cidade.', examples=['São Paulo', 'Porto Alegre'])
    unidade: Optional[UnidadeEnum]

# converter para um padrao de funcao da OpenAI
tool_temperatura = convert_to_openai_function(ObterTemperaturaAtual)

chat = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

# chamar o model passando a funcao
resposta = chat.invoke('Qual é a temperatura de Porto Alegre?', functions=[tool_temperatura])

# adicionar funcao no chat para nao precisar toda hora ficar passando
chat_com_func = chat.bind(functions=[tool_temperatura])
resposta = chat_com_func.invoke('Qual é a temperatura de Porto Alegre?')

# obrigar o modelo a sempre usar a function
resposta = chat.invoke(
    'Qual é a temperatura de Porto Alegre?',
    functions=[tool_temperatura],
    function_call={'name' : 'ObterTemperaturaAtual'}
    )

# colocando na chain

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável chamado Isaac'),
    ('user', '{input}')
])

chain = prompt | chat.bind(functions=[tool_temperatura])

retorno = chain.invoke({'input' : 'Qual a temperatura em São Paulo?'})

print(retorno)