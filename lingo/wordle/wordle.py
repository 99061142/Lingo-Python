from .wordle_settings.wordle_settings_utils import get_max_wordle_guess_attempts, get_wordle_win_conditions, get_wordle_lose_conditions
from ..lingo_utils import get_next_team_ID, print_message, set_winning_team
from .wordle_utils import *

def ask_wordle_word_guess(attempt_number: int, team_ID: int) -> str:
    """
        Let the team input their Wordle word guess for their current attempt.
        If the guess isn't valid, we print an error message and ask again.
        Else, we return the valid guess.
    """

    while True:
        guess = input(f"Enter your 5-letter for attempt number {attempt_number + 1}: ").strip().lower()
        guess_validation = is_valid_wordle_guess(guess, team_ID)

        if guess_validation["isValid"]:
            return guess
        
        message = guess_validation["message"]
        message_color = "red"
        print_message(message, message_color)

def play_wordle_round_for_team(team_ID: int) -> None:
    """
        Play a single Wordle round for the specified team.
    """

    wordle_win_conditions = get_wordle_win_conditions()
    wordle_lose_conditions = get_wordle_lose_conditions()


    # Add the initial Wordle round info for the specified team.
    #! This must be done at the start of each Wordle round to set the Wordle round state correctly
    add_single_initial_rounds_info_for_team(team_ID)

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    
    print_wordle_round_for_team(team_ID)

    max_attempts = get_max_wordle_guess_attempts()
    for current_attempt in range(max_attempts):
        print_wordle_board_for_team(team_ID)
        
        guess = ask_wordle_word_guess(current_attempt, team_ID)

        # Add the team's guess to the current Wordle round board.
        #! This must be done after the team has made their guess, to update the Wordle round state correctly
        add_guess_to_current_round_for_team(team_ID, guess, current_attempt)

        if guess == word_to_guess:
            print_wordle_board_for_team(team_ID)

            message = f"Team {team_ID + 1} guessed the word '{word_to_guess}' correctly!"
            message_color = "green"
            print_message(message, message_color)
            
            # If the team has won the required number of Wordle rounds to win the Wordle game, we print the win message, set them as the winning team, and return True
            if amount_of_wordle_rounds_won_by_team(team_ID) >= wordle_win_conditions["rounds_won"]:
                message = f"Team {team_ID + 1} has won {wordle_win_conditions['rounds_won']} Wordle rounds and wins the Wordle game!"
                message_color = "green"
                print_message(message, message_color)

                # Set the team that has won the Lingo game as the current team
                set_winning_team(team_ID)

            return
    
    # If the team has lost the required number of Wordle rounds in a row to lose the Wordle game, we print the lose message, set the other team as the winning team, and return False
    if amount_of_wordle_rounds_lost_in_a_row_by_team(team_ID) >= wordle_lose_conditions["rounds_lost_in_a_row"]:
        print_wordle_board_for_team(team_ID)

        message = f"Team {team_ID + 1} has lost {wordle_lose_conditions['rounds_lost_in_a_row']} Wordle rounds in a row and loses the Wordle game!"
        message_color = "red"
        print_message(message, message_color)

        # Set the team that has won the Lingo game as the other team
        next_team_ID = get_next_team_ID(team_ID)
        set_winning_team(next_team_ID)
        
        return

    print_wordle_board_for_team(team_ID)

    # If the team has used all their attempts without guessing the word, 
    # but hasn't lost the required number of rounds in a row yet,
    # we just print the fail message for this round
    message = f"Team {team_ID + 1} failed to guess the word within the maximum attempts. The correct word was '{word_to_guess}'."
    message_color = "red"
    print_message(message, message_color)

def print_wordle_round_for_team(team_ID: int) -> None:
    """
        Print which team's turn it is for the current Wordle round in the terminal.
    """

    board_width = get_current_wordle_round_board_width_for_team(team_ID)
    message = f"Team {team_ID + 1}'s turn"
    print_message(message.center(board_width))

def print_wordle_board_for_team(team_ID: int) -> None:
    """
        Print the current round's Wordle board for the specified team in the terminal.
    """

    stringified_wordle_board_for_team = get_stringified_current_wordle_round_board_for_team(team_ID)
    print_message(stringified_wordle_board_for_team)