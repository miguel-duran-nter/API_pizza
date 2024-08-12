from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import schemas
from models.dto import OrderCreate, OrderStatusUpdate


async def create_order(order: OrderCreate, db: Session, user_id: int, profile: str):
    if profile == "admin":
        with db as session:
            try:
                total = 0
                order_details = []

                for detail in order.details:
                    pizza = (
                        session.query(schemas.Pizza)
                        .filter(schemas.Pizza.id == detail.pizza_id)
                        .first()
                    )
                    if not pizza:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pizza with ID {detail.pizza_id} not found",
                        )

                    unit_price = pizza.price
                    total += detail.quantity * unit_price

                    if order.status == "dine-in":
                        discount = total * 0.40
                        total = total - discount

                    order_details.append(
                        schemas.OrderDetail(
                            pizza_id=detail.pizza_id,
                            quantity=detail.quantity,
                            unit_price=unit_price,
                        )
                    )

                db_order = schemas.Order(
                    user_id=user_id,
                    order_date=order.order_date,
                    total=total,
                    status=order.status,
                )
                session.add(db_order)
                session.commit()
                session.refresh(db_order)

                for detail in order_details:
                    detail.order_id = db_order.order_id
                    session.add(detail)

                session.commit()

                db_order_with_details = (
                    session.query(schemas.Order)
                    .options(
                        joinedload(schemas.Order.user),
                        joinedload(schemas.Order.details).joinedload(
                            schemas.OrderDetail.pizza
                        ),
                    )
                    .filter(schemas.Order.order_id == db_order.order_id)
                    .first()
                )

                return db_order_with_details
            except SQLAlchemyError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                )


async def list_orders(db: Session, profile: str, page: int, page_size: int):
    with db as session:
        try:
            if profile == "admin":
                offset = (page - 1) * page_size

                # Obtener el total de órdenes
                total_orders = session.query(schemas.Order).count()

                orders = (
                    session.query(schemas.Order)
                    .options(
                        joinedload(schemas.Order.user),
                        joinedload(schemas.Order.details).joinedload(
                            schemas.OrderDetail.pizza
                        ),
                    )
                    .offset(offset)
                    .limit(page_size)
                    .all()
                )

                return {
                    "total": total_orders,
                    "page": page,
                    "page_size": page_size,
                    "orders": orders,
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
                )

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def change_status(db: Session, order_update: OrderStatusUpdate, order_id: int):
    with db as session:
        try:
            db_order = (
                session.query(schemas.Order)
                .filter(schemas.Order.order_id == order_id)
                .first()
            )

            if not db_order:
                raise HTTPException(status_code=404, detail="Order not found")

            db_order.status = order_update.status  # type:ignore
            session.commit()
            session.refresh(db_order)

            db_order_with_details = (
                session.query(schemas.Order)
                .options(
                    joinedload(schemas.Order.user),
                    joinedload(schemas.Order.details).joinedload(
                        schemas.OrderDetail.pizza
                    ),
                )
                .filter(schemas.Order.order_id == db_order.order_id)
                .first()
            )

            return db_order_with_details
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def get_user_orders(db: Session, user_id: int):
    try:
        orders = db.query(schemas.Order).filter(schemas.Order.user_id == user_id).all()
        return orders
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
async def get_order_details(db: Session, order_id: int):
    with db as session:
        try:
            order = session.query(schemas.Order).filter(schemas.Order.order_id == order_id).first()
            if order is None:
                raise HTTPException(status_code=404, detail="Order not found")
            return order
    
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))