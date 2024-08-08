from typing import List
from fastapi import APIRouter, HTTPException, status, Request
from services.users import create_user, user_detail, read_user, get_user_by_id, update_user
from models.dto import UserCreate, UserUpdate, UserOrder
from db.client import SessionLocal
import base64

app = APIRouter(prefix="/users", tags=["Users"])


@app.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def new_user(user: UserCreate):
    """
    It is used to create/register a user
    """
    try:
        db = SessionLocal()
        db_user = await create_user(user, db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/me", response_model=UserOrder)
async def user_id(request: Request):
    """
    Displays the details of the user who has the provided id
    """
    try:
        db = SessionLocal()
        user_id = request.cookies.get("session_id")
        db_user = await user_detail(str(user_id), db, request)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/", response_model=List[UserOrder])
async def users(request: Request):
    """
    Display all users
    """
    try:
        db = SessionLocal()
        user_id= request.cookies.get("session_id")
        users = await read_user(db, str(user_id))
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.put("/update", response_model=UserUpdate)
async def update_user_endpoint(user_update: UserUpdate, request: Request):
    """
    Update data who has the provided id
    """
    try:
        db = SessionLocal()
        user_id = base64.b64decode(str(request.cookies.get("session_id")).encode()).decode('utf-8')
        user = await get_user_by_id(db, int(user_id))
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_user = await update_user(db, user, user_update)
        
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    