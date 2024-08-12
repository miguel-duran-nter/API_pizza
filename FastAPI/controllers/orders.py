import base64
from fastapi import APIRouter, HTTPException, Request, status
from typing import List
from db.client import SessionLocal
from models.dto import (
    Order,
    OrderCreate,
    OrderStatusUpdate,
    PaginatedOrders,
    OrderStatus,
)
from services.orders import (
    create_order,
    list_orders,
    get_user_orders,
    change_status,
    get_order_details,
)
from services.users import get_user_by_id
from models import schemas

app = APIRouter(prefix="/orders", tags=["Orders"])


@app.post("/", response_model=Order)
async def post_order(order: OrderCreate, request: Request):
    """
    Create a new pizza order
    """
    try:
        db = SessionLocal()
        if request.cookies.get("session_id"):
            id_user = int(
                base64.b64decode(
                    str(request.cookies.get("session_id")).encode()
                ).decode("utf-8")
            )
            user = await get_user_by_id(db, id_user)
            new_order = await create_order(order, db, user.id, str(user.profile))
            return new_order
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="You must log in"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/", response_model=PaginatedOrders)
async def get_orders(request: Request, page: int = 1, page_size: int = 10):
    """
    List all orders
    """
    try:
        db = SessionLocal()
        id_user = int(
            base64.b64decode(str(request.cookies.get("session_id")).encode()).decode(
                "utf-8"
            )
        )
        user = await get_user_by_id(db, id_user)
        orders = await list_orders(db, user.profile, page, page_size)
        return orders
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/{order_id}", response_model=OrderStatus)
async def update_order_status(
    order_id: int, order_update: OrderStatusUpdate, request: Request
):
    """
    Updates the order status with the entered id

    - **order_id**: the id of the order you want to update the status of
    """
    try:
        db = SessionLocal()
        id_user = int(
            base64.b64decode(str(request.cookies.get("session_id")).encode()).decode(
                "utf-8"
            )
        )
        user = await get_user_by_id(db, id_user)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.profile == "admin":  # type:ignore
            result = await change_status(db, order_update, order_id)
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Denied"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/history", response_model=List[Order])
async def history_orders(request: Request):
    try:
        db = SessionLocal()
        id_user = int(
            base64.b64decode(str(request.cookies.get("session_id")).encode()).decode(
                "utf-8"
            )
        )
        user = await get_user_by_id(db, id_user)
        orders_data = await get_user_orders(db, int(user.id))
        return orders_data  # Los datos se devolverán como una lista de dictados
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/{order_id}")
async def detail_order(order_id: int, request: Request):
    try:
        db = SessionLocal()
        id_user = int(base64.b64decode(str(request.cookies.get("session_id")).encode()).decode("utf-8"))
        user = await get_user_by_id(db, id_user)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.profile == "admin":  # type:ignore
            result = await get_order_details(db, order_id)
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Denied"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    
