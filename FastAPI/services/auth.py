from fastapi import Response, HTTPException, status, Request
from sqlalchemy.orm import Session
from models import schemas
from models.dto import LoginRequest

async def login(db: Session, request: LoginRequest, response: Response):
    with db as session:
        user_db = session.query(schemas.User).filter(schemas.User.username == str(request.username)).first()
        if user_db:
            user = session.query(schemas.User).filter(schemas.User.password == str(request.password)).first()
            if user:
                session_value = user.profile
                response.set_cookie(key="session_profile", value=str(session_value))
                return {"message": "Logged in successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Password incorrect")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
async def get_profile(db: Session, request: Request):
    with db as session:
        user_profile = session.query(schemas.User.profile).filter(schemas.User.id == request.cookies.get("session_profile"))
        return user_profile