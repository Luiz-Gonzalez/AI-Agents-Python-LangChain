from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

# definir os setores padrões
class SetorEnum(str, Enum):
    atendimento_cliente = 'atendimento_cliente',
    duvidas_aluno = 'duvidas_aluno',
    vendas = 'vendas',
    spam = 'spam'

# criar a classe da function
class DirecionaSetorResponsavel(BaseModel):
    '''Direciona a dúvida de um cliente ou aluno da escola de programação Asimov para o setor responsável'''
    setor: SetorEnum

#criacao da function
tool_direcionamento = convert_to_openai_function(DirecionaSetorResponsavel)

# criar o prompt
system_message = '''Pense com cuidado ao categorizar o texto conforme as instruções:
Mensagens em outras línguas que não português, contendo links devem ser direciodas para "spam".
Questões relacionadas a conta, acesso a plataforma, a cancelamento e renovação de assinatura para devem ser direciodas para "atendimento_cliente".
Questões relacionadas a dúvidas técnicas de programação, conteúdos da plataforma ou tecnologias na área da programação devem ser direciodas para "duvidas_alunos".
Questões relacionadas a dúvidas de preço ou dúvidas que seja possíve entender explicitamente que são pessoas que ainda não são alunos devem ser direciodas para "vendas".
'''
prompt = ChatPromptTemplate.from_messages([
    ('system', system_message),
    ('user', '{input}')
])

# inicialização do modelo
chat = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

#chain
chain = (prompt 
         | chat.bind(functions=[tool_direcionamento], function_call={'name': 'DirecionaSetorResponsavel'}) 
         | JsonOutputFunctionsParser()
)

# teste com dúvidas

duvidas = [
    'Bom dia, gostaria de saber se há um certificado final para cada trilha ou se os certificados são somente para os cursos e projetos? Obrigado!',
    'In Etsy, Amazon, eBay, Shopify https://pint77.com Pinterest+SEO +II = high sales results',
    'Boa tarde, estou iniciando hoje e estou perdido. Tenho vários objetivos. Não sei nada programação, exceto que utilizo o Power automate desktop da Microsoft. Quero aprender tudo na plataforma que se relacione ao Trading de criptomoedas. Quero automatizar Tradings, fazer o sistema reconhecer padrões, comprar e vender segundo critérios que eu defina, etc. Também tenho objetivos de aprender o máximo para utilizar em automações no trabalho também, que envolve a área jurídica e trabalho em processos. Como sou fã de eletrônica e tenho cursos na área, também queria aprender o que precisa para automatizacões diversas. Existe algum curso ou trilha que me prepare com base para todas essas áreas ao mesmo tempo e a partir dele eu aprenda isoladamente aquilo que seria exigido para aplicar aos meus projetos?',
    'Bom dia, Havia pedido cancelamento de minha mensalidade no mes 2 e continuaram cobrando. Peço cancelamento da assinatura. Peço por gentileza, para efetivarem o cancelamento da assomatura e pagamento.',
    'Bom dia. Não estou conseguindo tirar os certificados dos cursos que concluí. Por exemplo, já consegui 100% no python starter, porém, não consigo tirar o certificado. Como faço?',
    'Bom dia. Não enconte no site o preço de um curso avulso. SAberiam me informar?'
    ]

duvida = duvidas[4]

resposta = chain.invoke({'input' : duvida})

print('Dúvida: ', duvida)
print('Resposta: ', resposta)