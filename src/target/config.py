import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import logging

def setup_logger(filename: str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # delete handlers if there are any
    if logger.hasHandlers():
        logger.handlers.clear()

    # Format 
    log_format = f"%(asctime)s | %(levelname)s | {filename} | %(message)s\n"
    date_format = "%Y-%m-%d %H:%M:%S"

    # set handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    logger.addHandler(handler)

    return logger

load_dotenv()
id = os.getenv('ID')
secret = os.getenv('SECRET')
uri = os.getenv('URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id, 
                                               client_secret=secret, 
                                               redirect_uri=uri,
                                               scope="user-library-read \
                                                      playlist-modify-public \
                                                      playlist-modify-private \
                                                      playlist-read-private \
                                                      playlist-read-collaborative"))