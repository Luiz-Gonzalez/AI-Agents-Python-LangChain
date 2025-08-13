# Criando uma tool de busca de temperatura
# https://open-meteo.com/en/docs
import requests
import datetime
from langchain.agents import tool
from pydantic import BaseModel, Field

# definir os argumentos de entrada da funcao (argumentos)
class RetornaTempsArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=RetornaTempsArgs)
def retorna_temperatura_atual(latitude: float, longitude: float):
    '''Retorna a temperatura atual para uma dada coordenada'''

    URL = 'https://api.open-meteo.com/v1/forecast'

    params = {
        'latitude' : latitude,
        'longitude' : longitude,
        'hourly' : 'temperature_2m',
        'forecast_days' : 1, 
    }

    resposta = requests.get(URL, params=params)
    if resposta.status_code == 200:
        resultado = resposta.json()
        #pega o horário atual do dispositivo
        hora_agora = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        # pega a lista de horas da resposta da api
        lista_horas = [datetime.datetime.fromisoformat(temp_str) for temp_str in resultado['hourly']['time']]
        # index da lista_horas mais próximo a hora atual
        index_mais_prox = min(range(len(lista_horas)), key=lambda x: abs(lista_horas[x] - hora_agora))
        # pega a temperatura através do indice relativo ao resultado acima que é o horário mais próximo do horário atual
        temp_atual = resultado['hourly']['temperature_2m'][index_mais_prox]
        return temp_atual
    else:
        raise Exception(f'Request para API {URL} falhou: {resposta.status_code}')
    
latitude = -25
longitude = -49

resposta = retorna_temperatura_atual.invoke({'latitude' : latitude, 'longitude' : longitude})

print(resposta)

