from fastapi import APIRouter, HTTPException, status, Response
from db.client import SessionLocal
from services.auth import login, do_logout
from models.dto import LoginRequest

app = APIRouter(prefix = "/auth", tags = ["Auth"])

@app.post("/login")
async def log_in(request: LoginRequest, response: Response):
    try:
        db = SessionLocal()
        log = await login(db, request, response)
        return log
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
@app.post("/logout")
async def logout(response: Response):
    try:
        return await do_logout(response)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # return {"message": "Logged out successfully"}