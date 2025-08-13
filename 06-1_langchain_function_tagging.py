from pydantic import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

load_dotenv()

# classe da funcao
class Sentimento(BaseModel):
    '''Define o sentimento e a língua da mensagem enviada'''
    sentimento: str = Field(description='Sentimento do texto. Deve ser "pos", "neg" ou "nd" para não definido.')
    lingua: str = Field(description='Língua em que o texto foi escrito. Deve estar no formato ISO 639-1')

# criacao da funcao
tool_sentimento = convert_to_openai_function(Sentimento)

# criacao do prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', 'pense com cuidado ao categorizar o texto conforme as instruções'),
    ('user', '{input}')
])

# inicialização do modelo
chat = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

#criação da chain
chain = (
         prompt
         | chat.bind(functions=[tool_sentimento], function_call={'name' : 'Sentimento'}) # name: Sentimento -> Porque convert_to_openai_function usa o nome da classe como o name da função
         | JsonOutputFunctionsParser()
)

texto = 'I dont like peanutbutter'

resposta = chain.invoke({'input' : texto})

print(resposta)