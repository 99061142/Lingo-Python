from termcolor import colored
from .lingo_settings.lingo_settings_utils import get_amount_of_teams
from .wordle.wordle_utils import has_team_lost_wordle_game, has_team_won_wordle_game
from .teams_data import teams_data
from .bingo.bingo_utils import get_randomized_bingo_board_for_team, has_team_lost_bingo_game, has_team_won_bingo_game


###
### GETTERS
###


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
    Returns whether the team has won the game based on the winning conditions.
"""
def has_team_won(team_ID: int) -> bool:
    won_bingo_game = has_team_won_bingo_game(team_ID)
    if won_bingo_game:
        return True
    
    won_wordle_game = has_team_won_wordle_game(team_ID)
    if won_wordle_game:
        return True
    
    return False

"""
    Returns whether the team has lost the game based on the losing conditions.
"""
def has_team_lost(team_ID: int) -> bool:
    # If the team has lost the bingo game
    lost_bingo_game = has_team_lost_bingo_game(team_ID)
    if lost_bingo_game:
        return True
    
    lost_wordle_game = has_team_lost_wordle_game(team_ID)
    if lost_wordle_game:
        return True
    
    return False


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