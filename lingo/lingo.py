from lingo.bingo.bingo_utils import has_team_lost_bingo_game
from .lingo_utils import get_next_team_ID, print_message, set_winning_team, initialize_teams_data, has_team_won_wordle_game
from .lingo_settings.lingo_settings_utils import get_starting_team_ID
from .wordle.wordle import play_wordle_round_for_team
from .wordle.wordle_utils import has_team_guessed_word_correctly_in_current_round, has_team_lost_wordle_game
from .bingo.bingo import play_bingo_round_for_team

"""
    Starts the game by initializing teams data and managing the game loop.
"""
def start_game() -> None:
    # Initialize the teams data which we store within the teams_data.py file
    initialize_teams_data()
    
    current_team_ID = get_starting_team_ID()

    while True:
        play_wordle_round_for_team(current_team_ID)

        # If the team has won the Wordle game, we set them as the winning team and break out of the loop early
        if has_team_won_wordle_game(current_team_ID):
            set_winning_team(current_team_ID)
            break

        # If the current team has lost the Wordle game, we set the next team as the winning team and break out of the loop early
        if has_team_lost_wordle_game(current_team_ID):
            current_team_ID = get_next_team_ID(current_team_ID)
            set_winning_team(current_team_ID)
            break

        if has_team_guessed_word_correctly_in_current_round(current_team_ID):
            play_bingo_round_for_team(current_team_ID)

            # If the team has lost the Bingo game, we set the next team as the winning team, else we set the current team as the winning team.
            # After that, we break out of the loop early
            if has_team_lost_bingo_game(current_team_ID):
                current_team_ID = get_next_team_ID(current_team_ID)
            set_winning_team(current_team_ID)
            break

        current_team_ID = get_next_team_ID(current_team_ID)

    ask_to_play_again()

"""
    Restart the game by re-initializing the teams data and starting the game.
"""
def restart_game() -> None:
    start_game()

"""
    Ask the user if they want to play again after the game ends.
"""
def ask_to_play_again() -> None:
    # Valid user input options
    valid_options = {
        'yes': ['yes', 'y'],
        'no': ['no', 'n']
    }
    
    while True:
        user_input = input("Do you want to play another game of Lingo? (yes/no): ").strip().lower()
        
        # If the user wants to play again we restart the game
        if user_input in valid_options['yes']:
            restart_game()
            return
        
        # If the user does not want to play again we print a thank you message and exit
        if user_input in valid_options['no']:
            print_message("Thanks for playing the game!")
            return
        
        # If the user input is invalid, we print an error message and ask again
        error_message = "Invalid input. Please enter 'yes' or 'no'."
        error_message_color = "red"
        print_message(error_message, error_message_color)