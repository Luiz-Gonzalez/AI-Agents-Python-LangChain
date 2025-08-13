from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os

# Use sua chave da OpenRouter
os.environ["OPENAI_API_KEY"] = ""

# Nome do modelo exato (veja no site do OpenRouter)
chat = ChatOpenAI(
    model="moonshotai/kimi-dev-72b:free",  # ou outro modelo disponível
    temperature=1,
    openai_api_base="https://openrouter.ai/api/v1",
)

resposta = chat.invoke([
    HumanMessage(content="resposta curta e direta: de que cor é a melancia por fora?"),
])

print(resposta.content)
