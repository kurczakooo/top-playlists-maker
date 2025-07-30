#!/usr/bin/env python
# coding: utf-8

# #### **OBJECTIVES**
# 
# The goal is to ingest traffic and behaviour data from GA4, which is integrated with the LINK-TREE for the playlists using BigQuery, and create custom reports in a form of pdfs similar to the followers reports. The idea came from the fact that GA4 standalone is not intuitive for reporting purposes, can't be as flexible as custom reports, and I don't want to be dependent on the platform. That's why all the event data from GA4 is transfered to BigQuery, and with the use of the official API it can be easily extracted and used.
# 
# ##### **REPORT PLAN / VISUALIZATION**
# The most important things that need to be included in the report are:
# - DAILY GRANURALITY:
#   - Overall traffic, (bar chart or line chart with last 7 days)
#   - Traffic sources distribution, (a pie chart)
#   - Playlist link button clicks distribution, (horizontal bar chart)
#   - Social link button clicks distribution, (vertival bar chart)
#   - Singular Descriptive values like:
#     - sum(playlist buttons clicks) / traffic -> CTR for playlist buttons
#     - sum(social buttons clicks) / traffic -> CTR for social buttons
#     - avg(timestamp of clicking a button - timestamp of entering the page)
# 
# The rest is TDB.
# A mock report visualization made in canva is attached in the repo locally.
# 
# 
# ##### **EVENTS CUSTOMIZED FOR REPORTING PURPOSES:**
# - ##### Playlist link button click event:
#     - event_name : 'button_click'
#     - event_category : 'playlist'
#     - event_label : playlist mapping id e.g. top_200_global
# - ##### Social link button click event:
#     - **TBD**
# 
# ##### **DATA NEEDED FOR THE REPORTS:**
# - Daily playlist button click events,
# - Daily social button click events,
# - Daily amount of users on the website
# - Source of the user traffic, e.g. Organic, Tiktok, Instagram
# - User level data: user time on the website, user id for users comparison, timestamp of clicking a button, timestamp of enterign the website, timestamp of leaving the website
#   

# In[ ]:


from google.cloud import bigquery
import db_dtypes

import pandas as pd
import numpy as np
import json

from dotenv import load_dotenv
import os


# In[ ]:


date = "29/07/2025"

date_transformed = "".join([x for x in date.split("/")[::-1]])

date_transformed


# In[ ]:


load_dotenv()

big_query_credentials = os.getenv("BIG_QUERY_CREDENTIALS")
big_query_credentials = big_query_credentials.replace("\\\n", "\\n")


# In[ ]:


json_key = json.loads(big_query_credentials)


# In[ ]:


# client = bigquery.Client.from_service_account_json(key)
client = bigquery.Client.from_service_account_info(json_key)


# In[ ]:


query = f"""
    SELECT * 
    FROM `spotify-playlists-manager.analytics_491860361.events_{date_transformed}` 
    LIMIT 1000
"""


# In[ ]:


query_job = client.query(query)


# In[ ]:


results = query_job.to_dataframe()


# In[ ]:


results.info()


# In[ ]:


results.head(5)


# In[ ]:


results_filtered_button_clicks = results.loc[results['event_name'] == 'button_click']


# In[ ]:


results_filtered_button_clicks = results_filtered_button_clicks[['event_date', 
                                                                 'event_timestamp',
                                                                 'event_name',
                                                                 'event_params']]


# In[ ]:


results_filtered_button_clicks


# In[ ]:


results_filtered_button_clicks.count()
# old len 12


# In[ ]:


results_filtered_button_clicks['event_params'].value_counts()


# In[ ]:


def get_params(row):
    
    param_list = row['event_params']
    
    for element in param_list:
            if element['key'] == 'event_label':
                    row['event_label'] = element['value']['string_value']
    
    return row


# In[ ]:


fesults_with_params_extracted = results_filtered_button_clicks.apply(lambda row : get_params(row), axis=1)


# In[ ]:


fesults_with_params_extracted


# In[ ]:


clicks_count = fesults_with_params_extracted['event_label'].value_counts()


# In[ ]:


clicks_count_df = pd.DataFrame(clicks_count).reset_index()
clicks_count_df


# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# In[ ]:


sns.set_style("white", {"grid.color": "#2A2A2A"})

fig, ax = plt.subplots(figsize=(5, 3))

sns.barplot(x=clicks_count_df['count'], 
            y=clicks_count_df['event_label'],
            hue=clicks_count_df['event_label'],
            palette = "plasma",
            legend=False)

ax.grid(color='#808080', axis='x', linestyle='-', linewidth=0.5)
ax.set_ylabel("")
ax.set_xlabel("")
ax.tick_params(axis='y', labelleft=False)
ax.set_title(f"{date} Playlists buttons clicks on the link tree", 
             loc='center',
             pad=10)

