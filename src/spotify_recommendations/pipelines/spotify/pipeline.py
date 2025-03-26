"""
This is a boilerplate pipeline 'spotify'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import display_head, remove_unnecessary_columns


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
                func=display_head,
                inputs="spotify_songs_relevant_columns",
                outputs=None,
                name="display_after_column_removal"
            ),
        ]
    )

