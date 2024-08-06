from fastapi import APIRouter, HTTPException, Request, status
from typing import List
from db.client import SessionLocal
from models.dto import Order, OrderCreate, OrderStatusUpdate
from services.orders import create_order, list_orders

from models import schemas
from sqlalchemy.orm import joinedload

app = APIRouter(prefix="/orders", tags=["Orders"])


@app.post("/", response_model=Order)
async def post_order(order: OrderCreate, request: Request):
    """
    Create a new pizza order
    """
    db = SessionLocal()
    profile = request.cookies.get("session_profile")
    if profile == "admin":
        new_order = await create_order(order, db)
        return new_order
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@app.get("/", response_model=List[Order])
async def get_orders(request: Request):
    """
    List all orders
    """
    db = SessionLocal()
    profile = request.cookies.get("session_profile")
    if profile == "admin":
        orders = await list_orders(db)
        return orders
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@app.put("/{order_id}", response_model=Order)
def update_order_status(order_id: int, order_update: OrderStatusUpdate, request: Request):
    """
    Updates the order status with the entered id

    - **order_id**: the id of the order you want to update the status of
    """
    db = SessionLocal()
    user_profile = request.cookies.get("session_profile")
    if user_profile == 'admin':
        db_order = (
            db.query(schemas.Order).filter(schemas.Order.order_id == order_id).first()
        )

        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")

        db_order.status = order_update.status  # type:ignore
        db.commit()
        db.refresh(db_order)

        db_order_with_details = (
            db.query(schemas.Order)
            .options(
                joinedload(schemas.Order.user),
                joinedload(schemas.Order.details).joinedload(schemas.OrderDetail.pizza),
            )
            .filter(schemas.Order.order_id == db_order.order_id)
            .first()
        )

        return db_order_with_details
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")