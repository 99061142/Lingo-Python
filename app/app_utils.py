from .bingo.bingo_utils import create_randomized_bingo_board
from .teamsData import teamsData
from termcolor import colored

"""
    Returns the initial data structure for a single team with the given teamID.
"""
def get_initial_team_data(teamID: int) -> dict:
    initial_team_data = {
        "bingoBoard": {
            "board": create_randomized_bingo_board(teamID),
            "filledPositions": []
        },
        "balls": {
            "grabbed": {
                "green": 0,
                "red": 0,
                "numbers": 0
            }
        },
        "roundsInfo": [
            {
                "guesses": [],
                "guessesColor": [
                    [
                        "green"
                    ]
                ] 
            } # We set the first letter green when the round starts. This is why the `guesses` is empty even if `guessesColor` has one entry.
        ],
        "hasWon": False,
        "ID": teamID
    }
    return initial_team_data

"""
    Initializes the teamsData list with initial data for each team.
"""
def initialize_teams_data() -> None:
    teams_amount = 2 # Currently supporting 2 teams.

    for teamID in range(teams_amount):
        initial_team_data = get_initial_team_data(teamID)
        teamsData.append(initial_team_data)