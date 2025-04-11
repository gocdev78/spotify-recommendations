from torch.utils.data import Dataset
import torch
from .common import metadata_columns, feature_columns
import numpy as np


class SongDataset(Dataset):
    def __init__(self, df, include_metadata_columns=False):
        self.df = df
        self.include_metadata_columns = include_metadata_columns

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        features_numpy = row[feature_columns].to_numpy().astype(float)
        features_torch = torch.from_numpy(features_numpy).to(torch.float32)

        if not self.include_metadata_columns:
            return features_torch
        
        metadata = row[metadata_columns].to_numpy()
        return metadata, features_torch


class CollateBatch:
    def __init__(self, batch):
        metadata, features = zip(*batch)
        self.features = torch.stack(features, dim=0)
        self.metadata = np.asarray(list(metadata), dtype=str)

    @staticmethod
    def build(batch):
        return CollateBatch(batch)
