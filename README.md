# Spotify Playlist Creator

Spotty is a Spotify Playlist Creator that can create a new (or update) playlist based on an input string where each song corresponds to a word (or set of words) in the string.

Created by Calum Webb 2025

## How to use

You'll need to sign up for the Spotify Developer API program and fetch your `client_id` and `client_secret` for the steps below.

```bash
chmod +x ./run-api.sh

./run-api.sh \
   --client-id "<CLIENT_ID_HERE>" \
   --client-secret "<CLIENT_SECRET_HERE>"
```

Open up your browser at http://localhost:8888/login to find your access token (you'll need this in the next step).

```bash
chmod +x ./run.sh

# Creating: 
# When creating a new playlist, specify "playlist-name".
./run.sh \
  --access-token "<ACCESS_TOKEN_FROM_ABOVE>" \
  --playlist-name "My New Playlist" \
  --search-string "This is the search string that will display the playlist"

# Updating: 
# When updating an existing playlist (this will append the search texts to the end of the playlist, which is useful for long playlists),
# specify the playlist ID.
./run.sh \
  --access-token "<ACCESS_TOKEN_FROM_ABOVE>" \
  --playlist-id "<PLAYLIST_ID>" \
  --search-string "This is the search string that will display the playlist"
```

## Notes
The maximum number of songs added at once is 100, so be careful with long sentences.
Long sentences generate more permutations. If the app is too slow, break down the input into multiple runs and append each time with new sentences.
