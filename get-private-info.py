import requests
from urllib.parse import urlparse
import json
import time
from secrets import *
import webbrowser
from private import private_auth

def get_valid_auth_header():
    private_auth()
    with open('auth.json', 'r') as infile:
        auth = json.load(infile)
    if time.time() > auth["expires_at"]:
        auth = private_auth()
    return {"Authorization": "Bearer " + auth["access_token"]}

# Get streaming devices for your account
def get_devices():
    headers = get_valid_auth_header()
    devices = requests.get("https://api.spotify.com/v1/me/player/devices", headers=headers)
    print(devices.status_code)

    if devices.status_code == 401:
        print('Please check you have correct "user-read-playback-state" scope')
    else:
        devices = devices.json()
        print("YOU ARE LISTENING TO MUSIC ON:", devices)

# Get list of liked songs from your libary
def get_user_saved_track():
    headers = get_valid_auth_header()
    tracks = requests.get("https://api.spotify.com/v1/me/tracks/?limit=1&offset=1&market=GB", headers=headers)
    parsed = json.loads(tracks.text)
    print("\nPlease see full list of liked songs in songs.json\n")

    with open('songs.json', 'w') as json_file:
        json.dump(parsed, json_file, indent=2)

# Get list of playlist from your libary
def get_private_playlist():
    headers = get_valid_auth_header()
    playlists = requests.get("https://api.spotify.com/v1/me/playlists/?limit=50&offset=10", headers=headers)
    parsed = json.loads(playlists.text)
    print("\nPlease see full list of liked playlists in playlists.json\n")

    with open('playlists.json', 'w') as json_file:
        json.dump(parsed, json_file, indent=2)

# get_devices()
get_user_saved_track()
# get_private_playlist()
