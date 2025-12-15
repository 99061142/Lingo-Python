from test_lib import test
from .teams_data import teams_data
from .lingo_utils import get_next_team_ID, has_team_won_lingo_game, has_team_lost_lingo_game, get_winning_team_ID, get_losing_team_ID, initialize_teams_data, remove_teams_data, set_winning_team, set_losing_team, get_amount_of_teams
from .lingo_settings.lingo_settings_utils import get_starting_team_ID

def test_get_next_team_ID() -> None:
    """
        Test whether the function which gets the next team ID works in a circular manner works correctly.
    """

    amount_of_teams = get_amount_of_teams()
    for team_ID in range(amount_of_teams):
        expected_next_team_ID = (team_ID + 1) % amount_of_teams
        actual_next_team_ID = get_next_team_ID(team_ID)
        test(
            f"Getting the next team ID when the current team ID is {team_ID} (with a total of {amount_of_teams} teams) should return team ID {expected_next_team_ID}.",
            expected_next_team_ID,
            actual_next_team_ID,
        )
test_get_next_team_ID()

def test_has_team_won_lingo_game() -> None:
    """
        Test whether the function which checks if a team has won the Lingo game works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    amount_of_teams = get_amount_of_teams()
    if amount_of_teams < 2:
        test(
            "Not enough teams to run the 'has_team_won_lingo_game' test. At least 2 teams are required.",
            True,
            False,
        )
        
        # Remove the teams data after the test to reset the state for other tests
        remove_teams_data()
        return

    # We set the team that will start the Lingo game as the winning team for testing purposes
    winning_team_ID = get_starting_team_ID()
    set_winning_team(winning_team_ID)

    for team_ID in range(amount_of_teams):
        expected = (team_ID == winning_team_ID)
        result = has_team_won_lingo_game(team_ID)

        test(
            f"Checking whether team {team_ID} has won the Lingo game should return {expected} when the winning team is team {winning_team_ID}.",
            expected,
            result,
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()

test_has_team_won_lingo_game()

def test_has_team_lost_lingo_game() -> None:
    """
        Test whether the function which checks if a team has lost the Lingo game works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    amount_of_teams = get_amount_of_teams()
    if amount_of_teams < 2:
        test(
            "Not enough teams to run the 'has_team_lost_lingo_game' test. At least 2 teams are required.",
            True,
            False,
        )

        # Remove the teams data after the test to reset the state for other tests
        remove_teams_data()
        return

    # We set the team that will start the Lingo game as the losing team for testing purposes
    losing_team_ID = get_starting_team_ID()
    set_losing_team(losing_team_ID)

    for team_ID in range(amount_of_teams):
        expected = (team_ID == losing_team_ID)
        result = has_team_lost_lingo_game(team_ID)

        test(
            f"Checking whether team {team_ID} has lost the Lingo game should return {expected} when the losing team is team {losing_team_ID}.",
            expected,
            result,
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_lost_lingo_game()

def test_get_winning_team_ID() -> None:
    """
        Test whether the function which gets the winning team ID works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    amount_of_teams = get_amount_of_teams()
    if amount_of_teams < 2:
        test(
            "Not enough teams to run the 'get_winning_team_ID' test. At least 2 teams are required.",
            True,
            False,
        )

        # Remove the teams data after the test to reset the state for other tests
        remove_teams_data()
        return

    # We set the team that will start the Lingo game as the winning team for testing purposes
    winning_team_ID = get_starting_team_ID()
    set_winning_team(winning_team_ID)

    expected = winning_team_ID
    result = get_winning_team_ID()

    test(
        f"Getting the winning team ID should return {expected} when the winning team is team {winning_team_ID}.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_winning_team_ID()

def test_get_losing_team_ID() -> None:
    """
        Test whether the function which gets the losing team ID works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    amount_of_teams = get_amount_of_teams()
    if amount_of_teams < 2:
        test(
            "Not enough teams to run the 'get_losing_team_ID' test. At least 2 teams are required.",
            True,
            False,
        )

        # Remove the teams data after the test to reset the state for other tests
        remove_teams_data()
        return

    # We set the team that will start the Lingo game as the losing team for testing purposes
    losing_team_ID = get_starting_team_ID()
    set_losing_team(losing_team_ID)

    expected = losing_team_ID
    result = get_losing_team_ID()

    test(
        f"Getting the losing team ID should return {expected} when the losing team is team {losing_team_ID}.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_losing_team_ID()

def test_remove_teams_data() -> None:
    """
        Test whether if we remove the teams data, the teams data becomes empty.
    """

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
test_remove_teams_data()

def test_initialize_teams_data() -> None:
    """
        Test whether the initialize_teams_data function correctly initializes the teams data.
    """

    # Initialize the teams data
    initialize_teams_data()

    result = len(teams_data)
    expected = get_amount_of_teams()

    test(
        f"The initial teams data should contain {expected} teams after initialization.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_initialize_teams_data()

def test_setting_winning_team() -> None:
    """
        Test whether setting a specified team as the winning team updates the teams data correctly.
    """

    # First we initialize the teams data to ensure there is data to update
    initialize_teams_data()

    # We set the team that will start the Lingo game as the winning team for testing purposes
    winning_team_ID = get_starting_team_ID()
    set_winning_team(winning_team_ID)

    result = teams_data[winning_team_ID]["hasWon"]
    expected = True

    test(
        f"When setting team {winning_team_ID} as the winning team, their team data 'hasWon' value should be True.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_setting_winning_team()

def test_setting_losing_team() -> None:
    """
        Test whether setting a specified team as the losing team updates the teams data correctly.
    """

    # First we initialize the teams data to ensure there is data to update
    initialize_teams_data()

    # We set the team that will start the Lingo game as the losing team for testing purposes
    losing_team_ID = get_starting_team_ID()
    set_losing_team(losing_team_ID)

    result = teams_data[losing_team_ID]["hasLost"]
    expected = True

    test(
        f"When setting team {losing_team_ID} as the losing team, their team data 'hasLost' value should be True.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_setting_losing_team()

def test_get_amount_of_teams() -> None:
    """
        Test whether the function which gets the amount of teams works correctly.
    """

    result = get_amount_of_teams()
    expected = 2

    test(
        f"The amount of teams should be {expected} by default.",
        expected,
        result,
    )
test_get_amount_of_teams()

def test_get_starting_team_ID() -> None:
    """
        Test whether the function which gets the starting team ID works correctly.
    """

    result = get_starting_team_ID()
    expected = 0
    
    test(
        f"The starting team ID should be {expected} by default.",
        expected,
        result,
    )
test_get_starting_team_ID()