from langchain.agents import load_tools

tools = load_tools(['stackexchange'])

tool_stack = tools[0]

# para verificar se ficou tudo certo
# print('Descrição: ', tool_stack.description)
# print('Argumentos: ', tool_stack.args)

resposta = tool_stack.run({'query' : 'langchain agents problem'})
print(resposta)