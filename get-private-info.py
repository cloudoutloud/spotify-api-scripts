import requests
from urllib.parse import urlparse
import json
import os
import time
from secrets import *
import webbrowser

#----Functions----

# Authorize to Spotify API
def auth():

    payload = {'redirect_uri':'http://localhost', 'client_id': SPOTIFY_CLIENT_ID, 'client_secret': SPOTIFY_CLIENT_SECRET}

    scopes_num = int(input("Please enter number of scopes you wish to activate: "))
    scopes = [] 

    for scope in range(0, scopes_num):
        scope = str(input("\nPlease enter valid a scope for more information https://developer.spotify.com/documentation/general/guides/scopes/:  "))
        scopes.append(scope)

    print("\nConfirming scopes selected:", scopes)

    print("\nActivation box will open click ok, copy and paste the link you are redirected to from your browser starting with 'localhost'\n")
    firsturl = str("https://accounts.spotify.com/authorize/?client_id=" + SPOTIFY_CLIENT_ID + "&response_type=code&redirect_uri=http://localhost&scope=" + "%20".join(scopes))
    webbrowser.open(firsturl, new=0)
    
    url = input("\nPaste localhost url: ")
    # Error handling for wrong URL
    parsed_url = urlparse(url)
    payload['grant_type'] = 'authorization_code'
    payload['code'] = parsed_url.query.split('=')[1]
    auth_code = {}

    result = requests.post("https://accounts.spotify.com/api/token", data=payload)
    #print("\n",result.status_code)

    if result.status_code == 400:
        print("URL has expired")
    else:
        print("Successfully authorized to API")

    response_json = result.json()
    cur_seconds = time.time()
    auth_code['expires_at'] = cur_seconds + response_json["expires_in"] - 60
    auth_code['access_token'] = response_json["access_token"]

    # Creates auth json file with details
    with open('auth.json', 'w') as outfile:
        json.dump(auth_code, outfile)
        # # To see contents of dict
        # for x in auth_code:
        #     print(x)
    return auth_code

def get_valid_auth_header():
    with open('auth.json', 'r') as infile:
        auth = json.load(infile)
    if time.time() > auth["expires_at"]:
        auth = auth(auth)
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
    tracks = requests.get("https://api.spotify.com/v1/me/tracks/?limit=50&offset=20&market=GB", headers=headers)
    parsed = json.loads(tracks.text)
    print("\nPlease see full list of liked songs in songs.json\n")
    
    # Creates external json file with liked songs listed in pretty json
    with open('songs.json', 'w') as json_file:
        json.dump(parsed, json_file, indent=2)

#----Script----

auth()
get_valid_auth_header()
get_devices()
get_user_saved_track()
