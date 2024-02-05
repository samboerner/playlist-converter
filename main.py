import spotipy
import spotipy.util as util
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv


load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)