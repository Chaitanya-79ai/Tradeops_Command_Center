import random
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(title="Market Data Service")


@app.get("/health")
def health_check():
    return {
        "service": "market_data",
        "status": "OK"
    }

@app.get("/tick")
def get_tick():
    return {
        "symbol": "NIFTY",
        "price": round(random.uniform(22000, 23000), 2),
        "timestamp": datetime.now().isoformat(),
        "latency_ms": random.randint(5, 25)
    }