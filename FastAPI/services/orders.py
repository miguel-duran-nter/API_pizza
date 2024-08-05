from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import schemas
from models.dto import OrderCreate


async def create_order(order: OrderCreate, db: Session):
    with db as session:
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
                    status_code=404, detail=f"Pizza with ID {detail.pizza_id} not found"
                )

            unit_price = pizza.price

            total += detail.quantity * unit_price

            order_details.append(
                schemas.OrderDetail(
                    pizza_id=detail.pizza_id,
                    quantity=detail.quantity,
                    unit_price=unit_price,
                )
            )

        db_order = schemas.Order(
            user_id=order.user_id,
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
                joinedload(schemas.Order.details).joinedload(schemas.OrderDetail.pizza),
            )
            .filter(schemas.Order.order_id == db_order.order_id)
            .first()
        )

        return db_order_with_details


async def list_orders(db: Session):
    with db as session:
        return session.query(schemas.Order).order_by(schemas.Order.order_date.desc()).all()
