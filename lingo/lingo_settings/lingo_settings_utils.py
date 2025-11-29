import os
from json import load

# Let us read and use the Lingo settings
currentDir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(currentDir, 'lingo_settings.json'), 'r') as lingo_settings_file:
    lingo_settings = load(lingo_settings_file)


###
### GETTERS
###


def get_amount_of_teams() -> int:
    """
        Returns the amount of teams playing the game.
    """

    amount_of_teams = lingo_settings['teams_amount']
    return amount_of_teams

def get_starting_team_ID() -> int:
    """
        Returns the starting team ID.
    """

    starting_team_ID = lingo_settings['starting_team_ID']
    return starting_team_ID