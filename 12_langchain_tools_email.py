from email.message import EmailMessage
import smtplib
import ssl
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from pprint import pprint
from langchain.agents.agent import AgentFinish

# variáveis de ambiente
load_dotenv()
senha_email = os.environ['SENHA_EMAIL']
email_remetente = os.environ['EMAIL']

# classe dos dados do email a serem passadas como argumentos
class DadosEmailArgs(BaseModel):
    destinatario: str = Field(description='e-mail do destinatário')
    titulo: str = Field(description='Título do e-mail que será enviado')
    corpo: str = Field(description='Corpo do e-mail, ou seja, o texto que será enviado.')

# tool que envia e-mails
@tool (args_schema=DadosEmailArgs)
def envia_email(destinatario, titulo, corpo):
    '''Envia e-mail'''
    email_usuario = email_remetente
    senha_app = senha_email
    message_email = EmailMessage()
    message_email['From'] = email_usuario
    message_email['To'] = destinatario
    message_email['Subject'] = titulo

    message_email.set_content(corpo)
    safe = ssl.create_default_context()

    with smtplib.SMTP_SSL('br.avatar4040.com.br', 465, context=safe) as smtp:
        smtp.login(email_usuario, senha_app)
        smtp.sendmail(email_usuario, destinatario, message_email.as_string())

# model
chat = ChatOpenAI(model='gpt-4.1-nano')

#prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente que envia e-mails conforme dados passados.'),
    ('user', '{user_input}')
])

tools = [envia_email]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

# router
def roteamento(resultado):
    if isinstance(resultado, AgentFinish):
        return resultado.return_values['output']
    else:
        return tool_run[resultado.tool].run(resultado.tool_input)

# chain
chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | roteamento

retorno = chain.invoke({'user_input' : 'Preciso que voce envie um email para karlamoura@gmail.com com o título "oiee" e com o corpo do email "Como vai?"'})

pprint(retorno)