#!/usr/bin/env python
# coding: utf-8

# ## Daily updated top 50 global spotify playlist 

# ### 0. Import libraries

# In[ ]:


import pandas as pd

import sys
sys.path.append("../../")

from src.common.spotify_auth import execute_spotify_auth
from src.common.config import setup_logger

from src.common.validation import vaildate_top_df
from src.common.spotify import update_top_playlist_global


# ### 1. Custom functions

# In[2]:


def load_top_50_df(path: str) -> pd.DataFrame:
    
    df = pd.read_csv(path, index_col=0)
    
    return df.loc[ : 49, : ]


# ### 2. Environment variables

# In[ ]:


top_200_csv_path = "src/data/top_200_global.csv"

top_df_columns = ['pos', 'title', 'artist']

top_50_playlist_name = 'DAILY TOP 50'


# ### 3. Run the code

# In[ ]:


logger = setup_logger("top_200_global_daily.py")
logger.info('Starting job initialization.')


# In[ ]:


try:    
    logger.info('Reading the csv with songs.')
    # LOAD TOP 200 SONGS SCRAPED FROM BILLBOARD
    top_100_df = load_top_50_df(top_200_csv_path)

    # DQ
    assert vaildate_top_df(top_100_df, required_count=50, required_columns=top_df_columns) == 'OK', 'QC fail.'

    logger.info('Updating the playlist.')

    # spotify auth
    logger.info('Authorizing spotify access.')
    sp = execute_spotify_auth(logger)
    
    # UPDATING THE PLAYLIST
    top_50_df = update_top_playlist_global(top_100_df, sp, top_50_playlist_name)
except Exception as e:
    logger.error(f'Top 50 global pipeline fail: {e}')
    

logger.info('Job finished.')

