import os
from json import load

# Let us read and use the Bingo settings
currentDir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(currentDir, 'bingo_settings.json'), 'r') as bingo_settings_file:
    bingo_settings = load(bingo_settings_file)


###
### GETTERS
###


def get_bingo_board_size() -> int:
    """
        Returns the size of the Bingo board (amount of rows and columns).
    """

    board_size = bingo_settings['board_size']
    return board_size

def get_bingo_number_colors() -> dict:
    """
        Returns the colors used for the Bingo numbers based on their state (marked/unmarked).
    """

    number_colors = bingo_settings['number_colors']
    return number_colors

def get_maximum_grabs_per_round() -> int:
    """
        Returns the maximum amount of grabs a team can make during their Bingo round.
    """

    max_grabs_per_round = bingo_settings['maximum_grabs_per_round']
    return max_grabs_per_round

def get_bingo_lose_conditions() -> dict:
    """
        Returns the lose conditions for the Bingo game.
    """

    lose_conditions = bingo_settings['lose_conditions']
    return lose_conditions

def get_bingo_win_conditions() -> dict:
    """
        Returns the win conditions for the Bingo game.
    """

    win_conditions = bingo_settings['win_conditions']
    return win_conditions