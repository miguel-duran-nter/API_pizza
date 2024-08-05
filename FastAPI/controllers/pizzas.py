from fastapi import APIRouter, HTTPException, status
from models.schemas import Base
from db.client import SessionLocal, engine
from services.pizzas import get_pizza_by_id, get_all_pizzas

Base.metadata.create_all(bind=engine)

app = APIRouter(
    prefix="/pizzas",
    tags=["pizzas"],
)


@app.get("/{pizza_id}")
async def pizza_id(pizza_id: int):
    db = SessionLocal()
    try:
        pizza = await get_pizza_by_id(db, pizza_id)
        return pizza

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get("/")
async def obtener_pizzas_con_ingredientes():
    db = SessionLocal()
    try:
        pizzas = await get_all_pizzas(db)
        return pizzas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
