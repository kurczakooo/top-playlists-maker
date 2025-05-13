#!/usr/bin/env python
# coding: utf-8

# # Daily run script to generate playlists followers reports

# ### 0. Import libraries

# In[3]:


import sys
sys.path.append("../../")

from src.common.spotify_auth import sp
from src.common.config import setup_logger


# ### 1. Custom functions

# In[ ]:





# ### 2. Envinroment variables

# In[ ]:





# ### 3. Run the code

# In[ ]:


logger = setup_logger("followers_reporting.py")
logger.info('Starting job initialization.')

