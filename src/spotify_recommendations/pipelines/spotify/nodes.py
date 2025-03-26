"""
This is a boilerplate pipeline 'spotify'
generated using Kedro 0.19.12
"""
import pandas as pd


def display_head(df: pd.DataFrame) -> None:
    print(df.head())


def remove_unnecessary_columns(songs: pd.DataFrame) -> pd.DataFrame:
    unnecessary_columns = [
        "Unnamed: 0",
        "track_id",
        "artists",
        "album_name",
        "track_name"
    ]

    return songs.drop(columns=unnecessary_columns)
