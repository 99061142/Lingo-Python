from app.app_utils import print_message
from .wordle_utils import *

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
def show_wordle_board(current_team_ID: int, max_attempts: int, word_to_guess_length: int, word_to_guess: str) -> None:
    stringified_wordle_board = get_stringified_wordle_board(current_team_ID, max_attempts, word_to_guess_length, word_to_guess)
    print(stringified_wordle_board)

"""
    Main function to play the Wordle game.
"""
def play_wordle() -> None:
    max_attempts = 5
    word_to_guess = get_random_word()
    word_to_guess_length = len(word_to_guess)

    current_team_ID = 0 

    while True:
        for row in range(max_attempts):
            show_wordle_board(current_team_ID, max_attempts, word_to_guess_length, word_to_guess)
            
            user_guess = ask_user_guess(row)

        current_team_ID = (current_team_ID + 1) % len(teamsData) # Switch to the next team. If we exceed the number of teams, go back to team 0.