import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))


def get_artist_genre(artist_name):
    result = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)

    if result['artists']['items']:
        genres = result['artists']['items'][0]['genres']
        return genres if genres else ["Unknown"]
    return ["Unknown"]
