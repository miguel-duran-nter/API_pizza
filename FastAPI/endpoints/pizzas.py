from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import models, schemas
from db.client import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pizzas/{pizza_id}", response_model=schemas.Pizza)
def get_pizza_by_id(pizza_id: int, db: Session = Depends(get_db)):
    pizza = db.query(models.Pizza).filter(models.Pizza.id == pizza_id).first()
    if pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return pizza


@app.get("/pizzas/", response_model=List[schemas.Pizza])
def read_user(db: Session = Depends(get_db)):
    pizzas = db.query(models.Pizza).all()
    return pizzas
