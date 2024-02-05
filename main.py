import spotipy
import spotipy.util as util
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Get Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("REDIRECT_URI")

# Get YouTube API credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

print(SPOTIFY_REDIRECT_URI)

def get_playlists(username):
    # Get Spotify API token
    token = util.prompt_for_user_token(username,'playlist-read-private',
                                        client_id=SPOTIFY_CLIENT_ID,
                                        client_secret=SPOTIFY_CLIENT_SECRET,
                                        redirect_uri='http://localhost:8080/')
    # Create Spotify API instance
    sp = spotipy.Spotify(auth=token)

    # Get the user's playlists
    playlists = sp.user_playlists(username)

    playlist_dict = {}

    for playlist in playlists['items']:
        playlist_dict[playlist['name']] = playlist['id']

playlists = get_playlists('sboerner3')

for idx, name, playlist_id in playlists.items():
    print(f"{idx}. {name}: {playlist_id}")


def get_playlist_tracks(username, playlist_id):
    # Get Spotify API token
    token = util.prompt_for_user_token(username,'playlist-read-private',
                                        client_id=SPOTIFY_CLIENT_ID,
                                        client_secret=SPOTIFY_CLIENT_SECRET,
                                        redirect_uri=SPOTIFY_REDIRECT_URI)
    
    # Create a Spotify API instance
    sp = spotipy.Spotify(auth=token)

    # Get the user's playlist
    playlist = sp.user_playlist(username, playlist_id)

    return playlist['tracks']['items']