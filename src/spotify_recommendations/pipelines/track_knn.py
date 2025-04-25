from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from typing import List, Tuple
from functools import lru_cache

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

_spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials()
)

@lru_cache(maxsize=1024)
def _get_track_genres(track_id: str) -> List[str]:
    """
    Zwraca unikalną listę gatunków dla podanego track_id.
    """
    try:
        tr = _spotify.track(track_id)
        genres = []
        for art in tr['artists']:
            a = _spotify.artist(art['id'])
            genres.extend(a.get('genres', []))
        return list({g.lower() for g in genres})
    except Exception:
        return []

def train_track_knn(data_path: str) -> Tuple[pd.DataFrame, np.ndarray, NearestNeighbors]:
    """
    Wczytuje data.csv, buduje i skaluje feature matrix, trenuje KNN.
    Zwraca: (df, X, nn_model).
    """
    df = pd.read_csv(data_path)

    # Jeśli brakuje kolumny 'year', wyciągamy z 'release_date'
    if 'year' not in df.columns:
        df['year'] = (
            pd.to_datetime(df['release_date'], errors='coerce')
              .dt.year.fillna(0)
              .astype(int)
        )

    features = [
        'valence','acousticness','danceability','energy',
        'instrumentalness','liveness','loudness',
        'speechiness','tempo','popularity',
        'year','duration_ms','explicit','mode','key'
    ]
    X = df[features].values
    X = MinMaxScaler().fit_transform(X)

    nn = NearestNeighbors(metric='cosine', algorithm='brute')
    nn.fit(X)

    return df, X, nn

def recommend_from_track(
    df: pd.DataFrame,
    X: np.ndarray,
    nn: NearestNeighbors,
    seed_artist: str,
    seed_track: str,
    genre: str = None,
    k: int = 10,
    genre_weight: float = 0.3
) -> List[Tuple[str, str]]:
    """
    Zwraca k rekomendacji jako [(track_name, track_id), …],  
    uwzględniając dodanie genre_weight do similarity matchujących gatunek.
    """
    # 1) znajdź seed
    mask_seed = (
        df['name'].str.contains(seed_track, case=False, na=False) &
        df['artists'].str.contains(seed_artist, case=False, na=False)
    )
    if not mask_seed.any():
        return []
    idx0 = df[mask_seed].index[0]
    seed_id = df.at[idx0, 'id']

    # 2) pobierz k+1 sąsiadów
    distances, indices = nn.kneighbors(
        X[idx0].reshape(1, -1),
        n_neighbors=k+1,
        return_distance=True
    )
    base_sims = 1 - distances[0]

    # 3) debug: jakie gatunki ma seed?
    seed_genres = _get_track_genres(seed_id)
    print(f"[DEBUG] seed_genres for '{seed_track}' by '{seed_artist}': {seed_genres}")

    # 4) zbieraj rekomendacje z uwzględnieniem dodania stałej genre_weight
    scored: List[Tuple[int, float]] = []
    for sim, idx in zip(base_sims, indices[0]):
        if idx == idx0:
            continue
        tid = df.at[idx, 'id']

        # sprawdź match gatunku
        cand_genres = _get_track_genres(tid)
        match = False
        if genre:
            match = (genre.lower() in cand_genres)
        else:
            match = bool(set(seed_genres) & set(cand_genres))

        # debug: pokaż parę (tytuł, sim, match)
        print(f"[DEBUG] candidate '{df.at[idx,'name']}' sims={sim:.3f} genres={cand_genres} match={match}")

        # 5)
        score = sim + (genre_weight if match else 0.0)
        scored.append((idx, score))

    # 6)
    scored.sort(key=lambda x: x[1], reverse=True)
    result = [(df.at[i, 'name'], df.at[i, 'id']) for i,_ in scored[:k]]
    return result

__all__ = ['train_track_knn', 'recommend_from_track']
