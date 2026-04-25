import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Music App", layout="wide")

# -----------------------
# SPOTIFY STYLE THEME
# -----------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }

    h1, h2, h3 {
        color: #1DB954;
        font-weight: 700;
    }

    .stButton>button {
        background-color: #1DB954;
        color: black;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #1ed760;
        transform: scale(1.05);
    }

    .stTextInput>div>div>input {
        background-color: #282828;
        color: white;
        border-radius: 10px;
    }

    .stSelectbox>div>div {
        background-color: #282828;
        color: white;
        border-radius: 10px;
    }

    .stRadio label {
        color: white;
    }

    .card {
        background-color: #181818;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: 0.3s;
    }

    .card:hover {
        background-color: #282828;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# STATE (navigation)
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page

# -----------------------
# DATA + MODEL (cached)
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("tracks_features_clean.csv")

df = load_data()

@st.cache_resource
def build_model(df):
    features = [
        "danceability","energy","key","loudness","mode",
        "speechiness","acousticness","instrumentalness",
        "liveness","valence","tempo"
    ]

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    knn = NearestNeighbors(n_neighbors=10, metric="cosine")
    knn.fit(X_scaled)

    return knn, X_scaled

knn, X_scaled = build_model(df)

def recommend_songs(index):
    query_vector = X_scaled[index].reshape(1, -1)
    distances, indices = knn.kneighbors(query_vector)
    recommended_indices = indices[0][1:]
    return df.iloc[recommended_indices][["name", "artists"]]

# -----------------------
# HOME PAGE
# -----------------------
def show_home():
    st.title("🎧 Spotify Recs")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎵 Song Recommender")
        st.write("Find similar songs instantly.")
        if st.button("Open Recommender"):
            go_to("recommender")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎤 Artist Finder")
        st.write("Discover an artist")
        if st.button("Open Artist Finder"):
            go_to("artist")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📀 Playlist Generator")
        st.write("Build a full playlist")
        if st.button("Open Playlist"):
            go_to("playlist")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# RECOMMENDER PAGE
# -----------------------
def show_recommender():
    st.title("🎵 Song Recommender")
    st.markdown("---")

    if st.button("⬅ Back to Home"):
        go_to("home")

    query = st.text_input("Search songs or artists")

    if query:
        matches = df[
            df["name"].str.lower().str.contains(query.lower(), na=False) |
            df["artists"].str.lower().str.contains(query.lower(), na=False)
        ].copy()

        matches["display_name"] = matches["name"] + " - " + matches["artists"]
        matches = matches.drop_duplicates(subset=["display_name"]).head(50)

        if not matches.empty:
            song_options = {
                row["display_name"]: idx
                for idx, row in matches.iterrows()
            }

            selected_song = st.selectbox("Choose a song", list(song_options.keys()))
            selected_index = song_options[selected_song]

            if st.button("🎵 Recommend Songs"):
                recommendations = recommend_songs(selected_index)

                st.subheader("Recommended Songs")

                for _, row in recommendations.iterrows():
                    st.markdown(f"""
                    <div style="background-color:#181818;padding:12px;border-radius:10px;margin-bottom:8px">
                    <b>{row['name']}</b><br>
                    <span style="color:#b3b3b3">{row['artists']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# -----------------------
# ARTIST PAGE
# -----------------------
def show_artist():
    st.title("🎤 Artist Finder")
    st.markdown("---")

    if st.button("⬅ Back to Home"):
        go_to("home")

    query = st.text_input("Search songs or artists")

    if query:
        matches = df[
            df["name"].str.lower().str.contains(query.lower(), na=False) |
            df["artists"].str.lower().str.contains(query.lower(), na=False)
        ].copy()

        matches["display_name"] = matches["name"] + " - " + matches["artists"]
        matches = matches.drop_duplicates(subset=["display_name"]).head(50)

        if not matches.empty:
            song_options = {
                row["display_name"]: idx
                for idx, row in matches.iterrows()
            }

            selected_song = st.selectbox("Choose a song", list(song_options.keys()))
            selected_index = song_options[selected_song]

            if st.button("Find Artist"):
                artistFound = False
                i = 50

                while not artistFound:
                    features = [
                        "danceability","energy","key","loudness","mode",
                        "speechiness","acousticness","instrumentalness",
                        "liveness","valence","tempo"
                    ]

                    X = df[features]
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)

                    knn = NearestNeighbors(n_neighbors=i, metric="cosine")
                    knn.fit(X_scaled)

                    query_vector = X_scaled[selected_index].reshape(1, -1)
                    distances, indices = knn.kneighbors(query_vector)

                    recs = df.iloc[indices[0][1:]]
                    artist_counts = recs["artists"].value_counts()
                    duplicate_artists = artist_counts[artist_counts > 1]

                    if duplicate_artists.empty:
                        i += 10
                    else:
                        artist = duplicate_artists.index[0]
                        artistFound = True

                st.subheader("Recommended Artist")
                st.markdown(f"""
                <div style="background-color:#181818;padding:20px;border-radius:10px">
                🎤 <b>{artist}</b>
                </div>
                """, unsafe_allow_html=True)

# -----------------------
# PLAYLIST PAGE
# -----------------------
def show_playlist():
    st.title("📀 Playlist Maker")
    st.markdown("---")

    if st.button("⬅ Back to Home"):
        go_to("home")

    query = st.text_input("Search songs or artists")

    order = st.radio(
        "Energy Order",
        ["Ascending (chill → hype)", "Descending (hype → chill)"]
    )

    if query:
        matches = df[
            df["name"].str.lower().str.contains(query.lower(), na=False) |
            df["artists"].str.lower().str.contains(query.lower(), na=False)
        ].copy()

        matches["display_name"] = matches["name"] + " - " + matches["artists"]
        matches = matches.drop_duplicates(subset=["display_name"]).head(50)

        if not matches.empty:
            song_options = {
                row["display_name"]: idx
                for idx, row in matches.iterrows()
            }

            selected_song = st.selectbox("Choose a song", list(song_options.keys()))
            selected_index = song_options[selected_song]

        if st.button("🎶 Generate Playlist"):
            query_vector = X_scaled[selected_index].reshape(1, -1)

            distances, indices = knn.kneighbors(query_vector, n_neighbors=100)
            recs = df.iloc[indices[0][1:]]

            playlist = recs.iloc[::5].copy()

            ascending = "Ascending" in order
            playlist = playlist.sort_values(by="energy", ascending=ascending)

            st.subheader("Your Playlist")

            for i, row in enumerate(playlist.iterrows(), 1):
                song = row[1]
                st.markdown(f"""
                <div style="background-color:#181818;padding:12px;border-radius:10px;margin-bottom:8px">
                <b>{i}. {song['name']}</b><br>
                <span style="color:#b3b3b3">{song['artists']}</span>
                </div>
                """, unsafe_allow_html=True)

# -----------------------
# ROUTER
# -----------------------
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "recommender":
    show_recommender()
elif st.session_state.page == "artist":
    show_artist()
elif st.session_state.page == "playlist":
    show_playlist()


