from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

@app.post("/api/v1/availability")
async def check_availability():
    return {
        "available": True,
        "listings": [{
            "id": "mock_villa_1",
            "price": 450,
            "checkIn": (datetime.now() + timedelta(days=1)).isoformat(),
            "checkOut": (datetime.now() + timedelta(days=8)).isoformat()
        }]
    }
