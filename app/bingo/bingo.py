from app.app_utils import print_message
from .bingo_utils import *

"""
    Print the bingo board for the specified team.
"""
def print_bingo_board_for_team(team_ID: int) -> None:
    stringified_bingo_board = get_stringified_bingo_board_for_team(team_ID)
    print_message(stringified_bingo_board)