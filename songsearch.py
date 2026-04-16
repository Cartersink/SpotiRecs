import pandas as pd

df = pd.read_csv("tracks_features.csv")

def find_song_index(song_name, artist_name, df):
    matches = df[
        (df["name"].str.lower() == song_name.lower()) &
        (df["artists"].str.lower() == artist_name.lower())
    ]
    
    if matches.empty:
        return None
    
    return matches.index[0]

name = input("Enter song name: ")
artist_name = input("Enter artist name: ")

print(find_song_index(name, artist_name, df))

