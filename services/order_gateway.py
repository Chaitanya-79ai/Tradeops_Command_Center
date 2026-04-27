import random
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Order Gateway Service")
RISK_SERVICE_URL = "http://127.0.0.1:8002/check-order"

class Order(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float


@app.get("/health")
def health_check():
    return {
        "service": "order_gateway",
        "status": "OK"
    }

@app.post("/order")
def place_order(order: Order):
    risk_response = requests.post(
        RISK_SERVICE_URL,
        json=order.model_dump()
    )

    risk_result = risk_response.json()

    if risk_result["status"] == "REJECTED":
        return {
            "status": "REJECTED",
            "reason": risk_result["reason"]
        }

    order_id = f"ORD{random.randint(10000, 99999)}"

    return {
        "status": "ACCEPTED",
        "order_id": order_id,
        "symbol": order.symbol,
        "side": order.side,
        "quantity": order.quantity,
        "price": order.price
    }