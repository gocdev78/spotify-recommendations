import streamlit as st

st.set_page_config(page_title="Spotify Recommendations", layout="centered")

st.title("Spotify Recommendations")

st.write("Ta aplikacja będzie w przyszłości generować rekomendacje muzyczne na podstawie sztucznej Inteligencji")

artist = st.text_input("Wpisz ulubionego artystę:")
genre = st.selectbox("Wybierz gatunek:", ["Pop", "Rock", "Hip-hop", "Jazz", "Elektronika"])

if st.button("Generuj rekomendacje"):
    st.success("Wkrótce dostępne! (Tu będą rekomendacje AI)")
