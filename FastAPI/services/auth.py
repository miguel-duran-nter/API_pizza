from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import schemas
from models.dto import LoginRequest
import base64

async def login(db: Session, request: LoginRequest, response: Response):
    with db as session:
        try:
            user_db = session.query(schemas.User).filter(schemas.User.username == str(request.username)).first()
            if user_db:
                password_base64 = base64.b64encode(request.password.encode()).decode()
                user = session.query(schemas.User).filter(schemas.User.password == password_base64).first()
                if user:
                    session_id = base64.b64encode(str(user.id).encode()).decode()
                    response.set_cookie(key="session_id", value=str(session_id))
                    return {"message": "Logged in successfully"}
                else:
                    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Password incorrect")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
async def do_logout(response: Response):
    response.delete_cookie(key = "session_id")
    return {"message": "Logged out successfully"}