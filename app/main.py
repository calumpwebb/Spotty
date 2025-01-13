import logging
import sys

from app.cli import parse_arguments
from app.spotify_api import create_playlist, add_tracks_to_playlist
from app.caching import song_search_cache
from app.permutations import generate_all_sentence_permutations
from app.prompts import yes_no_select, scrollable_playlist_view
from InquirerPy import inquirer

# ANSI color codes (for terminal color). Adjust as needed.
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def fetch_tracks_for_grouping(grouping, access_token, max_results=20):
    """
    For each term in `grouping`, fetch exact matching tracks from Spotify.
    If any term has no matching tracks, return None for that entire permutation.
    Otherwise, returns a list of track lists (parallel to each term).
    """
    from app.spotify_api import search_song_by_name  # local import to avoid circular

    all_tracks = []
    for term in grouping:
        tracks = search_song_by_name(term, access_token, max_results)
        if not tracks:
            return None
        all_tracks.append(tracks)
    return all_tracks


def main():
    global song_search_cache
    args = parse_arguments()

    search_string = args.search_string
    playlist_name = args.playlist_name
    playlist_id = args.playlist_id
    max_words = args.max_words
    access_token = args.access_token
    max_search_results = args.max_search_results

    logger.info(f"{GREEN}Starting the Spotify playlist script...{RESET}")
    logger.info(
        f"Search string: '{search_string}', Playlist name: '{playlist_name}', Playlist id: '{playlist_id}"
    )

    sentences, sentence_permutations = generate_all_sentence_permutations(
        search_string, max_word_count_per_sentence=max_words
    )

    all_potential_playlists = []

    for i, word_permutations in enumerate(sentence_permutations):
        logger.info(
            f"Found {len(word_permutations):,} permutations in total for sentence {i}."
        )

        # Search for tracks for each permutation
        potential_playlists = []

        logger.info(
            "Beginning track searches for each permutation. This may take a while..."
        )

        total_permutations = len(word_permutations)

        for j, grouping in enumerate(word_permutations, start=1):
            pct_done = (i / total_permutations) * 100
            progress_color = RED
            if len(potential_playlists) > 0:
                progress_color = GREEN

            sys.stdout.write(
                f"\r{progress_color}Progress:{RESET} {i:,}/{total_permutations:,} "
                f"({pct_done:.2f}%) | Potential playlists found: {len(potential_playlists)} [{len(song_search_cache)} API searches]"
            )
            sys.stdout.flush()

            all_tracks = fetch_tracks_for_grouping(
                grouping, access_token, max_results=max_search_results
            )
            if not all_tracks:
                continue

            track_list = []
            for tracks_for_term in all_tracks:
                first_track = tracks_for_term[0]
                track_list.append(
                    {
                        "id": first_track["id"],
                        "name": first_track["name"],
                        "popularity": first_track["popularity"],
                        "artist": (
                            first_track["artists"][0]["name"]
                            if first_track.get("artists")
                            else "Unknown"
                        ),
                        "uri": first_track["uri"],
                    }
                )
            potential_playlists.append(track_list)

        print()

        print(potential_playlists)
        if potential_playlists:
            all_potential_playlists.append(potential_playlists)
        else:
            logger.warning(
                f"Unable to make a playlist as no valid sets of tracks matched. Unable to match \n\t'{sentences[i]}'"
            )
            sys.exit(0)

    for potential_playlists in all_potential_playlists:
        logger.info(f"Found {len(potential_playlists)} potential playlists total.")

        # Prepare user choices
        choices = []
        for idx, playlist in enumerate(potential_playlists, start=1):
            total_score = sum(t["popularity"] for t in playlist)
            choice_name = (
                f"Playlist #{idx} | Score={total_score} | {len(playlist)} track(s)"
            )
            choices.append({"name": choice_name, "value": idx - 1})

        # Loop until the user creates a playlist or exits
        selecting = True
        while selecting:
            chosen_idx = inquirer.select(
                message="Select the playlist you want to examine/create:",
                choices=choices,
                instruction="↑/↓ to navigate, Enter to select",
            ).execute()

            selected_playlist = potential_playlists[chosen_idx]
            total_score = sum(t["popularity"] for t in selected_playlist)
            logger.info(
                f"You selected playlist #{chosen_idx+1} with total popularity score of {total_score}."
            )

            scrollable_playlist_view(selected_playlist)

            action_verb = "create"

            if playlist_id is not None:
                action_verb = "add"

            if yes_no_select(f"Do you want to {action_verb} this playlist?"):

                if playlist_id is None:
                    created_playlist = create_playlist(access_token, playlist_name)

                    if created_playlist:
                        logger.info(
                            f"{GREEN}✅ Successfully created playlist:{RESET} {created_playlist.get('name')}"
                        )
                        playlist_id = created_playlist["id"]
                    else:
                        logger.error("Playlist creation failed.")
                        break

                add_tracks_to_playlist(access_token, playlist_id, selected_playlist)
                selecting = False
            else:
                logger.info(
                    "User chose not to create this playlist. Going back to selection."
                )


if __name__ == "__main__":
    main()
