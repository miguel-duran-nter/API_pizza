from fastapi import APIRouter

app = APIRouter()

orders_list = [{"id": 1, "client_id": 1, "id_pizza": 1}]

@app.get("/orders")
async def list_orders():
    return orders_list