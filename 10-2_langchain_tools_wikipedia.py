# tool de busca na Wikipedia
import wikipedia
from langchain.agents import tool
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from dotenv import load_dotenv

load_dotenv()

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

tools = [convert_to_openai_function(busca_wikipedia)]

chain = prompt | chat.bind(functions=tools)

# objetivo aqui é apenas ver que está sendo chamada a tool
query = 'quem foi Isaac Asimov?'
resposta = chain.invoke({'input' : query})
print(resposta)

