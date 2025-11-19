from app.app_utils import print_message
from .wordle_utils import *
from ..constants import STARTING_TEAM_ID

"""
    Let the user input their guess.
"""
def ask_user_guess(current_row: int) -> str:
    while True:
        guess = input(f"Enter your 5-letter guess for row {current_row + 1}: ").strip().lower()
        guess_validation = is_valid_guess(guess)

        if guess_validation["isValid"]:
            return guess
        
        error_message = guess_validation["message"]
        print_color = "red"
        print_message(error_message, print_color)

""""
    Print the current Wordle board for the specified team.
"""
def show_wordle_board(team_ID: int) -> None:
    stringified_wordle_board = get_stringified_wordle_board(team_ID)
    print(stringified_wordle_board)

"""
    Main function to play the Wordle game.
"""
def play_wordle() -> None:
    pass