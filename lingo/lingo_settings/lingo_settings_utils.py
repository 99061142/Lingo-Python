from json import load

# Load game settings from the JSON file
with open('lingo/lingo_settings/lingo_settings.json', 'r') as settings_file:
    game_settings = load(settings_file)


###
### GETTERS
###


"""
    Returns the amount of teams playing the game.
"""
def get_amount_of_teams() -> int:
    amount_of_teams = game_settings.get("teams_amount", 1)
    return amount_of_teams

"""
    Returns the starting team ID.
"""
def get_starting_team_ID() -> int:
    starting_team_ID = game_settings.get("starting_team_ID", 0)
    return starting_team_ID