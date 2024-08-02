# This script is using the Client Credentials Flow method to authenticate.
# https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# You will NOT be able to manage or access user private data only public information such as track/artist information.

import requests
from public import public_auth

api_endpoint = None
api_url = None

def endpoint():
    api_url_base = 'https://api.spotify.com/v1/'
    global api_endpoint
    api_endpoint = input('Please provide valid endpoint: ')
    global api_url
    api_url = api_url_base + api_endpoint

def get_track_info():
    from public import access_token
    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    track_id = input('Please provide valid track ID: ')

    if str(track_id) != '':
        print('Valid track ID')
    else:
        print('Error please provide valid track ID: ')


    r = requests.get(api_url + '/' + track_id, headers=headers)
    r = r.json()
    print(r)

def get_artists_info():
    from public import access_token
    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    artist_id = input('Please provide valid artist ID: ')
    # sub_endpoint = input('Please provide artist sub endpoint: ')

    if str(artist_id) != '':
        print('Valid artist ID')
    else:
        print('Error please provide valid artist ID: ')

    r = requests.get(api_url + '/' + artist_id, headers=headers)
    r = r.json()
    print(r)

public_auth()
endpoint()
print(api_url)
if api_endpoint == 'tracks' or api_endpoint == 'audio-features' or api_endpoint == 'audio-analysis':
    get_track_info()
elif api_endpoint == 'artists':
    get_artists_info()
else:
    print("Endpoint does not exists for full list please see https://developer.spotify.com/documentation/web-api/reference/")
