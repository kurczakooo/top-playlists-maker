import requests
import base64
from dotenv import load_dotenv
import os
import spotipy
from logging import Logger


def execute_spotify_auth(logger: Logger) -> spotipy.Spotify:
    load_dotenv()
    client_id = os.getenv('ID')
    client_secret = os.getenv('SECRET')
    refresh_token = os.getenv('REFRESH')
    access_token = ""

    # headers
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # body
    data = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token,
        # "client_id": client_id
    }

    # sending post request to ger access token
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    # analize the response
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        try:
            logger.info(f"refresh_token: {token_info['refresh_token']}")
        except Exception as e:
            logger.error('NO REFRESH TOKEN RETURNED')
        access_token = access_token
    else:
        logger.error(f"Błąd: {response.status_code}")
        logger.error(response.text)

    return spotipy.Spotify(auth = access_token)
