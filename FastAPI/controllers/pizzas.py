from typing import List
from fastapi import APIRouter, HTTPException, status
from models.schemas import Base
from db.client import SessionLocal, engine
from services.pizzas import get_pizza_by_id, get_all_pizzas
from models.dto import PizzaDetail, PizzaList

Base.metadata.create_all(bind=engine)

app = APIRouter(
    prefix="/pizzas",
    tags=["Pizzas"],
)


@app.get("/{pizza_id}", response_model=PizzaDetail)
async def pizza_id(pizza_id: int):
    """
    Displays the details of the pizza with the entered id

    - **pizza_id**: id of the pizza you want to see the details of
    """
    db = SessionLocal()
    try:
        pizza = await get_pizza_by_id(db, pizza_id)
        return pizza

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/", response_model=List[PizzaList])
async def pizza_with_ingredients():
    """
    Displays the details of the pizza with the entered id
    """
    db = SessionLocal()
    try:
        pizzas = await get_all_pizzas(db)
        return pizzas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
