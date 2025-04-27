from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import create_dataloader, generate_embeddings


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_dataloader,
                inputs="spotify_songs_autoencoder_prepared",
                outputs="dataloader",
                name="create_dataloader"
            ),
            node(
                func=generate_embeddings,
                inputs="dataloader",
                outputs="songs_embeddings",
                name="generate_embeddings"
            ),
        ]
    )