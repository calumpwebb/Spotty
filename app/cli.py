import argparse


def parse_arguments():
    """
    Parses command-line arguments and returns them in an argparse.Namespace.
    """
    parser = argparse.ArgumentParser(
        description="Generate permutations of words, search Spotify for matching tracks, and create a playlist."
    )
    parser.add_argument(
        "--search-string",
        type=str,
        required=True,
        help="The string to permute and search for tracks in Spotify.",
    )
    parser.add_argument(
        "--playlist-name",
        type=str,
        help="Name for the newly-created Spotify playlist (cannot be used with --playlist-id).",
    )
    parser.add_argument(
        "--playlist-id",
        type=str,
        help="Use an existing Spotify playlist ID (cannot be used with --playlist-name).",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=4,
        help="Maximum grouping of words to attempt in permutations.",
    )
    parser.add_argument(
        "--access-token", type=str, required=True, help="Spotify OAuth access token."
    )
    parser.add_argument(
        "--max-search-results",
        type=int,
        default=20,
        help="Maximum number of search results from Spotify for each song name.",
    )

    args = parser.parse_args()

    # If both playlist-name and playlist-id are provided, raise an error.
    if args.playlist_name and args.playlist_id:
        parser.error(
            "Cannot specify both --playlist-name and --playlist-id. Please specify only one."
        )

    return args
