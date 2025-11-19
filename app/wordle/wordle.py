from app.app_utils import print_message
from .wordle_utils import *
from ..constants import STARTING_TEAM_ID, MAX_ATTEMPTS, TEAMS_AMOUNT

"""
    Let the user input their guess.
"""
def ask_user_guess(attempt_number: int) -> str:
    while True:
        guess = input(f"Enter your 5-letter guess for row {attempt_number + 1}: ").strip().lower()
        guess_validation = is_valid_guess(guess)

        if guess_validation["isValid"]:
            return guess
        
        error_message = guess_validation["message"]
        print_color = "red"
        print_message(error_message, print_color)

"""
    Play a single Wordle round for the specified team.
"""
def play_wordle_round_for_team(team_ID: int) -> None:
    add_single_initial_rounds_info(team_ID)
    word_to_guess = get_current_wordle_round_word_to_guess(team_ID)

    for current_attempt in range(MAX_ATTEMPTS):
        show_wordle_board(team_ID)
        guess = ask_user_guess(current_attempt)
        add_guess_to_current_round(team_ID, guess, current_attempt)

        if guess == word_to_guess:
            show_wordle_board(team_ID)

            win_message = f"Team {team_ID + 1} guessed the word '{word_to_guess}' correctly!"
            print_color = "green"
            print_message(win_message, print_color)
            return

""""
    Print the current Wordle board for the specified team.
"""
def show_wordle_board(team_ID: int) -> None:
    stringified_wordle_board = get_stringified_wordle_board(team_ID)
    print_message(stringified_wordle_board)

"""
    Main function to play the Wordle game.
"""
def play_wordle() -> None:
    current_team_ID = STARTING_TEAM_ID
    board_width = get_wordle_board_width()

    while True:
        # Display which team's turn it is
        title = f"Team {current_team_ID + 1}'s turn"
        print_message(f"\n{title.center(board_width)}\n")

        play_wordle_round_for_team(current_team_ID)

        current_team_ID = (current_team_ID + 1) % TEAMS_AMOUNT