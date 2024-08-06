from fastapi import APIRouter, HTTPException, Request, status, Query, Path
from typing import List
from db.client import SessionLocal
from models.dto import Order, OrderCreate, OrderStatusUpdate
from services.orders import create_order, list_orders, get_user_orders, change_status

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
async def update_order_status(
    order_id: int, order_update: OrderStatusUpdate, request: Request
):
    """
    Updates the order status with the entered id

    - **order_id**: the id of the order you want to update the status of
    """
    db = SessionLocal()
    user_profile = request.cookies.get("session_profile")
    if user_profile == "admin":
        result = await change_status(db, order_update, order_id)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )


@app.get("/history/{user_id}", response_model=List[Order])
async def history_orders(user_id: int):
    try:
        db = SessionLocal()
        orders_data = await get_user_orders(db, user_id)
        return orders_data  # Los datos se devolverán como una lista de dictados
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )