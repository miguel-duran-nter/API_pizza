from dotenv import load_dotenv

from fastapi import FastAPI
from endpoints import pizzas, basic_auth_users, orders, user

load_dotenv()

app = FastAPI()

app.include_router(basic_auth_users.app)
# app.include_router(users.app)
app.include_router(user.app)
app.include_router(pizzas.app)
app.include_router(orders.app)

@app.get("/")
async def root():
    return {"detail": "Bienvenido a mi API"}