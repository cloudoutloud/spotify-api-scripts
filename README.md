# Spotify API Scripts

A collection of Python scripts for querying and managing your Spotify library via the Web API.

## Overview

These scripts use Spotify's OAuth 2.0 authentication to access both public and private user data:

- **Public API**: Access catalog information (track/artist details) without user authentication
- **Private API**: Access user-specific data (saved tracks, playlists, devices) with authentication

### Prerequisites

- Spotify Developer Account (create one at https://developer.spotify.com/dashboard)
- Python 3.x with `requests` library installed

### Installation

1. Clone or download this repository
2. Set your Spotify credentials as environment variables:

```bash
export SPOTIFY_CLIENT_ID=your_client_id
export SPOTIFY_CLIENT_SECRET=your_client_secret
```

Get your credentials from: https://developer.spotify.com/dashboard/applications

3. Register your redirect URI in Spotify Dashboard under "Edit Settings":
   - Add `http://127.0.0.1:8888` to Redirect URIs

## Scripts

### `public.py`
**Authenticates using Client Credentials Flow**
- No user interaction required
- Scope: None (public data only)
- Use for accessing public catalog information

### `public_endpoints.py`
**Query public Spotify catalog data**
- Valid endpoints: `tracks`, `audio-features`, `audio-analysis`, `artists`
- Examples:
  - `tracks` - get track information (requires track ID)
  - `audio-features` - get audio analysis for a track
  - `artists` - get artist information (requires artist ID)

### `private.py`
**Authenticates using Authorization Code Flow**
- Requires user approval in browser
- Stores access token in `auth.json`
- Scope: User configurable (up to 17 scopes available)

### `get_saved_tracks.py`
**Download all your liked songs**
- Required scope: `user-library-read`
- Outputs: `saved_tracks.json` (name and artist for each track)
- Fetches all tracks with pagination

### `get-private-info.py`
**Access your private user data**
Required scopes:
  - `user-read-playback-state` - for devices
  - `user-library-read` - for liked songs
  - `playlist-read-private` - for private playlists

Functions:
  - `get_devices()` - list your streaming devices
  - `get_user_saved_track()` - get liked songs
  - `get_private_playlist()` - get your playlists

## Usage Examples

### Get public track information
```bash
python3 public_endpoints.py
# Enter: tracks
# Enter track ID: 3n3Ppam7vgaVa1iaRUc9Lp
```

### Download all your liked songs
```bash
python3 get_saved_tracks.py
```

### Access private playlists and devices
```bash
python3 get-private-info.py
```

## Available Scopes

For private API authentication:
- `user-library-read` - Read saved tracks/albums
- `playlist-read-private` - Read private playlists
- `user-read-playback-state` - Read current playback device
- `user-modify-playback-state` - Control playback
- `user-read-private` - Read user profile
- `user-read-email` - Access user email
- And 11 more (see [Spotify docs](https://developer.spotify.com/documentation/general/guides/scopes/))

## Files Created

- `auth.json` - Stores access token and expiration (private auth)
- `saved_tracks.json` - Your liked songs
- `playlists.json` - Your playlists
- `songs.json` - Liked songs

## References

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [OAuth 2.0 Authorization Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
- [Available Scopes](https://developer.spotify.com/documentation/general/guides/scopes/)
