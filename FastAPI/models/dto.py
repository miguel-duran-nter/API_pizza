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
    password: str

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "name": "Item Example",
                "description": "This is an example item.",
                "price": 19.99,
                "tax": 1.50
            }
        }

class UserOrder(BaseModel):
    name: str
    email: str
    phone: str
    address: str

    class Config:
        from_attributes = True
        schema_extra = {}

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Ingredient(BaseModel):
    name: str

    class Config:
        from_attributes = True

class PizzaDTO(BaseModel):
    name: str
    price: float

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
    pizza_id: int
    quantity: int

    class Config:
        from_attributes = True

class OrderDetail(OrderDetailBase):
    pizza: PizzaDTO

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    # user_id: int
    order_date: datetime
    total: float
    status: str

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    order_date: datetime
    status: str
    details: List[OrderDetailBase]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

class Order(OrderBase):
    order_id: int
    details: List[OrderDetail]
    user: UserOrder

    class Config:
        from_attributes = True
