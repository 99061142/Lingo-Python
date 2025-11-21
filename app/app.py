from .app_utils import print_message, set_winning_team, initialize_teams_data
from .app_settings.app_settings_utils import get_amount_of_teams, get_starting_team_ID
from .wordle.wordle import play_wordle_round_for_team
from .wordle.wordle_utils import any_team_has_won_or_lost_the_wordle_game, has_team_guessed_word_correctly_in_current_round
from .bingo.bingo import play_bingo_round_for_team

"""
    Starts the game by initializing teams data and managing the game loop.
"""
def start_game() -> None:
    # Initialize the teams data which we store within the teams_data.py file
    initialize_teams_data()
    
    current_team_ID = get_starting_team_ID()
    teams_amount = get_amount_of_teams()

    while not any_team_has_won_or_lost_the_wordle_game():
        play_wordle_round_for_team(current_team_ID)

        # If the current team has won the Wordle game, we break out of the loop early
        if has_team_guessed_word_correctly_in_current_round(current_team_ID):
            play_bingo_round_for_team(current_team_ID)

        # Move to the next team, or back to the first team if all teams have played
        current_team_ID = (current_team_ID + 1) % teams_amount

    set_winning_team(current_team_ID)

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
        user_input = input("Do you want to play again? (yes/no): ").strip().lower()
        
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