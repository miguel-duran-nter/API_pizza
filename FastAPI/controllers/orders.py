from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from db.client import SessionLocal
from models import schemas
from models.dto import OrderCreate, Order

app = APIRouter(prefix = "/orders", tags = ["orders"])

@app.post("/", response_model=Order)
def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = schemas.Order(
        user_id=order.user,
        order_date=order.order_date,
        total=order.total,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for detail in order.details:
        db_order_detail = schemas.OrderDetail(
            order_id=db_order.order_id,
            pizza_id=detail.pizza,
            quantity=detail.quantity,
            unit_price=detail.unit_price
        )
        db.add(db_order_detail)
    
    db.commit()
    db.refresh(db_order)

    return db_order

@app.get("/", response_model=List[Order])
def get_orders():
    db = SessionLocal()
    orders = db.query(schemas.Order).order_by(schemas.Order.order_date.desc()).all()
    return orders