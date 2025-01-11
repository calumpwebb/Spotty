import logging
from InquirerPy import inquirer

logger = logging.getLogger(__name__)

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def yes_no_select(prompt: str) -> bool:
    """
    Make a Yes/No selection using arrow keys. Returns True if 'Yes', False if 'No'.
    """
    logger.info(prompt)
    choice = inquirer.select(
        message="Use ↑/↓ to choose:",
        choices=[
            {"name": f"Yes", "value": True},
            {"name": f"No", "value": False},
        ],
        default=0,  # 'Yes' by default
    ).execute()
    return choice


def scrollable_playlist_view(tracks):
    """
    Display a scrollable list of tracks (via InquirerPy).
    If the playlist is longer than 100 tracks, we won't show it here
    because we already handle that limit during creation.
    """

    if len(tracks) == 0:
        logger.info("No tracks found.")
        return

    # If the playlist is small, just log them.
    if len(tracks) <= 10:
        logger.info("Track listing (<= 10 total):")
        for i, track in enumerate(tracks, start=1):
            logger.info(
                f" {i}. {track['name']} by {track['artist']} (pop={track['popularity']})"
            )
        return

    # Otherwise, let's do a scrollable list with InquirerPy.
    logger.info(f"Playlist has {len(tracks)} tracks, showing a scrollable list:")
    display_choices = [
        f"{i}. ({track['name']}) by {track['artist']} (pop={track['popularity']})"
        for i, track in enumerate(tracks, start=1)
    ]
    # The user doesn't actually select anything; we just let them scroll
    # until they press Enter. We'll label them all as "choices" for display.
    _ = inquirer.select(
        message="Scroll through tracks. Press Enter to finish viewing:",
        choices=display_choices,
        instruction="↑/↓ to scroll, Enter to exit track view",
        default=0,
    ).execute()
