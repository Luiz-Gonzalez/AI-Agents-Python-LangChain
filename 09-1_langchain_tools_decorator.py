from langchain.agents import tool
from pydantic import BaseModel, Field


# descrever os argumentos que serão recebidos pela função
class RetornaTempArgs(BaseModel):
    localidade: str = Field(description='Localidade a ser buscada', examples=['São Paulo', 'Porto Alegre', 'Curitiba'])

# criar a função com decorator
@tool(args_schema=RetornaTempArgs)
def retorna_temperatura_atual(localidade: str):
    '''Faz busca online de temperatura de uma localidade'''
    return '25 C'

# chamar a tool: agora que tem o decorator ele ganha um método, como todos os runnables
resposta = retorna_temperatura_atual.invoke({'localidade' : 'Porto Alegre'})
print(resposta)