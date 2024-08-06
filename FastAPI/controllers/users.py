from typing import List
from fastapi import APIRouter, HTTPException, status
from services.users import create_user, search_user, read_user
from models.schemas import Base
from models.dto import User
from db.client import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = APIRouter(prefix="/users", tags=["Users"])

"""
endpoint users
"""

@app.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def new_user(user: User):
    """
    It is used to create/register a user
    """
    db = SessionLocal()
    db_user = await create_user(user, db)
    return db_user


@app.get("/{user_id}")
async def user_id(user_id: int):
    """
    Displays the details of the user who has the provided id

    - **user_id**: id of the user you want to see the details of
    """
    db = SessionLocal()
    db_user = await search_user(user_id, db)
    return db_user


@app.get("/")
async def users():
    """
    Display all users
    """
    db = SessionLocal()
    users = await read_user(db)
    return users