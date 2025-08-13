# prompt + model
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4.1-nano-2025-04-14')

prompt = ChatPromptTemplate.from_template('Crie uma frase sobre o seguinte: {assunto}')

chain = prompt | model

resposta = chain.invoke({'assunto' : 'Itália'})

print(resposta.content)