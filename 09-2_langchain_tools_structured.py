from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# descrever os argumentos que serão recebidos pela função
class RetornaTempArgs(BaseModel):
    localidade: str = Field(description='Localidade a ser buscada', examples=['São Paulo', 'Porto Alegre', 'Curitiba'])

# criar a função
def retorna_temperatura_atual(localidade: str):
    return '25 C'

# criar a função com StructuredTool
tool_temp = StructuredTool.from_function(
    func=retorna_temperatura_atual,
    name='ToolTemperatura',
    args_schema=RetornaTempArgs,
    description='Faz busca online de temperatura de uma localidade',
    return_direct=True,
)

# dados da tool
print(tool_temp)
print(tool_temp.name)
print(tool_temp.args)
print(tool_temp.description)

# rodar a tool
resposta = tool_temp.invoke({'localidade' : 'Porto Alegre'})
print(resposta)


