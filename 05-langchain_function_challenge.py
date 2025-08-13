# exercício proposto no curso para fazer filtragem de e-mails

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from enum import Enum
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# classes
class TipoEmail(str, Enum):
    todos = 'todos'
    nao_lidos = 'não lidos'
    lidos = 'lidos'

class obter_emails(BaseModel):
    '''Conta e filtra emails de acordo com o status solicitado'''
    tipo: TipoEmail = Field(description='Tipo de email que foi solicitado para filtrar')
    quantidade: int = Field(description='Número exato de emails encontrados com o tipo especificado na lista fornecida')

# criação da tool
tool_filtrar_emails = convert_to_openai_function(obter_emails)

# inicializar modelo
chat = ChatOpenAI(model='gpt-4o-mini')  # Modelo corrigido

# prompt melhorado
prompt = ChatPromptTemplate.from_messages([
    ('system', '''Você é um assistente que conta emails por tipo. 
    Sua tarefa é:
    1. Analisar a lista de emails fornecida
    2. Contar quantos emails têm o campo "tipo" igual ao tipo solicitado
    3. Retornar o tipo solicitado e a quantidade EXATA encontrada
    
    IMPORTANTE: Conte apenas os emails que têm EXATAMENTE o tipo solicitado.'''),
    
    ('user', '''Conte quantos emails da lista abaixo têm o campo "tipo" igual a "{tipo}".

Lista de emails:
{lista_emails}

Tipo solicitado: {tipo}

Analise cada email individualmente e conte apenas aqueles que têm o campo "tipo" exatamente igual a "{tipo}".''')
])

# chain
chain = (prompt 
         | chat.bind(functions=[tool_filtrar_emails], function_call={'name' : 'obter_emails'})
         | JsonOutputFunctionsParser()
)

# Dados de teste
emails = [
    {
        'remetente': 'luizgonzalez2@gmail.com',
        'assunto': 'Entrega',
        'tipo': 'lidos',
    },
    {
        'remetente': 'karlamoura@gmail.com',
        'assunto': 'Oportunidade',
        'tipo': 'lidos',
    },
    {
        'remetente': 'joao@empresa.com',
        'assunto': 'Reunião',
        'tipo': 'lidos',
    },
    {
        'remetente': 'maria@teste.com',
        'assunto': 'Proposta',
        'tipo': 'lidos',
    }
]

# Teste com diferentes tipos
print("=== TESTES ===")

print("\nTestando 'lidos':")
status = 'lidos'
resposta = chain.invoke({'tipo': status, 'lista_emails': emails})
print(f"Resposta: {resposta}")

print("\nTestando 'não lidos':")
status = 'não lidos'
resposta = chain.invoke({'tipo': status, 'lista_emails': emails})
print(f"Resposta: {resposta}")