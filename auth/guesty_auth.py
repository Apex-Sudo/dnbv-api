import os
import requests
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GUESTY_CLIENT_ID")
CLIENT_SECRET = os.getenv("GUESTY_CLIENT_SECRET")
AUTH_HEADER = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

class GuestyAPI:
    def authenticate(self):
        try:
            response = requests.post(
                "https://login.guesty.com/oauth2/token",
                headers={
                    "Authorization": f"Basic {AUTH_HEADER}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"grant_type": "client_credentials"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Auth Failed: {e}")
            return None

if __name__ == "__main__":
    api = GuestyAPI()
    print(api.authenticate())
