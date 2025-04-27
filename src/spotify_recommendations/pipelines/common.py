batch_size = 32
metadata_columns = ['track_id', 'track_name', 'album_name', 'artists']
feature_columns = [
    'popularity',
    'duration_ms',
    'explicit',
    'danceability',
    'energy',
    'key',
    'loudness',
    'mode',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'liveness',
    'valence',
    'tempo',
    'genre_id'
]
latent_space = 32
input_dim = 14
vocab_size = 114
embed_dim = 128
epochs = 30
