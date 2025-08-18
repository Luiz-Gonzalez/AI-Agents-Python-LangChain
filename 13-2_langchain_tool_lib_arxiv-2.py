### Instanciando tool já criada no LangChain: customizável médio
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper


tool_arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=2))

# para verificar se ficou tudo certo
# print('Descrição: ', tool_arxiv.description)
# print('Argumentos: ', tool_arxiv.args)

resposta = tool_arxiv.run({'query' : 'LLM'})
print(resposta)