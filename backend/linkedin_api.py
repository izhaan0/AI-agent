import requests
import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"

def get_user_profile(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None