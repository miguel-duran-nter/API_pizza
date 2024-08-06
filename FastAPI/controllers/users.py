from typing import List
from fastapi import APIRouter, HTTPException, status, Request
from services.users import create_user, user_detail, read_user, get_user_by_id, update_user
from models.dto import User, UserUpdate
from db.client import SessionLocal

app = APIRouter(prefix="/users", tags=["Users"])


@app.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def new_user(user: User):
    """
    It is used to create/register a user
    """
    db = SessionLocal()
    db_user = await create_user(user, db)
    return db_user


@app.get("/{user_id}")
async def user_id(user_id: int, request: Request):
    """
    Displays the details of the user who has the provided id

    - **user_id**: id of the user you want to see the details of
    """
    db = SessionLocal()
    db_user = await user_detail(user_id, db, request)
    return db_user


@app.get("/")
async def users(request: Request):
    """
    Display all users
    """
    db = SessionLocal()
    user_profile = request.cookies.get("session_profile")
    if user_profile == 'admin':
        users = await read_user(db)
        return users
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")

@app.put("/update/{user_id}", response_model=UserUpdate)
async def update_user_endpoint(user_id: int, user_update: UserUpdate):
    """
    Update data who has the provided id
    - **user_id**:  id of the user you want to update data
    """
    db = SessionLocal()
    user = await get_user_by_id(db, user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await update_user(db, user, user_update)
    
    return updated_user
