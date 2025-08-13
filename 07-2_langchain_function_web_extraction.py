from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List
from pprint import pprint

load_dotenv()

loader = WebBaseLoader('https://fli.pet/blog/')
page = loader.load()

class BlogPost(BaseModel):
    '''Informações sobre um post de Blog'''
    titulo: str = Field(description='O título do post de blog')
    autor: str = Field(description='O autor do post de blog')
    data: str = Field(description='A data de publicação do post de blog')

class BlogSite(BaseModel):
    '''Lista de blog posts de um site'''
    posts: List[BlogPost] = Field(description='Lista de postos de blog do site.')

tool_blog = convert_to_openai_function(BlogSite)

chat = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Extraia do texto fornecido (texto de um blog) todos os posts de blog com autor e data de publicação'),
    ('user', '{input}')
])

chain = (prompt
         | chat.bind(functions=[tool_blog], function_call={'name' : 'BlogSite'})
         | JsonKeyOutputFunctionsParser(key_name='posts')
)

resposta = chain.invoke({'input' : page})
pprint(resposta)