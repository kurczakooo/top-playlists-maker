import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

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