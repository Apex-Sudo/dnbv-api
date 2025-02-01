import os
from dotenv import load_dotenv
import requests

load_dotenv()

class GuestyClient:
    def __init__(self):
        self.client_id = os.getenv('GUESTY_CLIENT_ID')
        self.client_secret = os.getenv('GUESTY_CLIENT_SECRET')
        self.api_url = os.getenv('GUESTY_API_URL')
        self.token = None

    def authenticate(self):
        auth_url = "https://login.guesty.com/oauth2/token"
        response = requests.post(
            auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )
        if response.ok:
            self.token = response.json()['access_token']
            return True
        return False

    def get_listings(self):
        if not self.token:
            self.authenticate()
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.api_url}/listings", headers=headers)
        return response.json()
