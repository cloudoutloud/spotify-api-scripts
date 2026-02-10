import os
import requests

access_token = None

def public_auth():
    global access_token
    print("Authenticating to spotify API.....")

    auth_url = 'https://accounts.spotify.com/api/token'

    try:
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
        })

        if auth_response.status_code == 200:
            print('You have successfully authenticated to the Spotify API')
        elif auth_response.status_code in [400, 404, 500]:
            print('[!] Error bad request')
        else:
            print('[!] Request has failed')

    except requests.exceptions.RequestException as e:
        print(f"[!] A network error occurred: {e}")

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']