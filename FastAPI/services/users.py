from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import schemas
from models.dto import User, UserOrder, UserUpdate


async def create_user(user: User, db: Session):
    db_user = schemas.User(**user.dict())
    try:

        with db as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def user_detail(user_id: int, db: Session, request: Request):
    try:
        with db as session:
            db_user = (
                session.query(schemas.User).filter(schemas.User.id == user_id).first()
            )
            user_dto = UserOrder(
                name=db_user.name,
                email=db_user.email,
                username=db_user.username,
                phone=db_user.phone,
                address=db_user.address,
                profile=db_user.profile,
            )
            return user_dto

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def read_user(db: Session):
    try:
        with db as session:
            db_user = session.query(schemas.User).all()
            users_dto = []
            for user in db_user:
                user_dto = UserOrder(
                    name=user.name,
                    email=user.email,
                    phone=user.phone,
                    address=user.address,
                )
                users_dto.append(user_dto)
            return users_dto

    except SQLAlchemyError as e:
        error_msg = str(e.__cause__) or str(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)


async def get_user_by_id(db: Session, user_id: int):
    with db as session:
        return session.query(schemas.User).filter(schemas.User.id == user_id).first()

async def update_user(db: Session, user: User, user_update: UserUpdate):
    # Asegurarse de que la instancia esté asociada con la sesión actual
    user = db.merge(user)

    if user_update.email:
        user.email = user_update.email
    if user_update.name:
        user.name = user_update.name
    if user_update.phone:
        user.phone = user_update.phone
    if user_update.address:
        user.address = user_update.address

    db.commit()
    db.refresh(user)
    return user