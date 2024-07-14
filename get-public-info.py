# This script is using the Client Credentials Flow method to authenticate.
# https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# You will NOT be able to manage or access user private data only public information such as track/artist information.

from secrets import *
import requests
import json

# Authenticate to API
def auth():

    print("Authenticating to spotify API.....")

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # Post to API
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    })

    if auth_response.status_code == 200:
        print(auth_response.status_code)
        print('You have sucessfully authenticated to spotify API!')
    elif auth_response.status_code == 400 or 404 or 500:
        print(auth_response.status_code)
        print('[!] Error bad request')
    else:
        print('[!] Request has Failed')

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token and make a global variable
    global access_token
    access_token = auth_response_data['access_token']

    print("Your spotify access token is:")
    print(access_token)

# Define the endpoint
def endpoint():
    api_url_base = 'https://api.spotify.com/v1/'
    # Full list of endpoints https://developer.spotify.com/documentation/web-api/reference/
    global api_endpoint
    api_endpoint = input('Please provide valid endpoint: ')
    global api_url
    api_url = api_url_base + api_endpoint

# Tracks
def get_track_info():

    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    track_id = input('Please provide valid track ID: ')

    if str(track_id) != '':
        print('Valid track ID')
    else:
        print('Error please provide valid track ID: ')


    r = requests.get(api_url + '/' + track_id, headers=headers)
    r = r.json()
    print(r)

# Artists
def get_artists_info():

    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
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

auth()
endpoint()
print(api_url)

if api_endpoint == 'tracks' or api_endpoint == 'audio-features' or api_endpoint == 'audio-analysis':
    get_track_info()
elif api_endpoint == 'artists':
    get_artists_info()
else:
    print("Endpoint does not exists for full list please see https://developer.spotify.com/documentation/web-api/reference/")
