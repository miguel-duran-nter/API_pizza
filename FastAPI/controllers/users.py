from typing import List
from fastapi import APIRouter, HTTPException, status
from services.users import create_user, search_user, read_user
from models.schemas import Base
from models.dto import User
from db.client import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = APIRouter(prefix="/users", tags=["users"])

@app.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def new_user(user: User):
    db = SessionLocal()
    db_user = await create_user(user, db)
    return db_user


@app.get("/{user_id}")
async def user_id(user_id: int):
    db = SessionLocal()
    db_user = await search_user(user_id, db)
    return db_user


@app.get("/")
async def users():
    db = SessionLocal()
    users = await read_user(db)
    return users