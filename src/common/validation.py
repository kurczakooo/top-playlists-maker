import pandas as pd

def vaildate_top_df(top_x_df: pd.DataFrame, required_count: int, required_columns: list[str]) -> str:
    assert top_x_df['pos'].count() == required_count, f'Number of records is not {required_count}.'
    assert all(col in top_x_df.columns for col in required_columns), "Missing required columns."
    assert pd.to_numeric(top_x_df['pos'], errors='raise').notnull().all(), "'pos' has non-numeric values."
    assert top_x_df.notnull().all().all(), "There are missing values!"
    assert top_x_df['pos'].is_monotonic_increasing, "'pos' is not sorted!"
    assert top_x_df['pos'].is_unique, "'pos' is not unique!"
    assert not top_x_df[['pos', 'title', 'artist']].duplicated().any(), "A record is duplicated."
    assert not top_x_df[['title', 'artist']].duplicated().any(), "A song is duplicated."
    
    return 'OK'