from .app_utils import initialize_teams_data, print_message
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

"""
    Ask the user if they want to play again after the game ends.
    If they do, we restart the game.
    If not, we print a thank you message.
"""
def ask_to_play_again() -> None:
    # Valid user input options
    valid_options = {
        'yes': ['yes', 'y'],
        'no': ['no', 'n']
    }
    
    while True:
        user_input = input("Do you want to play again? (yes/no): ").strip().lower()
        
        # If they user wants to play again
        if user_input in valid_options['yes']:
            restart_game()
            return
        
        # If the user does not want to play again
        if user_input in valid_options['no']:
            print_message("Thank's for playing the game!'")
            return
        
        error_message = "Invalid input. Please enter 'yes' or 'no'."
        error_message_color = "red"
        print_message(error_message, error_message_color)