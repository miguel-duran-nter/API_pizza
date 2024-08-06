from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI
from controllers import pizzas, orders, users, login

load_dotenv(find_dotenv())

app = FastAPI()

app.include_router(users.app)
app.include_router(pizzas.app)
app.include_router(orders.app)
app.include_router(login.app)

@app.get("/")
async def root():
    return {"detail": "Bienvenido a mi APIzzeria"}
    