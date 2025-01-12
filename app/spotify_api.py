import logging
import requests
import sys

from app.caching import song_search_cache

logger = logging.getLogger(__name__)

# We always use market="US" and limit_per_request=20
DEFAULT_MARKET = "US"
LIMIT_PER_REQUEST = 20
MAX_TRACKS_PER_ADD = 100


def spotify_request(method="GET", url="", access_token="", params=None, json_data=None):
    """
    Makes a request to the Spotify API with the given method, URL,
    token, params, and JSON data. Logs an error if non-2xx response.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.request(
        method=method, url=url, headers=headers, params=params, json=json_data
    )

    if not 200 <= response.status_code < 300:
        logger.error(f"Spotify API Error: {response.status_code}, {response.json()}")
        return None

    return response


def search_song_by_name(song_name, access_token, max_results=20):
    """
    Searches Spotify for tracks with the exact `song_name` (in market=US).
    Returns a list of matching tracks sorted by popularity (descending).
    Uses a simple cache to avoid repeated requests for the same name.
    """

    if song_name in song_search_cache:
        logger.debug(f"Cache hit for: {song_name}")
        return song_search_cache[song_name]

    logger.debug(f"Cache miss for: {song_name}")

    url = "https://api.spotify.com/v1/search"
    tracks = []
    offset = 0

    while len(tracks) < max_results:
        params = {
            "q": f'track:"{song_name}"',
            "type": "track",
            "market": DEFAULT_MARKET,
            "limit": LIMIT_PER_REQUEST,
            "offset": offset,
        }

        response = spotify_request("GET", url, access_token, params=params)
        if not response:
            logger.warning(
                "Stopping track search due to API error or non-2xx response."
            )
            break

        results = response.json()
        items = results.get("tracks", {}).get("items", [])
        tracks.extend(items)

        if len(items) < LIMIT_PER_REQUEST:
            break
        offset += LIMIT_PER_REQUEST

    # Sort by popularity descending
    tracks = sorted(
        tracks[:max_results], key=lambda x: x.get("popularity", 0), reverse=True
    )
    # Filter to exact matches (case-insensitive)
    filtered_tracks = [t for t in tracks if t["name"].lower() == song_name.lower()]

    logger.debug(f"Found {len(filtered_tracks)} tracks matching '{song_name}' exactly.")
    song_search_cache[song_name] = filtered_tracks
    return filtered_tracks


def get_user_id(access_token):
    """
    Retrieves the current user ID from the Spotify API.
    """
    url = "https://api.spotify.com/v1/me"
    response = spotify_request("GET", url, access_token)
    if not response:
        logger.error("Unable to retrieve user ID. Exiting.")
        sys.exit(1)
    user_id = response.json().get("id")
    logger.info(f"Spotify user ID retrieved: {user_id}")
    return user_id


def create_playlist(access_token, playlist_name):
    """
    Creates a new Spotify playlist.
    Returns the full JSON response from the playlist creation API call.
    """

    user_id = get_user_id(access_token)
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    data = {"name": playlist_name, "public": False}

    logger.info(f"Creating playlist: '{playlist_name}' for user {user_id}...")
    response = spotify_request("POST", url, access_token, json_data=data)
    if not response:
        logger.error("Playlist creation returned an error.")
        return None

    playlist_info = response.json()
    logger.info(
        f"Playlist created: {playlist_info.get('name')} (ID: {playlist_info.get('id')})"
    )

    return playlist_info


def add_tracks_to_playlist(access_token, playlist_id, tracks):
    """
    Adds the list of tracks to the specified playlist by ID.
    """
    if len(tracks) > MAX_TRACKS_PER_ADD:
        logger.error(
            f"This playlist has more than {MAX_TRACKS_PER_ADD} tracks, which is too many. Aborting."
        )
        sys.exit(1)

    logger.info(f"Adding {playlist_id}")

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    uris = [track["uri"] for track in tracks]

    logger.info(f"Adding {len(uris)} tracks to playlist {playlist_id}...")
    data = {"uris": uris}
    spotify_request("POST", url, access_token, json_data=data)
