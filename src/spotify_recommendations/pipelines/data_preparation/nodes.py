"""
This is a boilerplate pipeline 'spotify'
generated using Kedro 0.19.12
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import numpy as np


def display_head(df: pd.DataFrame) -> pd.DataFrame:
    print(df.head())
    return df


def remove_unnecessary_columns(songs: pd.DataFrame) -> pd.DataFrame:
    unnecessary_columns = [
        "Unnamed: 0",
        "track_id",
        "artists",
        "album_name",
        "track_name"
    ]

    return songs.drop(columns=unnecessary_columns)


def create_genre_id(df: pd.DataFrame) -> pd.DataFrame:
    label_encoder = LabelEncoder()
    df["genre_id"] = label_encoder.fit_transform(df["track_genre"].copy())
    return df


def scale_columns(df: pd.DataFrame) -> pd.DataFrame:
    scale_features = [
        "popularity",
        "duration_ms",
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    standard_scaler = StandardScaler()
    df[scale_features] = standard_scaler.fit_transform(df[scale_features].copy())
    return df


def clip_outliers(df: pd.DataFrame) -> pd.DataFrame:
    def clip(df, col):
        lower, upper = np.percentile(df[col], [1, 99])
        df[col] = np.clip(df[col].copy(), lower, upper)
        return df

    clipped = clip(df, "loudness")
    clipped = clip(clipped, "loudness")

    if clipped["time_signature"].std() < 0.5:
        return df.drop(columns=["time_signature"])

    return clipped
