from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from dotenv import load_dotenv

load_dotenv()


db = SQLDatabase.from_uri('sqlite:///arquivos/Chinook.db')

chat = ChatOpenAI(model='gpt-4.1-mini')

agent_executor = create_sql_agent(
    chat,
    db=db,
    agent_type='tool-calling',
    verbose=True
)

resposta = agent_executor.invoke({'input' : 'Qual artista possui mais álbuns?'})
print(resposta)

