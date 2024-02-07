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

'''# Get YouTube API credentials
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

'''

def get_playlists(username, sp):

    # Get the user's playlists
    response = sp.user_playlists(username)

    playlists = {}

    idx = 0
    for playlist in response['items']:
        idx += 1
        playlists[idx] = [playlist['id'], playlist['name']]
    
    return playlists


def get_playlist_tracks(username, playlist_id, sp):

    # Get the user's playlist
    playlist = sp.user_playlist(username, playlist_id)

    return playlist['tracks']['items']


def main():
    print("Welcome to Spotify->YouTube Playlist Converter!")
    username = input("Please enter your Spotify username: ")

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

    print("Here are your playlists:")
  
    playlists = get_playlists(username, sp)
    for idx in playlists:
        print(f"{idx}. {playlists[idx][1]}, {playlists[idx][0]}")

    playlist_idx = int(input("Please enter the corresponding number of the playlist you would like to transfer: "))
    tracks = get_playlist_tracks(username, playlists[playlist_idx][0], sp)

    i = 0
    for track in tracks:
        i += 1
        print(f"{i}. {track['track']['name']}")


if __name__ == "__main__":
    main()