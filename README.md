#  Spotify Recommendations – Placeholder UI

Prototyp aplikacji rekomendującej muzykę oparty na Streamlit.  
Ta wersja zawiera interfejs użytkownika i placeholdery zamiast działania AI.

##  Instalacja

1. Sklonuj repo:
git clone https://github.com/huchlatymon/spotify-recommendations.git 
cd spotify-recommendations

2. Aktywuj środowisko wirtualne i zainstaluj zależności:
python -m venv .venv .venv\Scripts\activate pip install -r requirements.txt

## Uruchamianie aplikacji
streamlit run app.py lub jeśli masz `run.sh`: 

./run.sh

## Placeholder

Po kliknięciu przycisku pojawia się komunikat: **"Wkrótce dostępne!"**

# Update Tymon 2025-04-11
## Modelowanie danych
### Autoencoder - https://medium.com/@syed_hasan/autoencoders-theory-pytorch-implementation-a2e72f6f7cb7
### Pipeline danych
- `src/spotify_recommendations/pipelines/data_preparation` pipeline przygotowujący dane (skalowanie, usuwanie outlierów itp) `kedro run --pipeline=data_preparation`
- `src/spotify_recommendations/pipelines/autoencoder_training` pipeline trenujący model, zapisuje wagi modelu `kedro run --pipeline=autoencoder_training`
- `src/spotify_recommendations/pipelines/generate_embeddings` pipeline, który generuje embeddingi dla naszego datasetu i zapisuje je do późniejszego użycia `kedro run --pipeline=generate_embeddings`
Pipeliny'y trzeba wykonać w danej koljeności żeby odtworzyć model lokalnie
### Apka
Uruchomienie: `docker-compose up --build`

Flow:
- pobieramy gatunek od użytkownika (żeby przefiltorwać całkiem spory dataframe)
- pobieramy arystę (znowu filtrujemy)
- pobieramy nazwę piosenki
- dla danej piosenki generujemy top 10 rekomendacji 
  - szukamy piosenki w datasecie z embeddingami
  - liczymy podobieństwo cosinusowe między wyszukaną piosenką a całym datasetem
  - zwracamy top 10 najpodobniejszych piosenek

