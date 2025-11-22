from test_lib import test
from .lingo_settings.lingo_settings_utils import get_amount_of_teams
from .teams_data import teams_data
from .lingo_utils import initialize_teams_data, remove_teams_data, remove_teams_data, set_winning_team

# Run all lingo-related tests
import lingo.bingo.bingo_tests

# Run all wordle-related tests
import lingo.wordle.wordle_tests

# Run all lingo-related tests

"""
    Test whether the teams data is initialized with the correct number of teams.
"""
def test_initialize_teams_data_function():
    # Initialize the teams data
    initialize_teams_data()

    result = len(teams_data)
    expected = get_amount_of_teams()

    test(
        f"The initial teams data should contain {expected} teams after initialization.",
        expected,
        result,
    )
test_initialize_teams_data_function()

"""
    Test whether if we remove the teams data, the teams data becomes empty.
"""
def test_remove_teams_data_function():
    # First we initialize the teams data to ensure there is data to remove
    initialize_teams_data()

    # Now we remove the teams data to test if it becomes empty
    remove_teams_data()

    result = len(teams_data)
    expected = 0

    test(
        f"After removing the teams data, the teams data should be empty.",
        expected,
        result,
    )
test_remove_teams_data_function()


"""
    Test whether setting a specified team as the winning team updates the teams data correctly.
"""
def test_setting_winning_team():
    # First we initialize the teams data to ensure there is data to update
    initialize_teams_data()

    # Set team 0 as the winning team
    winning_team_ID = 0
    set_winning_team(winning_team_ID)

    result = teams_data[winning_team_ID]["hasWon"]
    expected = True

    test(
        f"When setting team {winning_team_ID} as the winning team, their team data 'hasWon' value should be True.",
        expected,
        result,
    )
test_setting_winning_team()