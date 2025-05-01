import requests
import base64
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def retirive_acces_token():
    load_dotenv()
    client_id = os.getenv('ID')
    client_secret = os.getenv('SECRET')
    refresh_token = os.getenv('REFRESH')

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token,
        # "client_id": client_id
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=body)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        try:
            print(f"refresh_token: {token_info['refresh_token']}")
        except Exception as e:
            print('NO REFRESH TOKEN RETURNED')
        return access_token
    else:
        print(f"Błąd: {response.status_code}")
        print(response.text)



access_token = retirive_acces_token()
sp = spotipy.Spotify(auth = access_token)
