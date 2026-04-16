import streamlit as st
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.preprocessing import StandardScaler

st.title("Song Recommender")
FILE_ID = "1VZd1_sPBgCAXhAlKDnHr7tVZ8W56w1E5"
df = pd.read_csv("https://drive.google.com/uc?export=download&id="+FILE_ID)
st.write(list(df.columns))
query = st.text_input("Search songs, artists...")

def recommend_songs(index):
    songs = df
    features = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
    ]

    X = songs[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X) 
    
    knn = NearestNeighbors(
    n_neighbors=6,   # 5 recommendations + itself
    metric="cosine"
    )

    knn.fit(X_scaled)
    
    query_vector = X_scaled[index].reshape(1, -1)
    distances, indices = knn.kneighbors(query_vector)
    
    recommended_indices = indices[0][0:]

    recommendations = df.iloc[recommended_indices][
        ["name", "artists"]
    ]
    
    return recommendations


if query:
    matches = df[
        df["name"].str.contains(query, case=False, na=False) |
        df["artists"].str.contains(query, case=False, na=False)
    ].copy()

    matches["display_name"] = (
        matches["name"] + " - " + matches["artists"]
    )

    matches = matches.drop_duplicates(subset=["display_name"])

    if not matches.empty:
        song_options = {
            row["display_name"]: idx
            for idx, row in matches.iterrows()
        }

        selected_song = st.selectbox(
            "Choose a song",
            list(song_options.keys())
        )

        selected_index = song_options[selected_song]

        st.write("Selected index:", selected_index)
        
        if st.button("🎵 Recommend Songs"):
            recommendations = recommend_songs(selected_index)

            st.subheader("Recommended Songs")
            st.dataframe(recommendations)       



