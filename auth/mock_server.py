from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from guesty_client import GuestyClient
import os

app = FastAPI()
client = GuestyClient()

app.mount("/webflow", StaticFiles(directory="../webflow"), name="webflow")

@app.post("/api/v1/availability")
async def check_availability(dates: dict = Body(...)):
    try:
        if os.getenv('USE_MOCK') == 'true':
            return {
                "available": True,
                "listings": [{
                    "id": "mock_villa_1",
                    "price": 450,
                    "checkIn": dates.get('checkIn'),
                    "checkOut": dates.get('checkOut')
                }]
            }
        else:
            listings = client.get_listings()
            return {"available": True, "listings": listings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
