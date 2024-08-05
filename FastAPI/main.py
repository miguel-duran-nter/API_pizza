from dotenv import load_dotenv

from fastapi import FastAPI
from controllers import pizzas, orders, users

load_dotenv()

app = FastAPI()

app.include_router(users.app)
app.include_router(pizzas.app)
app.include_router(orders.app)

@app.get("/")
async def root():
    return {"detail": "Bienvenido a mi API Pizzeria"}
    