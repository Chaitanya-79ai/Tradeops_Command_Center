from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Risk Service")

MAX_ORDER_QTY = 500
MAX_ORDER_VALUE = 1000000

class Order(BaseModel):
    symbol: str
    side: str
    quantity: int
    price: float

@app.get("/health")
def health_check():
    return {
        "service": "risk_service",
        "status": "OK"
    }

@app.post("/check-order")
def check_order(order: Order):
    order_value = order.quantity * order.price

    if order.quantity > MAX_ORDER_QTY:
        return {
            "status": "REJECTED",
            "reason": "Order quantity exceeds limit"
        }

    if order_value > MAX_ORDER_VALUE:
        return {
            "status": "REJECTED",
            "reason": "Order value exceeds limit"
        }

    return {
        "status": "APPROVED",
        "reason": "Order passed risk checks"
    }