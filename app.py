import streamlit as st
import sys, os

# 1) musi być pierwsze
st.set_page_config(page_title="Spotify Recommendations", layout="centered")

# 2) dołączamy src do PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from spotify_recommendations.pipelines.track_knn import (
    train_track_knn,
    recommend_from_track
)

@st.cache_data(show_spinner=False)
def load_model():
    return train_track_knn("data/data.csv")

def main():
    st.title("🎵 Spotify Recommendations")

    df, X, nn = load_model()

    # wejścia użytkownika
    artist = st.text_input("Ulubiony artysta:")
    track  = st.text_input("Ulubiona piosenka (tytuł):")
    genre  = st.text_input("Gatunek (opcjonalnie):")
    k      = st.slider("Ile rekomendacji?", 1, 20, 10)
    genre_weight = st.slider(
        "Waga gatunku (dodawana stała)", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.1
    )

    if st.button("Generuj rekomendacje"):
        recs = recommend_from_track(
            df, X, nn,
            seed_artist=artist,
            seed_track=track,
            genre=genre or None,
            k=k,
            genre_weight=genre_weight
        )
        if not recs:
            st.warning("Brak rekomendacji – sprawdź dane wejściowe.")
        else:
            st.success("Twoje rekomendacje:")
            for name, tid in recs:
                url = f"https://open.spotify.com/track/{tid}"
                st.markdown(f"- [{name}]({url})")

if __name__ == "__main__":
    main()
