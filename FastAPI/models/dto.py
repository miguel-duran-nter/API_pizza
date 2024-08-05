from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    address: str
    profile: str

    class Config:
        from_attributes = True

class UserOrder(BaseModel):
    name: str
    phone: str
    address: str

    class Config:
        from_attributes = True

class Ingredient(BaseModel):
    name: str

    class Config:
        from_attributes = True

class PizzaDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PizzaList(BaseModel):
    image: str
    name: str
    price: float

    class Config:
        from_attributes = True

class PizzaDetail(BaseModel):
    name: str
    price: float
    ingredients: List[Ingredient]

    class Config:
        from_attributes = True

class OrderDetailBase(BaseModel):
    pizza: PizzaList
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetail(OrderDetailBase):
    detail_id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user: UserOrder
    order_date: datetime
    total: float
    status: str

    class Config:
        from_attributes = True

class OrderCreate(OrderBase):
    details: List[OrderDetailCreate]

class Order(OrderBase):
    order_id: int
    details: List[OrderDetail]

    class Config:
        from_attributes = True