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

    tracks = []

    # Get the user's playlist
    response = sp.user_playlist_tracks(username, playlist_id)

    while response:
        for item in response['items']:
            track = item['track']
            info = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']]
            }
            tracks.append(info)
        
        if response['next']:
            response = sp.next(response)
        else:
            response = None

    return tracks


def create_yt_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body{
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    return response['id']


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

    confirm = False
    while not confirm:
        print("Here are your playlists:")
        playlists = get_playlists(username, sp)
        for idx in playlists:
            print(f"{idx}. {playlists[idx][1]}, {playlists[idx][0]}")

        playlist_idx = int(input("Please enter the number that corresponds with the playlist you would like to transfer: "))
        ans = input(f"Are you sure you want to transfer playlist '{playlists[playlist_idx][1]}'? (Confirm y/n)")
        
        if ans == 'y':
            confirm = True
    
    tracks = get_playlist_tracks(username, playlists[playlist_idx][0], sp)

    i = 0
    for track in tracks:
        i += 1
        print(f"{i}. {track['name']} - {', '.join(track['artists'])}")


if __name__ == "__main__":
    main()