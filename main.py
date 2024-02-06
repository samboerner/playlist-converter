import spotipy
import spotipy.util as util

'''from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build'''
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Get Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("REDIRECT_URI")

username = ''

try:
    token = util.prompt_for_user_token(username, 'playlist-read-private', client_id=SPOTIFY_CLIENT_ID,
                                        client_secret=SPOTIFY_CLIENT_SECRET,
                                        redirect_uri=SPOTIFY_REDIRECT_URI)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, 'playlist-read-private', client_id=SPOTIFY_CLIENT_ID,
                                       client_secret=SPOTIFY_CLIENT_SECRET,
                                       redirect_uri=SPOTIFY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

'''# Get YouTube API credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

'''

def get_playlists(username):

    playlists = []
    offset = 0
    limit = 50
    # Get the user's playlists
    while True:

        response = sp.user_playlists(username, offset=offset, limit=limit)
        if not response['items']:
            break

        playlists.extend(response['items'])
        offset += limit

    playlist_dict = {}

    for playlist in playlists:
        playlist_dict[playlist['name']] = playlist['id']
    
    return playlist_dict

idx = 0
playlists = get_playlists(username)
for name, playlist_id in playlists.items():
    idx += 1
    print(f"{idx}. {name}, {playlist_id}")

def get_playlist_tracks(username, playlist_id):

    # Get the user's playlist
    playlist = sp.user_playlist(username, playlist_id)

    return playlist['tracks']['items']