import json
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

def obter_temperatura_atual(local, unidade='Celsius'):
    if 'são paulo' in local.lower():
        return json.dumps(
            {'local' : 'São Paulo', 'temperatura' : '32', 'unidade' : unidade}
        )
    elif 'porto alegre' in local.lower():
        return json.dumps(
            {'local' : 'Porto Alegre', 'temperatura' : '25', 'unidade' : unidade}
        )
    else:
        return json.dumps(
            {'local' : local, 'temperatura' : 'unknown'}
        )

tools = [
    {
        "type": "function",
        "function": {
            "name": "obter_temperatura_atual",
            "description": "Obtém a temperatura atual em uma dada cidade",
            "parameters": {
                "type": "object",
                "properties": {
                    "local": {
                        "type": "string",
                        "description": "O nome da cidade. Ex: São Paulo",
                    },
                    "unidade": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["local"],
            },
        },
    }
    ]

mensagens = [
    {'role' : 'user', 'content' : 'Qual a temperatura em porto alegre agora?'}
]

resposta = client.chat.completions.create(
    model='gpt-4.1-nano-2025-04-14',
    messages=mensagens,
    tools=tools,
    tool_choice='auto'
)

mensagem = resposta.choices[0].message

tools_call = mensagem.tool_calls[0]

observacao = obter_temperatura_atual(**json.loads(tools_call.function.arguments))

print(observacao)

# não finalizei... no meio comecei a não entender nada... tem que ver o curso de explorando a api da openai