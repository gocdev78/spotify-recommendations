"""
This is a boilerplate pipeline 'spotify'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=display_head,
                inputs="spotify_songs",
                outputs=None,
                name="display_input"
            ),
            node(
                func=remove_unnecessary_columns,
                inputs="spotify_songs",
                outputs="spotify_songs_relevant_columns",
                name="remove_unnecessary_columns"
            ),
            node(
                func=create_genre_id,
                inputs="spotify_songs_relevant_columns",
                outputs="spotify_songs_genre_id",
                name="create_genre_id"
            ),
            node(
                func=scale_columns,
                inputs="spotify_songs_genre_id",
                outputs="spotify_songs_scaled",
                name="scale_columns"
            ),
            node(
                func=clip_outliers,
                inputs="spotify_songs_scaled",
                outputs="spotify_songs_clipped",
                name="clip_outliers"
            ),
            node(
                func=display_head,
                inputs="spotify_songs_clipped",
                outputs="spotify_songs_autoencoder_prepared",
                name="display_output"
            ),
        ]
    )

