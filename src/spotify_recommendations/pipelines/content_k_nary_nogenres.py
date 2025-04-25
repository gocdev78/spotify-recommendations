import ast
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from typing import Tuple, List

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Parsujemy listę artystów (string) → listę Pythonową
    df['artists_list'] = df['artists'].apply(ast.literal_eval)
    return df

def preprocess_features(df: pd.DataFrame) -> np.ndarray:
    # Wybieramy tylko cechy numeryczne opisane w data.csv
    feats = [
        'valence','acousticness','danceability','energy',
        'instrumentalness','liveness','loudness',
        'speechiness','tempo','popularity'
    ]
    mat = df[feats].values
    mat_scaled = MinMaxScaler().fit_transform(mat)
    return mat_scaled

def train_content_k_nary(data_path: str) -> Tuple[pd.DataFrame, np.ndarray, NearestNeighbors]:
    df = load_data(data_path)
    feature_matrix = preprocess_features(df)
    # ustawiamy metrykę cosine → NN będzie liczył 1 - cosine_similarity
    nn = NearestNeighbors(metric='cosine', algorithm='brute')
    nn.fit(feature_matrix)
    return df, feature_matrix, nn

def recommend(
    df: pd.DataFrame,
    feature_matrix: np.ndarray,
    nn: NearestNeighbors,
    artist_query: str,
    k: int = 10
) -> List[str]:
    # 1) Wybieramy indeksy utworów danego artysty
    mask = df['artists_list']\
        .apply(lambda lst: any(artist_query.lower() in art.lower() for art in lst))
    artist_idxs = df[mask].index.tolist()
    if not artist_idxs:
        return []

    # 2) Pobieramy k+|artist_idxs| sąsiadów dla każdego utworu artysty
    n_neigh = k + len(artist_idxs)
    distances, indices = nn.kneighbors(
        feature_matrix[artist_idxs],
        n_neighbors=n_neigh,
        return_distance=True
    )
    # cosine distance = 1 - cosine similarity
    sim_scores = 1 - distances

    # 3) Agregujemy wyniki: dla każdego kandydata liczymy średnią z podobieństw
    score_sum = {}
    count = {}
    for row_idxs, row_sims in zip(indices, sim_scores):
        for idx, sim in zip(row_idxs, row_sims):
            if idx in artist_idxs:
                continue
            score_sum[idx] = score_sum.get(idx, 0.0) + sim
            count[idx] = count.get(idx, 0) + 1

    # 4) Obliczamy średnią i wybieramy top-k
    avg_scores = {idx: score_sum[idx] / count[idx] for idx in score_sum}
    top_idxs = sorted(avg_scores, key=lambda idx: avg_scores[idx], reverse=True)[:k]

    return df.loc[top_idxs, 'name'].tolist()
