from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(
    'https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv'
)

chat = ChatOpenAI(model='gpt-4.1-mini')

agent = create_pandas_dataframe_agent(
    chat,
    df,
    verbose=True,
    agent_type='tool-calling',
    allow_dangerous_code=True
)

resposta = agent.invoke({'input' : 'Quantas pessoas sobreviveram?'})
print(resposta['output'])