from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.agent import AgentFinish
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from dotenv import load_dotenv

load_dotenv()

tool_kit = FileManagementToolkit(
    root_dir='arquivos',
    selected_tools=['write_file', 'read_file', 'file_search', 'list_directory']
)

tools = tool_kit.get_tools()

# for tool in tools:
#     print('Nome: ', tool.name)
#     print('Descrição: ', tool.description)
#     print('Argumentos: ', tool.args)
#     print()

tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

prompt = ChatPromptTemplate.from_messages([
    ('system', 'você é um assistente amigável chamado Isaac capaz de gerenciar arquivos'),
    ('user', '{input}')
])

chat = ChatOpenAI()

def roteamento(resultado):
    if isinstance(resultado, AgentFinish):
        return resultado.return_values['output']
    else:
        return tool_run[resultado.tool].run(resultado.tool_input)

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | roteamento

resultado = chain.invoke({'input' : 'o que tem escrito dentro do aruivo karla.txt?'})
print(resultado)