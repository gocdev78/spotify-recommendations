import pandas as pd
from .data import SongDataset, CollateBatch
from .common import *
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import torch.nn as nn
from torch import optim
from .model import SongAutoencoder
import torch


def create_dataloaders(df: pd.DataFrame) -> tuple[DataLoader, DataLoader]:
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    train_dataset = SongDataset(train)
    test_dataset = SongDataset(test, False)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)
    return train_dataloader, test_dataloader


def train_fn(train_dataloader: DataLoader, test_dataloader: DataLoader) -> None:
    autoencoder = SongAutoencoder(input_dim, vocab_size, embed_dim, latent_space)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(autoencoder.parameters(), lr=0.001, weight_decay=1e-5)
    best_val_loss = float("inf")
    best_model_path = "data/models/autoencoder/v1.pth"

    print("Starting training...")
    for epoch in range(epochs):
        autoencoder.train()
        epoch_loss = 0.0

        for data in train_dataloader:
            optimizer.zero_grad()
            reconstructed = autoencoder(data)
            loss = criterion(reconstructed, data)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        avg_train_loss = epoch_loss / len(train_dataloader)

        autoencoder.eval()
        val_loss = 0.0
        with torch.no_grad():
            for data in test_dataloader:
                reconstructed = autoencoder(data)
                loss = criterion(reconstructed, data)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(test_dataloader)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(autoencoder.state_dict(), best_model_path)
            print(f"✅ Model saved at epoch {epoch + 1} with val_loss: {avg_val_loss:.6f}")

        print(f"Epoch {epoch + 1}/{epochs}, Train Loss: {avg_train_loss:.6f}, Val Loss: {avg_val_loss:.6f}")

    print("Training complete! Best model saved as", best_model_path)