from spotipy import Spotify
from fuzzywuzzy import fuzz
import pandas as pd

def search_and_match_track(row, sp: Spotify) -> str:
    query = f"{row['title']} {row['artist']}"
    result = sp.search(q = query, type='track', limit = 5)
    
    scored_results = [] # (score, uri, explicit)
    
    if result['tracks']['items']:
        for track in result['tracks']['items']:
            spotify_title = track['name']
            spotify_artists = ", ".join([artist['name'] for artist in track['artists']])
            uri = track['uri']
            explicit = track['explicit']
            
            title_score = fuzz.token_set_ratio(row['title'], spotify_title)
            artist_score = fuzz.token_set_ratio(row['artist'], spotify_artists)
            total_score = (title_score + artist_score) / 2
            
            scored_results.append((total_score, uri, explicit))
            
        scored_results.sort(reverse=True, key=lambda x: (x[0], x[2]))  # sort on score and explicit
        return scored_results[0][1]
    
    return None


def get_songs_ids_from_spotify(top_playlist_df: pd.DataFrame, sp: Spotify) -> pd.DataFrame:
    
    top_playlist_df['uri'] = top_playlist_df.apply(search_and_match_track, axis=1, args = (sp,))
    
    return top_playlist_df


def update_top_playlist_global(top_x_df: pd.DataFrame, sp: Spotify, playlist_name: str) -> pd.DataFrame:
    
    tracks = top_x_df['uri'].to_list()
    tracks1, tracks2 = [], []
    if len(tracks) > 100:
        tracks1, tracks2 = tracks[0 : 100], tracks[100 : 200]
    else :
        tracks1 = tracks
        
    playlists = sp.current_user_playlists()
    top_playlist_id = ""
    
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            top_playlist_id = playlist['id']
            

    sp.playlist_replace_items(top_playlist_id, [])
    
    sp.playlist_add_items(top_playlist_id, tracks1)
    if len(tracks2) > 0:
        sp.playlist_add_items(top_playlist_id, tracks2)
    
    return top_x_df