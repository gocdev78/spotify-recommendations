import torch
import torch.nn as nn


class SongAutoencoder(nn.Module):
    def __init__(self, input_dim, genre_vocab_size, genre_emb_dim, latent_dim):
        super(SongAutoencoder, self).__init__()
        self.return_latent = False
        self.genre_embedding = nn.Embedding(genre_vocab_size, genre_emb_dim)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim + genre_emb_dim, latent_dim * 4),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(latent_dim * 4, latent_dim * 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(latent_dim * 2, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, latent_dim * 2),
            nn.ReLU(),
            nn.Linear(latent_dim * 2, latent_dim * 4),
            nn.ReLU(),
            nn.Linear(latent_dim * 4, input_dim + 1),
        )

    def forward(self, x):
        genre_id = x[:, -1].to(torch.int32)
        x = x[:, :-1]
        genre_emb = self.genre_embedding(genre_id)
        x = torch.cat([x, genre_emb], dim=1)
        latent = self.encoder(x)
        if self.return_latent:
            return latent
        reconstructed = self.decoder(latent)
        return reconstructed
