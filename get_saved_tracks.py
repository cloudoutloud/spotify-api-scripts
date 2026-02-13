import requests
import json
from private import private_auth

# Need scope user-library-read
def get_saved_tracks():
    """Get all tracks saved in user's library"""
    auth_code = private_auth()

    access_token = auth_code['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    all_tracks = []
    url = 'https://api.spotify.com/v1/me/tracks'

    # Paginate through all saved tracks
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Add tracks from this page
        for item in data.get('items', []):
            track = item.get('track', {})
            all_tracks.append({
                'name': track.get('name'),
                'artist': ', '.join([artist['name'] for artist in track.get('artists', [])])
            })

        # Get next page URL
        url = data.get('next')

    # Save to file
    with open('saved_tracks.json', 'w') as f:
        json.dump(all_tracks, f, indent=2)

    print(f"Found {len(all_tracks)} saved tracks")
    print(f"Saved to saved_tracks.json")

    # Print first 10
    print("\nFirst 10 tracks:")
    for i, track in enumerate(all_tracks[:10], 1):
        print(f"{i}. {track['name']} - {track['artist']}")

if __name__ == '__main__':
    get_saved_tracks()
