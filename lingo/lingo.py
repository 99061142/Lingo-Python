from .lingo_utils import get_next_team_ID, print_message, has_team_won_lingo_game, initialize_teams_data
from .lingo_settings.lingo_settings_utils import get_starting_team_ID
from .wordle.wordle import play_wordle_round_for_team
from .wordle.wordle_utils import has_team_won_or_lost_wordle_game, has_team_guessed_word_correctly_in_current_wordle_round
from .bingo.bingo import play_bingo_round_for_team
from .bingo.bingo_utils import has_team_won_or_lost_bingo_game

def print_winning_team_message(team_ID: int) -> None:
    """
        Print a winning message for the specified team in the terminal.
    """

    message = f"Team {team_ID + 1} wins the game of Lingo!"
    message_color = "green"
    print_message(message, message_color)

def print_losing_team_message(team_ID: int) -> None:
    """
        Print a losing message for the specified team in the terminal.
    """

    message = f"Team {team_ID + 1} has lost the game of Lingo."
    message_color = "red"
    print_message(message, message_color)

def start_game() -> None:
    """
        Start the Lingo game.
    """

    # Initialize the teams data.
    # This must be done at the start of the Lingo game
    initialize_teams_data()
    
    # Set the team that will start the game as the team ID which is set in the Lingo settings
    current_team_ID = get_starting_team_ID()

    while True:
        play_wordle_round_for_team(current_team_ID)

        # If any team has won or lost the Wordle game, we break out of the loop early
        if has_team_won_or_lost_wordle_game(current_team_ID):
            break

        # If the current team has guessed the current word correctly for the Wordle round, they get to play a Bingo round
        if has_team_guessed_word_correctly_in_current_wordle_round(current_team_ID):
            play_bingo_round_for_team(current_team_ID)

            # If any team has won or lost the Bingo game, we break out of the loop early
            if has_team_won_or_lost_bingo_game(current_team_ID):
                break
        
        # Switch to the next team to let them play the next Lingo round
        current_team_ID = get_next_team_ID(current_team_ID)

    # Print the winning or losing message for the team based on whether they have won or lost the Lingo game
    if has_team_won_lingo_game(current_team_ID):
        print_winning_team_message(current_team_ID)
    else:
        print_losing_team_message(current_team_ID)

    # Ask both teams if they want to play the Lingo game again
    ask_to_play_again()

def restart_game() -> None:
    """
        Restart the Lingo game.
    """

    start_game()

def ask_to_play_again() -> None:
    """
        Ask both teams if they want to play another game of Lingo.
    """

    # Valid user input options
    valid_options = {
        'yes': ['yes', 'y'],
        'no': ['no', 'n']
    }
    
    while True:
        user_input = input("Do you want to play another game of Lingo? (yes/no): ").strip().lower()
        
        # If both teams want to play again we restart the Lingo game
        if user_input in valid_options['yes']:
            restart_game()
            return
        
        # If both teams do not want to play another game of Lingo, we thank them for playing, and exit the application
        if user_input in valid_options['no']:
            print_message("Thanks for playing the game!")
            exit(0)
        
        # If both teams provided an answer that is not valid, we print an error message and ask them the question again
        message = f"Invalid input. Please enter one of the following options: {', '.join(valid_options.keys())}."
        message_color = "red"
        print_message(message, message_color)