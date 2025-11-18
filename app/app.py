from .app_utils import initialize_teams_data
from .wordle.wordle import play_wordle

def start_game() -> None:
    initialize_teams_data()
    play_wordle()