from pydantic import BaseModel

class pydPessoa(BaseModel):
    nome: str
    idade: int
    peso: float

luiz = pydPessoa(nome='Luiz', idade=41, peso=65)

print(luiz)
print(luiz.nome)