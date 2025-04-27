import pandas as pd
import torch
from ..model import SongAutoencoder
from ..data import SongDataset, CollateBatch
from ..common import *
from torch.utils.data import DataLoader


def create_dataloader(df: pd.DataFrame):
    dataset = SongDataset(df, True)
    return DataLoader(dataset, batch_size=32, collate_fn=CollateBatch.build)


def generate_embeddings(dataloader: DataLoader) -> pd.DataFrame:
    preds = {
        "latent_vectors": [],
        "song": [],
        "album": [],
        "id": [],
        "artist": [],
    }

    autoencoder_eval = SongAutoencoder(input_dim, vocab_size, embed_dim, latent_space)
    autoencoder_eval.load_state_dict(torch.load("data/models/autoencoder/v1.pth", weights_only=True))
    autoencoder_eval.eval()
    autoencoder_eval.return_latent = True

    with torch.no_grad():
        for collate_batch in dataloader:
            latent_vector = autoencoder_eval(collate_batch.features)
            metadata = collate_batch.metadata
            preds["latent_vectors"].extend(latent_vector.numpy())
            preds["id"].extend(metadata[:, 0])
            preds["song"].extend(metadata[:, 1])
            preds["album"].extend(metadata[:, 2])
            preds["artist"].extend(metadata[:, 3])

    return pd.DataFrame.from_dict(preds)
