from fastapi import APIRouter, HTTPException, status
from db.client import SessionLocal
from models import schemas
from models.dto import LoginRequest

app = APIRouter(prefix = "/auth", tags = ["Auth"])

@app.post("/login")
async def login(request: LoginRequest):
    db = SessionLocal()
    with db as session:
        user_db = session.query(schemas.User).filter(schemas.User.username == request.username).first()
        if user_db:
            user = session.query(schemas.User).filter(schemas.User.password == request.password).first()
            if user:
                return user
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Password incorrect")
        else:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found, username or password incorrect")