from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List
import csv

load_dotenv()

class ItensReceita(BaseModel):
    '''Utensilios e igrendientes de uma receita'''
    utensilios: List[str] = Field(description='utensílios de cozinha que são utilizados para preparar a receira.', examples=['espátula', 'liquidificador'])
    ingredientes: List[str] = Field(description='igredientes utilizados para preparar a receita.', examples=['ovo', 'farinha', 'cenoura'])

tool_itens = convert_to_openai_function(ItensReceita)

chat = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

prompt = ChatPromptTemplate.from_messages([
    ('system', ''''
     Você é um assistente que extrai os utensílios (por exemplo: liquidificador, batedeira, espatula, etc)
     e também os igredientes (por exemplo: ovos, mação, farinha, etc) da receita fornecida pelo user.
     
     Tenha muita atenção em cada ítem, não pode faltar nada. Se faltar, minha lista de compra estará incompleta.

     Pare e pense antes de dar a resposta.
     '''
     ),
    ('user', '{input}')
])

chain = (prompt
         | chat.bind(functions=[tool_itens], function_call={'name' : 'ItensReceita'})
         | JsonOutputFunctionsParser()
)

receita = ''''
Receita de Bolo de Cenoura

Em um liquidificador, adicione a cenoura, os ovos e o óleo, depois misture.
Acrescente o açúcar e bata novamente por 5 minutos.
Em uma tigela ou na batedeira, adicione a farinha de trigo e depois misture novamente.
Acrescente o fermento e misture lentamente com uma colher.
Asse em um forno preaquecido a 180° C por aproximadamente 40 minutos.
Cobertura
Despeje em uma tigela a manteiga, o chocolate em pó, o açúcar e o leite, depois misture.
Leve a mistura ao fogo e continue misturando até obter uma consistência cremosa, depois despeje a calda por cima do bolo.
'''

respostas = chain.invoke({'input' : receita})

def salvar_em_csv(nome_arquivo, nome_coluna, lista):
    with open(f'{nome_arquivo}.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([nome_coluna])
        for item in lista:
            writer.writerow([item])
 
salvar_em_csv('utensilios', 'Utensílios', respostas['utensilios'])
salvar_em_csv('ingredientes', 'Ingredientes', respostas['ingredientes'])