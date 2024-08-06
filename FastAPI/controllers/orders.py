from fastapi import APIRouter, HTTPException
from typing import List
from db.client import SessionLocal
from models.dto import Order, OrderCreate, OrderStatusUpdate
from services.orders import create_order, list_orders

from models import schemas
from sqlalchemy.orm import joinedload

app = APIRouter(prefix = "/orders", tags = ["Orders"])

@app.post("/", response_model=Order)
async def post_order(order: OrderCreate):
    """
    Create a new pizza order
    """
    db = SessionLocal()
    new_order = await create_order(order, db)
    return new_order

@app.get("/", response_model=List[Order])
async def get_orders():
    """
    List all orders
    """
    db = SessionLocal()
    orders = await list_orders(db)
    return orders

@app.put("/{order_id}", response_model=Order)
def update_order_status(order_id: int, order_update: OrderStatusUpdate):
    """
    Updates the order status with the entered id

    - **order_id**: the id of the order you want to update the status of
    """
    db = SessionLocal()
    # Busca la orden en la base de datos
    db_order = db.query(schemas.Order).filter(schemas.Order.order_id == order_id).first()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Actualiza el estado de la orden
    db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)

    # Recupera la orden actualizada con los detalles y el usuario
    db_order_with_details = db.query(schemas.Order).options(
        joinedload(schemas.Order.user),
        joinedload(schemas.Order.details).joinedload(schemas.OrderDetail.pizza)
    ).filter(schemas.Order.order_id == db_order.order_id).first()
    
    return db_order_with_details