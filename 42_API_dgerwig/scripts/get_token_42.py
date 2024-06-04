import requests
from dotenv import load_dotenv
import os

load_dotenv()

UID = os.getenv("UID")
SECRET = os.getenv("SECRET")

def get_access_token(uid=UID, secret=SECRET):
    response = requests.post("https://api.intra.42.fr/oauth/token", data={
        'grant_type': 'client_credentials',
        'client_id': uid,
        'client_secret': secret
    })
    response.raise_for_status()
    return response.json()['access_token']

if __name__ == "__main__":
    access_token = get_access_token()
    print(f"✨ Access Token: {access_token}")
