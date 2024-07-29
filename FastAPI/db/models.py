from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .client import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    name = Column(String(100), index = True)
    username = Column(String(100), index = True)
    email = Column(String(120), unique = True, index = True)
    address = Column(String(255), nullable = False)

class Pizza(Base):
    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255))
    name = Column(String(100))

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)

class PizzaIngredient(Base):
    __tablename__ = "pizza_ingredients"
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    pizza = relationship("Pizza")
    ingredient = relationship("Ingredient")
