from termcolor import colored
from .lingo_settings.lingo_settings_utils import get_amount_of_teams
from .teams_data import teams_data
from .bingo.bingo_utils import get_randomized_bingo_board_for_team


###
### GETTERS
###


"""
    Returns the next team ID in a circular manner.
"""
def get_next_team_ID(current_team_ID: int) -> int:
    teams_amount = get_amount_of_teams()
    next_team_ID = (current_team_ID + 1) % teams_amount
    return next_team_ID

"""
    Returns the initial data structure for a single team with the given teamID.
"""
def get_initial_team_data_for_team(team_ID: int) -> dict:
    initial_team_data = {
        "bingoBoard": {
            "board": get_randomized_bingo_board_for_team(team_ID),
            "filledPositions": set()
        },
        "balls": {
            "grabbed": {
                "green": 0,
                "red": 0
            },
            "remaining": {
                "green": 3,
                "red": 3
            }
        },
        "roundsInfo": [],
        "hasWon": False
    }
    return initial_team_data

"""
    Returns whether any team has won the Lingo game.
"""
def has_any_team_won_lingo_game() -> bool:
    for team_ID in range(get_amount_of_teams()):
        if has_team_won_lingo_game(team_ID):
            return True
    return False

"""
    Returns whether the team has won the Lingo game.
"""
def has_team_won_lingo_game(team_ID: int) -> bool:
    team_data = teams_data[team_ID]
    has_won = team_data["hasWon"]
    return has_won

### 
### SETTERS
###


"""
    Initializes the teams_data list with initial data for each team.
"""
def initialize_teams_data() -> None:
    remove_teams_data()

    for team_ID in range(get_amount_of_teams()):
        initial_team_data = get_initial_team_data_for_team(team_ID)
        teams_data.append(initial_team_data)

"""
    Resets the teams_data list to an empty state.
"""
def remove_teams_data() -> None:
    teams_data.clear()

"""
    Sets the winning status for the specified team.
"""
def set_winning_team(team_ID: int) -> None:
    teams_data[team_ID]["hasWon"] = True


###
### UTILITIES
###


"""
    Prints a message to the terminal with optional color.
"""
def print_message(message: str, color: str = "white") -> None:
    colored_message = colored(message, color)
    print(f"\n{colored_message}\n")