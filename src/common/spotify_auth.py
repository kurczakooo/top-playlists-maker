import requests
import base64
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
client_id = os.getenv('ID')
client_secret = os.getenv('SECRET')
refresh_token = os.getenv('REFRESH')
access_token = ""

# Przygotuj nagłówki
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Przygotuj body
data = {
    "grant_type": 'refresh_token',
    "refresh_token": refresh_token,
    # "client_id": client_id
}

# Wyślij POST na token endpoint
response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

# Wyświetl odpowiedź
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    try:
        print(f"refresh_token: {token_info['refresh_token']}")
    except Exception as e:
        print('NO REFRESH TOKEN RETURNED')
    access_token = access_token
else:
    print(f"Błąd: {response.status_code}")
    print(response.text)


print(f"ACCESS TOKEN FORM CONGIF BEFORE CONNECTION: {access_token}")
sp = spotipy.Spotify(auth = access_token)
