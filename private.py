import sys
import json
from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import webbrowser
import time
from urllib.parse import urlparse, parse_qs
import requests


# Auth to API with scopes using a access token
def private_auth():

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

    url = input("\nPaste localhost authentication url: ")

    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL: Missing scheme or netloc")

        query_params = parse_qs(parsed_url.query)
        if 'code' not in query_params:
            raise ValueError("Invalid URL: Missing 'code' query parameter")

        payload['grant_type'] = 'authorization_code'
        payload['code'] = query_params['code'][0]
        auth_code = {}

        print("URL parsed successfully.")

    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)

    try:
        result = requests.post("https://accounts.spotify.com/api/token", data=payload)
        result.raise_for_status()
        response_json = result.json()

        cur_seconds = time.time()
        auth_code['expires_at'] = cur_seconds + response_json["expires_in"] - 60
        auth_code['access_token'] = response_json["access_token"]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        sys.exit(1)
    except Exception as err:
        print(f"An error occurred: {err}")
        sys.exit(1)

    with open('auth.json', 'w') as outfile:
        json.dump(auth_code, outfile)
    return auth_code
