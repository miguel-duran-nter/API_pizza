# from typing import List
from sqlalchemy import Column, Float, Integer, String, ForeignKey, DECIMAL, DateTime, Table
from sqlalchemy.orm import relationship
from db.client import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    name = Column(String(100), index = True)
    username = Column(String(100), index = True)
    phone = Column(String(20), unique = True, index = True)
    email = Column(String(120), unique = True, index = True)
    address = Column(String(255), nullable = False)
    profile = Column(String(50), nullable = False, default = "cliente")
    password = Column(String, nullable = False)

    orders = relationship("Order", back_populates="user")

pizza_ingredients = Table(
    'pizza_ingredients', Base.metadata,
    Column('pizza_id', Integer, ForeignKey('pizzas.id'), primary_key = True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key = True)
)

class Pizza(Base):
    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Float)

    ingredients = relationship("Ingredient", secondary=pizza_ingredients, back_populates="pizzas")
    details = relationship("OrderDetail", back_populates="pizza")

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pizzas = relationship("Pizza", secondary=pizza_ingredients, back_populates="ingredients")

class Order(Base):
    __tablename__ = 'orders'

    
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    order_date = Column(DateTime, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), nullable=False)

    user = relationship("User", back_populates="orders")
    details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = 'order_details'

    detail_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    pizza_id = Column(Integer, ForeignKey('pizzas.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="details")
    pizza = relationship("Pizza", back_populates="details")