### Criando tool através do load_tools: pouca customização
from langchain_community.agent_toolkits.load_tools import load_tools

tools = load_tools(['arxiv'])
tool_arxiv = tools[0]

# para verificar se ficou tudo certo
# print('Descrição: ', tool_arxiv.description)
# print('Argumentos: ', tool_arxiv.args)

resposta = tool_arxiv.run({'query' : 'LLM'})
print(resposta)