### Criando tool manualmente através do Wrapper: mais customizável
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class ArxivArgs(BaseModel):
    query: str = Field(description='Query de busca no ArXiv.')

# forma "mais manual" de criar uma ferramenta que já está pronta
tool_arxiv = StructuredTool.from_function(
    func=ArxivAPIWrapper(top_k_results=2).run,
    args_schema=ArxivArgs,
    name='arxiv',
    description = (
        "Uma ferramenta em torno do Arxiv.org. "
        "Útil para quando você precisa responder a perguntas sobre Física, Matemática, "
        "Ciência da Computação, Biologia Quantitativa, Finanças Quantitativas, Estatística, "
        "Engenharia Elétrica e Economia utilizando artigos científicos do arxiv.org. "
        "A entrada deve ser uma consulta de pesquisa em inglês."
    ),
    return_direct=True
)

# para verificar se ficou tudo certo
# print('Descrição: ', tool_arxiv.description)
# print('Argumentos: ', tool_arxiv.args)

resposta = tool_arxiv.run({'query' : 'LLM'})
print(resposta)