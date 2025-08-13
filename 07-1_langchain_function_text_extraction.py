# extrair dados de um texto
from pydantic import BaseModel, Field
from typing import List
from langchain_core.utils.function_calling import convert_to_openai_function
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from pprint import pprint

load_dotenv()

class Acontecimento(BaseModel):
    '''Informação sobre um acontecimento'''
    data: str = Field(description='Data do acontecimento no formato YYYY-MM-DD')
    acontecimento: str = Field(description='Acontecimento extraído do texto')

class ListaAcontecimentos(BaseModel):
    '''Acontecimentos para extração'''
    acontecimentos: List[Acontecimento] = Field(description='Lista de acontecimentos presentes no texto informado')

tool_acontecimentos = convert_to_openai_function(ListaAcontecimentos)

prompt = ChatPromptTemplate.from_messages([
    ('system','Extraia as frases de acontecimentos. Elas devem ser extraídas integralmente.'),
    ('user', '{input}')
])

chat = ChatOpenAI(model='gpt-4.1-nano')

chain = (prompt
         | chat.bind(functions=[tool_acontecimentos], function_call={'name' : 'ListaAcontecimentos'})
         | JsonKeyOutputFunctionsParser(key_name='acontecimentos'))

texto = '''A Apple foi fundada em 1 de abril de 1976 por Steve Wozniak, Steve Jobs e Ronald Wayne 
com o nome de Apple Computers, na Califórnia. O nome foi escolhido por Jobs após a visita do pomar 
de maçãs da fazenda de Robert Friedland, também pelo fato do nome soar bem e ficar antes da Atari 
nas listas telefônicas.

O primeiro protótipo da empresa foi o Apple I que foi demonstrado na Homebrew Computer Club em 1975, 
as vendas começaram em julho de 1976 com o preço de US$ 666,66, aproximadamente 200 unidades foram 
vendidas,[21] em 1977 a empresa conseguiu o aporte de Mike Markkula e um empréstimo do Bank of America.'''

resposta = chain.invoke({'input' : texto})
pprint(resposta)