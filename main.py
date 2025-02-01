from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Setup
REQUEST_LIMIT = 480
request_counter = 0
last_reset = time.time()

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    global request_counter, last_reset

    if time.time() - last_reset > 60:
        request_counter = 0
        last_reset = time.time()

    if request_counter >= REQUEST_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )

    request_counter += 1
    return await call_next(request)

class GuestyAPI:
    def __init__(self):
        self.base_url = os.getenv("GUESTY_API_BASE_URL")
        self.client_id = os.getenv("GUESTY_CLIENT_ID")
        self.client_secret = os.getenv("GUESTY_CLIENT_SECRET")
        self.token = None
        self.token_expires = 0

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.token}"}

    def authenticate(self):
        if time.time() < self.token_expires:
            return True

        auth_url = f"{self.base_url}/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, data=data)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.token_expires = time.time() + response.json()["expires_in"] - 60
            return True
        return False

guesty = GuestyAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DNBV API</title>
    </head>
    <body>
        <h1>Welcome to the DNBV Instant Booking Site</h1>
    </body>
    </html>
    """

@app.get("/api/test")
async def test_connection():
    if guesty.authenticate():
        return {"status": "success", "message": "Connected to Guesty API"}
    raise HTTPException(status_code=401, detail="Failed to authenticate with Guesty")

@app.get("/api/v1/availability")
async def get_availability(check_in: str, check_out: str):
    if not guesty.authenticate():
        raise HTTPException(status_code=401)

    response = requests.get(
        f"{guesty.base_url}/v1/listings/availability",
        headers=guesty.get_auth_header(),
        params={
            "checkIn": check_in,
            "checkOut": check_out,
            "include": "pricing"
        }
    )
    return response.json()
