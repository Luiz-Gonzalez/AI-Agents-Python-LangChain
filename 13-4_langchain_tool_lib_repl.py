from langchain_experimental.tools.python.tool import PythonAstREPLTool

tool_repl = PythonAstREPLTool()

# para verificar se ficou tudo certo
# print('Descrição: ', tool_repl.description)
# print('Argumentos: ', tool_repl.args)

resposta = tool_repl.run({'query' : 'print("oi")'})
print(resposta)