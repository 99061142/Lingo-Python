from ..wordle.wordle_settings.wordle_settings_utils import get_max_wordle_guess_attempts
from ..lingo_utils import get_next_team_ID, print_message, set_winning_team
from .wordle_utils import *

"""
    Let the user input their guess.
    If the guess is valid, we return it.
    If not, we print an error message and ask again.
"""
def ask_wordle_word_guess(attempt_number: int, team_ID: int) -> str:
    while True:
        guess = input(f"Enter your 5-letter guess for row {attempt_number + 1}: ").strip().lower()
        guess_validation = is_valid_wordle_guess(guess, team_ID)

        if guess_validation["isValid"]:
            return guess
        
        error_message = guess_validation["message"]
        error_message_color = "red"
        print_message(error_message, error_message_color)

"""
    Play a single Wordle round for the specified team.
"""
def play_wordle_round_for_team(team_ID: int) -> None:
    # Add the initial round info for the team within the global teams_data structure.
    #! Do note that we must do this before calling any other functions which rely on the current round info existing. 
    #! Which in most cases, are most functions within the wordle_utils.py file.
    add_single_initial_rounds_info_for_team(team_ID)

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    print_wordle_round_for_team(team_ID)

    for current_attempt in range(get_max_wordle_guess_attempts()):
        print_wordle_board_for_team(team_ID)
        
        guess = ask_wordle_word_guess(current_attempt, team_ID)
        add_guess_to_current_round_for_team(team_ID, guess, current_attempt)

        if guess == word_to_guess:
            print_wordle_board_for_team(team_ID)

            win_message = f"Team {team_ID + 1} guessed the word '{word_to_guess}' correctly!"
            print_color = "green"
            print_message(win_message, print_color)
            
            # If the team has won 10 Wordle rounds, we print the win message and set the current team as the winning team
            if amount_of_wordle_rounds_won_by_team(team_ID) >= 10:
                win_message = f"Team {team_ID + 1} has won 10 Wordle rounds and wins the Wordle game!"
                print_color = "green"
                print_message(win_message, print_color)

                set_winning_team(team_ID)

            return
    
    # If the team has lost 3 Wordle rounds in a row, we print the fail message, set the next team as the winning team, and return
    if amount_of_wordle_rounds_lost_in_a_row_by_team(team_ID) >= 3:
        fail_message = f"Team {team_ID + 1} has lost 3 Wordle rounds in a row and loses the Wordle game!"
        print_color = "red"
        print_message(fail_message, print_color)

        next_team_ID = get_next_team_ID(team_ID)
        set_winning_team(next_team_ID)
        return
    
    # If the team has used all their attempts without guessing the word, 
    # but hasn't lost 3 rounds in a row yet, 
    # we just print the fail message for this round
    fail_message = f"Team {team_ID + 1} failed to guess the word within the maximum attempts. The correct word was '{word_to_guess}'."
    print_color = "red"
    print_message(fail_message, print_color)

"""
    Print which team's turn it is.
"""
def print_wordle_round_for_team(team_ID: int) -> None:
    # Use the board width for the current round to center the message
    board_width = get_current_wordle_round_board_width_for_team(team_ID)
    message = f"Team {team_ID + 1}'s turn"
    print_message(f"{message.center(board_width)}")

"""
    Print the current round's wordle board for the specified team.
"""
def print_wordle_board_for_team(team_ID: int) -> None:
    stringified_wordle_board_for_team = get_stringified_current_wordle_round_board_for_team(team_ID)
    print_message(stringified_wordle_board_for_team)