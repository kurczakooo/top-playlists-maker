from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_billboard_global_200(driver: webdriver, 
                                class_name: str,
                                load_time: int = 20) -> list[str]:
    try:
        WebDriverWait(driver, load_time).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        unfiltered_songs = soup.find_all('div', class_ = class_name)
        return unfiltered_songs
    except Exception as e:
        print(f'Scraping Error: {e}')
    finally:
        driver.quit()
        
        
def filter_names_artists_pos(unfiltered_songs: list[str], 
                             song_html_id: str, 
                             artist_class: str, 
                             pos_class: str,
                             df_columns: list[str]) -> pd.DataFrame:
    
    separators = [" Featuring ", " & ", " X ", " feat. ", " featuring ", " with ", ", "]
    pattern = "|".join(map(re.escape, separators))
    
    songs_list = []
    for element in unfiltered_songs:
        pos = int(element.find('span', class_ = pos_class).text.strip())
        title = element.find('h3', id = song_html_id).text.strip()
        artist = element.find('span', class_ = artist_class).text.strip()
        artist = re.split(pattern, artist, maxsplit = 1)[0]
        
        songs_list.append([pos, title, artist])
        
    top_x_df = pd.DataFrame(data = songs_list, columns = df_columns)
    
    return top_x_df