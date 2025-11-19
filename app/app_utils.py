from .bingo.bingo_utils import create_randomized_bingo_board
from .teams_data import teams_data
from termcolor import colored
from .constants import TEAMS_AMOUNT

"""
    Returns the initial data structure for a single team with the given teamID.
"""
def get_initial_team_data(team_ID: int) -> dict:
    initial_team_data = {
        "bingoBoard": {
            "board": create_randomized_bingo_board(team_ID),
            "filledPositions": []
        },
        "balls": {
            "grabbed": {
                "green": 0,
                "red": 0
            }
        },
        "roundsInfo": [],
        "hasWon": False,
        "ID": team_ID
    }
    return initial_team_data

"""
    Initializes the teams_data list with initial data for each team.
"""
def initialize_teams_data() -> None:
    for team_ID in range(TEAMS_AMOUNT):
        initial_team_data = get_initial_team_data(team_ID)
        teams_data.append(initial_team_data)

"""
    Prints a message to the terminal with optional color.
"""
def print_message(message: str, color: str = None) -> None:
    print("\n" + colored(message, color) + "\n")