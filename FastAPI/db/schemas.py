from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    username: str
    email: str
    address: str

class IngredienteBase(BaseModel):
    id: int
    nombre: str

class PizzaBase(BaseModel):
    name: str
    image: str
    ingredientes: list[IngredienteBase] = []

class Pizza(PizzaBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class Ingrediente(IngredienteBase):
    pass