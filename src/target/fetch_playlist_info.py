#!/usr/bin/env python
# coding: utf-8

# ## Fetch data about current playlists, update the covers, and json file 

# ### 0. Import libraries

# In[ ]:


import sys
sys.path.append("../../")

from src.common.config import setup_logger
from src.common.spotify_auth import execute_spotify_auth
from src.common.telegram_alerts import init_telegram_bot, send_telegram_message

from spotipy import Spotify
import requests
import json

from io import BytesIO
from PIL import Image
import logging
import asyncio
import os
import subprocess
from dotenv import load_dotenv


# ### 1. Custom functions

# In[ ]:


def get_playlists_data(sp: Spotify, 
                       cover_images_folder: str,
                       logger: logging.Logger) -> list[dict[str, str]]:
    
    playlists = sp.current_user_playlists()
    playlists_json = []
    
    for playlist in playlists['items']:
        name = playlist['name']
        description = playlist['description']
        url = playlist['external_urls']['spotify']
        cleared_name = "_".join(name.encode('ascii', 'ignore').decode().lower().split())
        playlist_id = playlist['id']
        
        # looking for the playlist based on id to get details
        logger.info(f"Extracting {name} info.")
        playlist_details = sp.playlist(playlist_id) 
        
        logger.info(f"Extracting {name} cover image.")
        # getting and saving playlist cover to a file
        cover_url = playlist_details['images'][0]['url']
        
        response = requests.get(cover_url)
        response.raise_for_status()
        cover_image = Image.open(BytesIO(response.content))
        
        cover_image.save(f"{cover_images_folder}/{cleared_name}.png")
        
        logger.info(f"Extracting {name} details for the playlists json.")
        playlist_json_item = {
            "label": name,
            "description" : description,
            "image": f"{cleared_name}.png",
            "url": url,
            "button_id": cleared_name
        }
        playlists_json.append(playlist_json_item)

    return playlists_json


# ### 2. Environment variables

# In[ ]:


# in dev do ../
# in prod do src/

data_folder_path = "src/"

covers_url = data_folder_path + "data/assets/covers"
json_url = data_folder_path + "data/playlists.json"


# ### 3. Run the code

# In[ ]:


logger = setup_logger("fetch_playlist_info.py")
logger.info('Starting job initialization.')


# In[ ]:


try:

    logger.info('Authorizing spotify access.')
    sp = execute_spotify_auth(logger)
    
    logger.info('Authorizing and initializing telegram bot.')
    bot, chat_id = init_telegram_bot()
    
    logger.info('Retrieving playlists data.')
    playlist_json = get_playlists_data(sp, covers_url, logger)

    logger.info('Overwriting playlists json.')
    
    with open(json_url, "w", encoding="utf-8") as j:
        json.dump(playlist_json, j, indent=4, ensure_ascii=False)
        
    asyncio.run(send_telegram_message(bot, chat_id, "Playlists covers pulled, json updated locally.", logger))
    
    logger.info('Job finished.')
    
except Exception as e:
    logger.error(f'Playlist followers reports pipeline fail: {e}')

