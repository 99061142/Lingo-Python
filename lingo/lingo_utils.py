from termcolor import colored
from .teams_data import teams_data
from .lingo_settings.lingo_settings_utils import get_amount_of_teams
from .bingo.bingo_utils import get_randomized_bingo_board_for_team


###
### GETTERS
###


def get_next_team_ID(current_team_ID: int) -> int:
    """
        Returns the next team ID in a circular manner.
    """

    teams_amount = get_amount_of_teams()
    next_team_ID = (current_team_ID + 1) % teams_amount
    return next_team_ID

def get_initial_team_data_for_team(team_ID: int) -> dict:
    """
        Returns the initial data structure for the specified team.
    """

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
        "hasWon": False,
        "hasLost": False
    }
    return initial_team_data

def has_team_won_lingo_game(team_ID: int) -> bool:
    """
        Returns whether the team has won the Lingo game.
    """

    team_data = teams_data[team_ID]
    has_won = team_data["hasWon"]
    return has_won

def has_team_lost_lingo_game(team_ID: int) -> bool:
    """
        Returns whether the team has lost the Lingo game.
    """

    team_data = teams_data[team_ID]
    has_lost = team_data["hasLost"]
    return has_lost

def get_winning_team_ID() -> int:
    """
        Return the team ID of the team that has won the Lingo game.
    """

    team_amount = get_amount_of_teams()
    for team_ID in range(team_amount):
        if has_team_won_lingo_game(team_ID):
            return team_ID

def get_losing_team_ID() -> int:
    """
        Return the team ID of the team that has lost the Lingo game.
    """

    team_amount = get_amount_of_teams()
    for team_ID in range(team_amount):
        if has_team_lost_lingo_game(team_ID):
            return team_ID


### 
### SETTERS
###


def initialize_teams_data() -> None:
    """
        Initializes the list that holds the data for each team.
    """

    # Clear any existing data first
    remove_teams_data()

    amount_of_teams = get_amount_of_teams()
    for team_ID in range(amount_of_teams):
        initial_team_data = get_initial_team_data_for_team(team_ID)
        teams_data.append(initial_team_data)

def remove_teams_data() -> None:
    """
        Clears the teams_data list.
    """

    teams_data.clear()

def set_winning_team(team_ID: int) -> None:
    """
        Sets the winning status for the specified team, 
        while also setting the losing status for the other team if it hasn't already been set.
    """

    teams_data[team_ID]["hasWon"] = True

def set_losing_team(team_ID: int) -> None:
    """
        Sets the losing status for the specified team, 
        while also setting the winning status for the other team if it hasn't already been set.
    """

    teams_data[team_ID]["hasLost"] = True


###
### UTILITIES
###


def print_message(message: str, color: str = "white") -> None:
    """
        Print a colored message in the terminal.
    """

    colored_message = colored(message, color)
    print(f"\n{colored_message}\n")