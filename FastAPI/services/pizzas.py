from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import List
from models import schemas
from models.dto import PizzaList, PizzaDetail

async def get_pizza_by_id(db: Session, pizza_id: int):
    with db as session:
        try:
            pizza = session.query(schemas.Pizza).filter(schemas.Pizza.id == pizza_id).first()
            return PizzaDetail.from_orm(pizza)
        except SQLAlchemyError as e:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    

async def get_all_pizzas(db: Session):
    with db as session:
        try:
            pizzas = session.query(schemas.Pizza).all()
            return [PizzaList.from_orm(pizza) for pizza in pizzas]
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))