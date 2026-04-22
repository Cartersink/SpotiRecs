import streamlit as st

st.set_page_config(page_title="Music App", layout="wide")

st.title("🎧 Music Recommendation App")
st.markdown("### Choose a feature")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation function
def go_to(page_name):
    st.session_state.page = page_name

# Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎵 Song Recommender")
    st.write("Find songs similar to your favorites.")
    if st.button("Open", key="rec"):
        go_to("recommender")

with col2:
    st.subheader("🔥 Playlist Generator")
    st.write("Auto-generate a full playlist.")
    if st.button("Open", key="playlist"):
        go_to("playlist")

with col3:
    st.subheader("📊 Explore Data")
    st.write("Analyze song features.")
    if st.button("Open", key="explore"):
        go_to("explore")

if st.session_state.page == "recommender":
    import pages_1  # or call a function if you refactor

elif st.session_state.page == "playlist":
    st.write("Playlist page coming soon")

elif st.session_state.page == "explore":
    st.write("Explore page coming soon")
