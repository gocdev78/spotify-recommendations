import pandas as pd
import streamlit as st
import json
from typing import Iterable
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_genres_mapping() -> dict:
    with open('data/models/autoencoder/genre_id.json', 'r') as f:
        genre_ids = json.load(f)

    return genre_ids


genre_ids = get_genres_mapping()


def get_artists_by_genre(genre_id: str) -> Iterable:
    df = pd.read_csv("data/spotify_songs_autoencoder_prepared.csv")
    artists = df[df["genre_id"] == genre_id]['artists'].tolist()
    artists_flat = []
    for artist in artists:
        split = artist.split(";")
        artists_flat.extend(split)

    artists_unique = set(artists_flat)
    return artists_unique


def get_songs_by_artist(artist_name: str) -> Iterable:
    df = pd.read_csv("data/spotify_songs_autoencoder_prepared.csv")
    return set(df[df["artists"].astype(str).str.contains(artist_name)]['track_name'].tolist())


def get_recommendation(song_name: str, artist_name: str) -> pd.DataFrame:
    df = pd.read_parquet("data/song_embeddings.parquet")
    song_features = df[df["artist"].astype(str).str.contains(artist_name) & df["song"].str.contains(song_name)]['latent_vectors'].values[0]

    similarities = cosine_similarity(
        song_features.reshape(1, -1),
        np.vstack(df["latent_vectors"].values)
    )[0]

    top_n = 10
    top_indices = np.argsort(similarities)[::-1][:top_n]

    return df.iloc[top_indices].copy()[["song", "artist", "album"]]


st.set_page_config(page_title="Spotify Recommendations", layout="centered")

st.title("Spotify Recommendations")

st.write("Ta aplikacja będzie w przyszłości generować rekomendacje muzyczne na podstawie sztucznej Inteligencji")

genre = st.selectbox("Wybierz gatunek:", genre_ids.keys())
artist = st.selectbox("Wybierz ulubionego artyste: ", get_artists_by_genre(genre_ids[genre]))
song = st.selectbox("Wybierz piosenkę: ", get_songs_by_artist(artist))

if st.button("Generuj rekomendacje"):
    st.dataframe(get_recommendation(song, artist))
