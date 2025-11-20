from .app_utils import initialize_teams_data
from .wordle.wordle import play_wordle

"""
    Starts the game by initializing teams data and starting the Wordle game.
"""
def start_game() -> None:
    initialize_teams_data()
    play_wordle()

"""
    Restart the game by re-initializing the teams data and starting the game.
"""
def restart_game() -> None:
    start_game()