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
                func=create_dataloaders,
                inputs="spotify_songs_autoencoder_prepared",
                outputs=["spotify_songs_autoencoder_train", "spotify_songs_autoencoder_test"],
                name="create_dataloaders"
            ),
            node(
                func=train_fn,
                inputs=["spotify_songs_autoencoder_train", "spotify_songs_autoencoder_test"],
                outputs=None,
                name="train"
            ),
        ]
    )

