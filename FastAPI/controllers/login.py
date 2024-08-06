from fastapi import APIRouter, HTTPException, status, Response
from db.client import SessionLocal
from models import schemas
from services.auth import login
from models.dto import LoginRequest

app = APIRouter(prefix = "/auth", tags = ["Auth"])

@app.post("/login")
async def log_in(request: LoginRequest, response: Response):
    db = SessionLocal()
    log = await login(db, request, response)
    return log
        
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key = "session_profile")
    return {"message": "Logged out successfully"}