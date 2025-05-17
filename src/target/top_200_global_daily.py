#!/usr/bin/env python
# coding: utf-8

# ## Daily updated top 200 global spotify playlist 

# ### 0. Import libraries

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import sys
sys.path.append("../../")

from src.common.spotify_auth import execute_spotify_auth
from src.common.config import setup_logger
from src.common.chromedriver_config.chromedriver_config import chrome_options, user_agent_string_override_command
from src.common.validation import vaildate_top_df
from src.common.scraping import reject_billboard_cookies, scrape_billboard_global_200, filter_names_artists_pos
from src.common.spotify import update_top_playlist_global, get_songs_ids_from_spotify


# ### 1. Custom functions

# In[ ]:





# ### 2. Environment variables

# In[ ]:


global_200_url = "https://www.billboard.com/charts/billboard-global-200/"

reject_cookies_button_id = 'onetrust-reject-all-handler'
html_class = 'o-chart-results-list-row-container'
pos_class = 'c-label a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet'
song_html_id = 'title-of-a-story'
artist_class = 'a-no-trucate'

top_df_columns = ['pos', 'title', 'artist']
top_200_playlist_name = 'DAILY TOP 200'


# ### 3. Run the code

# In[ ]:


logger = setup_logger("top_200_global_daily.py")
logger.info('Starting job initialization.')

service = Service(ChromeDriverManager().install())  
driver = webdriver.Chrome(service = service, options = chrome_options)
driver.set_page_load_timeout(60)

logger.info('Webdriver setup complete.')


# In[ ]:


# SCRAPING THE TOP 200 GLOABAL FROM BILLBOARD
logger.info('Scraping top 200 global from billboard.')
try:
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent' : user_agent_string_override_command})
    
    reject_billboard_cookies(driver, reject_cookies_button_id, logger)

    driver.get(global_200_url)

    songs = scrape_billboard_global_200(driver, html_class, logger)
except Exception as e:
    
    logger.error(f'Error scraping top 200 global from billboard\n{e}')

assert len(songs) == 200, 'Number of html elements is not 200.'

# TRASFORMING THE DATA TO A DF, DO QC
logger.info('Transforming the data to a DataFrame, doing quality checks.')
top_200_df = filter_names_artists_pos(songs, 
                                      song_html_id, 
                                      artist_class, 
                                      pos_class, 
                                      top_df_columns)

assert vaildate_top_df(top_200_df, required_count=200, required_columns=top_df_columns) == 'OK', 'QC fail.'
    
logger.info('Getting songs from Spotify and updating the playlist.')
try:
    # spotify auth
    logger.info('Authorizing spotify access.')
    sp = execute_spotify_auth(logger)
    
    # GET SONGS FROM SPOTIFY
    top_200_df = get_songs_ids_from_spotify(top_200_df, sp)

    # REFRESH TOP 200 GLOBAL PLAYLIST
    top_200_df = update_top_playlist_global(top_200_df, sp, top_200_playlist_name)
except Exception as e:
    logger.error(f'Matching Spotify songs or updating playlist fail.\n{e}')
    
try:
    logger.info('Saving the DataFrame to a file.')

    top_200_df.to_csv("src/data/top_200_global.csv")

    logger.info('Job finished.')
except Exception as e:
    logger.error(f'Saving new dataframe fail.\n{e}')

