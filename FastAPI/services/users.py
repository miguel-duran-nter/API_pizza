from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import schemas
from models.dto import UserCreate, UserUpdate, User
import base64


async def create_user(user: UserCreate, db: Session):
    password_base64 = base64.b64encode(user.password.encode()).decode()
    db_user = schemas.User(**user.dict())
    db_user.password = password_base64
    try:
        with db as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def user_detail(user_id: str, db: Session, request: Request):
    try:
        id_user = int(base64.b64decode(user_id.encode()).decode("utf-8"))
        user = await get_user_by_id(db, id_user)
        with db as session:
            db_user = (
                session.query(schemas.User)
                .filter(schemas.User.id == user.id)
                .first()
            )
            return db_user

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def read_user(db: Session, user_id: str):
    try:
        # profile_decode = base64.b64decode(profile.encode()).decode("utf-8")
        id_user = int(base64.b64decode(user_id.encode()).decode("utf-8"))
        user = await get_user_by_id(db, id_user)
        if user.profile == "admin":
            with db as session:
                db_user = session.query(schemas.User).all()
                return db_user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
            )

    except SQLAlchemyError as e:
        error_msg = str(e.__cause__) or str(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)


async def get_user_by_id(db: Session, user_id: int):
    with db as session:
        return session.query(schemas.User).filter(schemas.User.id == user_id).first()


async def update_user(db: Session, user: User, user_update: UserUpdate):
    with db as session:
        try:
            # Asegurarse de que la instancia esté asociada con la sesión actual
            user = session.merge(user)

            if user_update.email:
                user.email = user_update.email
            if user_update.name:
                user.name = user_update.name
            if user_update.phone:
                user.phone = user_update.phone
            if user_update.address:
                user.address = user_update.address
            if user_update.username:
                user.username = user_update.username

            session.commit()
            session.refresh(user)
            return user

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
