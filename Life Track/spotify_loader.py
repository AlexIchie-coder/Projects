import os
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def load_spotify_data(folder_path):
    records = []

    for filename in os.listdir(folder_path):
        if filename.startswith("StreamingHistory_music") and filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                data = json.load(f)
                records.extend(data)

    StreamingMusic = pd.DataFrame(records)
    StreamingMusic['endTime'] = pd.to_datetime(StreamingMusic['endTime'])
    return StreamingMusic




# Example usage:
# spotify_df = load_spotify_data("Spotify Account Data/")
# print(spotify_df.head())


# # Set up Spotify API client
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="your_client_id",
#                                             client_secret="your_client_secret",
#                                             redirect_uri="http://localhost:8888/callback",
#                                             scope=["user-library-read", "playlist-read-private"]))

# def get_track_genre(track_name, artist_name):
#     # Search for the track on Spotify
#     result = sp.search(q=f"track:{track_name} artist:{artist_name}", limit=1)
#     if result['tracks']['items']:
#         track = result['tracks']['items'][0]
#         artist_id = track['artists'][0]['id']
        
#         # Fetch artist details
#         artist = sp.artist(artist_id)
#         genres = artist['genres']
        
#         # Return the genre information, or a default value if no genre is found
#         if genres:
#             return genres[0]  # Return the first genre
#         else:
#             return "Unknown Genre"
#     else:
#         return "Track not found"

# # Assuming spotify_df contains the trackName and artistName columns
# spotify_df['genre'] = spotify_df.apply(lambda row: get_track_genre(row['trackName'], row['artistName']), axis=1)

# # Display updated data with genre
# print(spotify_df[['trackName', 'artistName', 'genre']])





