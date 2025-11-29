import os
from json import load

# Let us read and use the Wordle settings
currentDir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(currentDir, "wordle_settings.json"), "r") as wordle_settings_file:
    wordle_settings = load(wordle_settings_file)


###
### GETTERS
###


def get_empty_column_placeholder_for_wordle_board() -> str:
    """
        Return the letter placeholder used for empty letters on the Wordle board.
    """

    letter_placeholder = wordle_settings["empty_column_placeholder"]
    return letter_placeholder

def get_max_wordle_guess_attempts() -> int:
    """
        Return the maximum attempts allowed for guessing the Wordle word.
    """

    max_attempts = wordle_settings["max_guess_attempts"]
    return max_attempts

def get_available_letter_position_colors() -> dict:
    """
        Return the available letter position colors.
    """

    available_letter_position_colors = wordle_settings["letter_color_for_guess"]
    return available_letter_position_colors

def get_wordle_win_conditions() -> dict:
    """
        Return the win conditions for the Wordle game.
    """

    win_conditions = wordle_settings["win_conditions"]
    return win_conditions

def get_wordle_lose_conditions() -> dict:
    """
        Return the lose conditions for the Wordle game.
    """

    lose_conditions = wordle_settings["lose_conditions"]
    return lose_conditions