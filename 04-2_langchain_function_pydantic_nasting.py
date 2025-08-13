from pydantic import BaseModel
from typing import List

class pydPessoa(BaseModel):
    nome: str
    idade: int
    peso: float

class pydAsimovTeam(BaseModel):
    funcionarios: List[pydPessoa]

team = pydAsimovTeam(funcionarios=[pydPessoa(nome='Luiz', idade=41, peso=65), pydPessoa(nome='Luizo', idade=41, peso=65)])

print(team.funcionarios[1].nome)