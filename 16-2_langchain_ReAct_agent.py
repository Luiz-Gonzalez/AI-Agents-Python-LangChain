from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_experimental.tools import PythonAstREPLTool
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()

# prompt = hub.pull('hwchase17/react') # esta padrao do hub do langchain está com problemas devido a ter um [] no tool_names: [{tool_names}]. LLM está se perdendo.


prompt = PromptTemplate.from_template(
'''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {tool_names}
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''
)

print(prompt.template) # prompt pronto estilo ReAct

tools = [PythonAstREPLTool()]

chat = ChatOpenAI()

agent = create_react_agent(chat, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
resposta = agent_executor.invoke({'input' : 'Qual é o décimo valor da sequência fibonacci?'})