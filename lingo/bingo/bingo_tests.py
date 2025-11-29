from test_lib import test
from ..lingo_utils import get_amount_of_teams, initialize_teams_data, remove_teams_data, get_next_team_ID
from ..lingo_settings.lingo_settings_utils import get_starting_team_ID
from .bingo_settings.bingo_settings_utils import *
from .bingo_utils import *

def test_get_bingo_board_size() -> None:
    """
        Test whether the function which returns the size of the Bingo board works correctly.
    """

    expected_board_size = 4
    actual_board_size = get_bingo_board_size()

    # Test whether the actual bingo board size matches the expected size
    test(
        f"The bingo board size should be {expected_board_size}.",
        expected_board_size,
        actual_board_size
    )
test_get_bingo_board_size()

def test_get_bingo_number_colors() -> None:
    """
        Test whether the function which returns the bingo number colors works correctly.
    """

    expected_number_colors = {
        "marked": "green",
        "unmarked": "white"
    }
    actual_number_colors = get_bingo_number_colors()

    for state in expected_number_colors:
        # Test whether the actual color for each state matches the expected color
        expected_color = expected_number_colors[state]
        actual_color = actual_number_colors[state]
        
        test(
            f"The color for '{state}' Bingo numbers should be '{expected_color}'.",
            expected_color,
            actual_color
        )
test_get_bingo_number_colors()

def test_get_maximum_grabs_per_round() -> None:
    """
        Test whether the function which returns the maximum grabs per round works correctly.
    """

    expected_max_grabs = 2
    actual_max_grabs = get_maximum_grabs_per_round()

    # Test whether the actual maximum grabs per round matches the expected value
    test(
        f"The maximum grabs per round should be {expected_max_grabs}.",
        expected_max_grabs,
        actual_max_grabs
    )
test_get_maximum_grabs_per_round()

def test_get_even_numbers_list_from_range() -> None:
    """
        Test whether the function which returns a list of even numbers from a specified range works correctly.
    """

    start = 1
    end = 10
    expected_even_numbers = [2, 4, 6, 8, 10]
    actual_even_numbers = get_even_numbers_list_from_range(start, end)

    # Test whether the actual list of even numbers matches the expected list
    test(
        f"The even numbers from {start} to {end} should be {expected_even_numbers}.",
        expected_even_numbers,
        actual_even_numbers
    )
test_get_even_numbers_list_from_range()

def test_get_odd_numbers_list_from_range() -> None:
    """
        Test whether the function which returns a list of odd numbers from a specified range works correctly.
    """

    start = 0
    end = 10
    expected_odd_numbers = [1, 3, 5, 7, 9]
    actual_odd_numbers = get_odd_numbers_list_from_range(start, end)

    # Test whether the actual list of odd numbers matches the expected list
    test(
        f"The odd numbers from {start} to {end} should be {expected_odd_numbers}.",
        expected_odd_numbers,
        actual_odd_numbers
    )
test_get_odd_numbers_list_from_range()

def test_get_randomized_bingo_board_for_team() -> None:
    """
        Test whether the function which returns a randomized bingo board for a team works correctly.
    """

    team_amount = get_amount_of_teams()
    for team_ID in range(team_amount):
        bingo_board = get_randomized_bingo_board_for_team(team_ID)
        board_size = get_bingo_board_size()

        # Test whether the bingo board has the correct dimensions
        test(
            f"Bingo board for team {team_ID + 1} should have dimensions {board_size}x{board_size}.",
            (board_size, board_size),
            (len(bingo_board), len(bingo_board[0]))
        )

        # Test whether the numbers for team ID 0 has even numbers only, and for team ID 1 has odd numbers only
        expect_even_numbers = (team_ID % 2 == 0)
        result_even_numbers = True
        for row in bingo_board:
            for number in row:
                if expect_even_numbers and (number % 2 != 0):
                    result_even_numbers = False
                elif not expect_even_numbers and (number % 2 == 0):
                    result_even_numbers = False
        test(
            f"Bingo board for team {team_ID + 1} should have {'even' if expect_even_numbers else 'odd'} numbers only.",
            True,
            result_even_numbers
        )
test_get_randomized_bingo_board_for_team()


def test_get_balls_grabbed_by_team() -> None:
    """
        Test whether the function which returns the balls grabbed by a team works correctly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being team data available.
    initialize_teams_data()

    # Add 2 red balls and 1 green ball to each team's grabbed balls for testing
    team_ID = get_starting_team_ID()
    grabbed_balls = teams_data[team_ID]["balls"]["grabbed"]
    grabbed_balls["red"] = 2
    grabbed_balls["green"] = 1

    # Test whether if a team has already grabbed some colored balls, the function returns the correct amount
    expected_grabbed_balls = {
        "red": 2,
        "green": 1
    }
    actual_grabbed_balls = get_balls_grabbed_by_team(team_ID)
    for key in expected_grabbed_balls:
        expected_value = expected_grabbed_balls[key]
        actual_value = actual_grabbed_balls[key]
        test(
            f"When a team has already grabbed {expected_value} {key} colored ball(s), the function should return the correct amount.",
            expected_value,
            actual_value
        )

    # Test whether the default values for the grabbed balls are 0
    team_ID = get_next_team_ID(team_ID)
    expected_grabbed_balls = {
        "red": 0,
        "green": 0
    }
    actual_grabbed_balls = get_balls_grabbed_by_team(team_ID)
    for key in expected_grabbed_balls:
        expected_value = expected_grabbed_balls[key]
        actual_value = actual_grabbed_balls[key]
        test(
            f"The default value for the {key} colored balls should be 0",
            expected_value,
            actual_value
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_balls_grabbed_by_team()

def test_get_amount_of_color_balls_grabbed_by_team() -> None:
    """
        Test whether the function which returns the amount of colored balls grabbed by a team works correctly.
        Do note that this also tests the increase_grabbed_color_balls_for_team function as well, since we need to increase some balls to test the amount function properly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being team data available.
    initialize_teams_data()

    # Add 3 red balls and 2 green balls to the starting team's grabbed balls for testing purposes
    team_ID = get_starting_team_ID()
    for _ in range(3):
        increase_grabbed_color_balls_for_team(team_ID, "red")
    for _ in range(2):
        increase_grabbed_color_balls_for_team(team_ID, "green")

    # Test whether if a team has already grabbed some colored balls, the function returns the correct amount
    expected_red_balls = 3
    actual_red_balls = get_amount_of_color_balls_grabbed_by_team(team_ID, "red")
    test(
        f"When a team has already grabbed {expected_red_balls} red colored balls, the function should return the correct amount.",
        expected_red_balls,
        actual_red_balls
    )

    expected_green_balls = 2
    actual_green_balls = get_amount_of_color_balls_grabbed_by_team(team_ID, "green")
    test(
        f"When a team has already grabbed {expected_green_balls} green colored balls, the function should return the correct amount.",
        expected_green_balls,
        actual_green_balls
    )

    # Test whether the default values for the grabbed balls are 0
    team_ID = get_next_team_ID(team_ID)
    expected_red_balls = 0
    actual_red_balls = get_amount_of_color_balls_grabbed_by_team(team_ID, "red")
    test(
        f"The default value for the red colored balls should be 0",
        expected_red_balls,
        actual_red_balls
    )

    expected_green_balls = 0
    actual_green_balls = get_amount_of_color_balls_grabbed_by_team(team_ID, "green")
    test(
        f"The default value for the green colored balls should be 0",
        expected_green_balls,
        actual_green_balls
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_amount_of_color_balls_grabbed_by_team()

def test_get_remaining_balls_for_team() -> None:
    """
        Test whether the function which returns the remaining balls for a team works correctly.
        Do note that this also tests the decrease_remaining_color_balls_for_team function as well, since we need to decrease some balls to test the remaining balls function properly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being team data available.
    initialize_teams_data()

    # Test whether the default values for the remaining balls are correct
    team_ID = get_starting_team_ID()
    expected_remaining_balls = {
        "red": 3,
        "green": 3
    }
    actual_remaining_balls = get_remaining_balls_for_team(team_ID)
    for key in expected_remaining_balls:
        expected_value = expected_remaining_balls[key]
        actual_value = actual_remaining_balls[key]
        test(
            f"The default value for the remaining {key} colored balls should be {expected_value}",
            expected_value,
            actual_value
        )

    # Test if the function works correctly after some balls have been grabbed
    grabbed_balls = teams_data[team_ID]["balls"]["grabbed"]
    for _ in range(2):
        decrease_remaining_color_balls_for_team(team_ID, "red")
        grabbed_balls["red"] += 1
        expected_remaining_balls["red"] -= 1
    for _ in range(1):
        decrease_remaining_color_balls_for_team(team_ID, "green")
        grabbed_balls["green"] += 1
        expected_remaining_balls["green"] -= 1

    actual_remaining_balls = get_remaining_balls_for_team(team_ID)
    for key in expected_remaining_balls:
        expected_value = expected_remaining_balls[key]
        actual_value = actual_remaining_balls[key]
        test(
            f"After some balls have been grabbed, the remaining {key} colored balls should be {expected_value}",
            expected_value,
            actual_value
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_remaining_balls_for_team()

def test_get_available_bingo_board_pit_balls_for_team() -> None:
    """
        Test whether the function which returns the available bingo board pit balls for a team works correctly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being team data available.
    initialize_teams_data()

    team_ID = get_starting_team_ID()


    initial_remaining_colored_balls = get_remaining_balls_for_team(team_ID)
    expected_balls = []
    for color, amount in initial_remaining_colored_balls.items():
        for _ in range(amount):
            expected_balls.append(color)
    
    bingo_board = get_bingo_board_for_team(team_ID)
    for row in bingo_board:
        for number in row:
            expected_balls.append(number)

    # Test whether the available bingo board pit balls for the team matches the expected balls if we haven't grabbed any balls yet
    actual_balls = get_available_bingo_board_pit_balls_for_team(team_ID)
    test(
        f"The available bingo board pit balls for team {team_ID + 1} should include the remaining colored balls and all numbers on the bingo board when no balls have been grabbed yet.",
        expected_balls,
        actual_balls
    )


    # Test whether the available bingo board pit balls for the team updates correctly after some balls have been grabbed
    # Grab 1 red ball and 1 number from the bingo board
    decrease_remaining_color_balls_for_team(team_ID, "red")
    number_to_mark = bingo_board[0][0]
    mark_number_on_bingo_board_for_team(team_ID, number_to_mark)

    expected_balls.remove("red")
    expected_balls.remove(number_to_mark)
    test(
        f"After grabbing a red ball and marking a number on the bingo board, the available bingo board pit balls for team {team_ID + 1} should update correctly.",
        expected_balls,
        get_available_bingo_board_pit_balls_for_team(team_ID)
    )


    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_available_bingo_board_pit_balls_for_team()

def test_has_team_won_bingo_game() -> None:
    """
        Test whether the function which checks if a team has won the Bingo game works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    bingo_win_conditions = get_bingo_win_conditions()
    
    # Test whether the default state is that the team hasn't won yet
    team_ID = get_starting_team_ID()
    expected_has_won = False
    actual_has_won = has_team_won_bingo_game(team_ID)
    test(
        f"By default, team {team_ID + 1} should not have won the Bingo game yet.",
        expected_has_won,
        actual_has_won
    )

    # Test whether if we set the team as having the required green balls grabbed to win, the function returns that they have won
    for _ in range(bingo_win_conditions["green_balls_grabbed"]):
        increase_grabbed_color_balls_for_team(team_ID, "green")
    expected_has_won = True
    actual_has_won = has_team_won_bingo_game(team_ID)
    test(
        f"After grabbing the required green balls, team {team_ID + 1} should have won the Bingo game.",
        expected_has_won,
        actual_has_won
    )
    
    # Reset the grabbed green balls for further testing
    teams_data[team_ID]["balls"]["grabbed"]["green"] = 0


    # Test whether if we fill enough lines on the bingo board for the team to win, the function returns that they have won
    lines_needed_to_win = bingo_win_conditions["lines_needed"]
    bingo_board_size = get_bingo_board_size()

    # Fill a single line on the bingo board for the team (top-left to top-right)
    for col in range(bingo_board_size):
        teams_data[team_ID]["bingoBoard"]["filledPositions"].add((0, col))

    team_has_won = has_team_won_bingo_game(team_ID)
    test(
        f"After filling 1 line on the bingo board, team {team_ID + 1} should have won the Bingo game if only 1 line is needed to win.",
        (lines_needed_to_win == 1),
        team_has_won
    )


    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_won_bingo_game()

def test_has_team_lost_bingo_game() -> None:
    """
        Test whether the function which checks if a team has lost the Bingo game works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    bingo_lose_conditions = get_bingo_lose_conditions()
    
    # Test whether the default state is that the team hasn't lost yet
    team_ID = get_starting_team_ID()
    expected_has_lost = False
    team_has_lost = has_team_lost_bingo_game(team_ID)
    test(
        f"By default, team {team_ID + 1} should not have lost the Bingo game yet.",
        expected_has_lost,
        team_has_lost
    )

    # Test whether if we set the team as having the required red balls grabbed to lose, the function returns that they have lost
    for _ in range(bingo_lose_conditions["red_balls_grabbed"]):
        increase_grabbed_color_balls_for_team(team_ID, "red")
    expected_has_lost = True
    team_has_lost = has_team_lost_bingo_game(team_ID)
    test(
        f"After grabbing the required red balls, team {team_ID + 1} should have lost the Bingo game.",
        expected_has_lost,
        team_has_lost
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_lost_bingo_game()

def test_mark_number_on_bingo_board_for_team() -> None:
    """
        Test whether the function which marks a number on the bingo board for a team works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    team_ID = get_starting_team_ID()
    bingo_board = get_bingo_board_for_team(team_ID)

    # We pick a number from the bingo board to mark
    number_to_mark = bingo_board[0][0]

    # Mark the number on the bingo board for the team
    mark_number_on_bingo_board_for_team(team_ID, number_to_mark)

    # Test whether the position of the marked number is in the filled positions for the team
    filled_positions = get_filled_positions_for_team(team_ID)
    expected_filled_position = (0, 0)
    test(
        f"After marking the number {number_to_mark} on the bingo board for team {team_ID + 1}, its position {expected_filled_position} should be in the filled positions set.",
        True,
        (expected_filled_position in filled_positions)
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_mark_number_on_bingo_board_for_team()

def test_get_bingo_board_filled_vertical_lines_amount_for_team() -> None:
    """
        Test whether the function which checks if a vertical line is filled on the bingo board for a team works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    team_ID = get_starting_team_ID()
    bingo_board_size = get_bingo_board_size()

    # FIll the vertical lines one by one and test if the function detects them correctly
    for col in range(bingo_board_size):
        # Fill the vertical line at the current column
        for row in range(bingo_board_size):
            teams_data[team_ID]["bingoBoard"]["filledPositions"].add((row, col))

        # Test whether the function detects the filled vertical line correctly
        expected_amount_of_lines_filled = 1
        amount_of_lines_filled = get_bingo_board_filled_vertical_lines_amount_for_team(team_ID)
        test(
            f"After filling the vertical line at column {col} on the bingo board for team {team_ID + 1}, the function should detect it as filled.",
            expected_amount_of_lines_filled,
            amount_of_lines_filled
        )

        # Clear the filled positions for the next iteration
        teams_data[team_ID]["bingoBoard"]["filledPositions"].clear()

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_bingo_board_filled_vertical_lines_amount_for_team()

def test_get_bingo_board_filled_horizontal_lines_amount_for_team() -> None:
    """
        Test whether the function which checks if a horizontal line is filled on the bingo board for a team works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    team_ID = get_starting_team_ID()
    bingo_board_size = get_bingo_board_size()

    # FIll the horizontal lines one by one and test if the function detects them correctly
    for row in range(bingo_board_size):
        # Fill the horizontal line at the current row
        for col in range(bingo_board_size):
            teams_data[team_ID]["bingoBoard"]["filledPositions"].add((row, col))

        # Test whether the function detects the filled horizontal line correctly
        expected_amount_of_lines_filled = 1
        amount_of_lines_filled = get_bingo_board_filled_horizontal_lines_amount_for_team(team_ID)
        test(
            f"After filling the horizontal line at row {row} on the bingo board for team {team_ID + 1}, the function should detect it as filled.",
            expected_amount_of_lines_filled,
            amount_of_lines_filled
        )

        # Clear the filled positions for the next iteration
        teams_data[team_ID]["bingoBoard"]["filledPositions"].clear()

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_bingo_board_filled_horizontal_lines_amount_for_team()

def test_get_bingo_board_filled_diagonal_lines_amount_for_team() -> None:
    """
        Test whether the function which checks if a diagonal line is filled on the bingo board for a team works correctly.
    """

    # First we initialize the teams data to ensure there is data to check
    initialize_teams_data()

    team_ID = get_starting_team_ID()
    bingo_board_size = get_bingo_board_size()

    # Fill the top-left to bottom-right diagonal line
    for i in range(bingo_board_size):
        teams_data[team_ID]["bingoBoard"]["filledPositions"].add((i, i))

    # Test whether the function detects the filled top-left to bottom-right diagonal line correctly
    expected_amount_of_lines_filled = 1
    amount_of_lines_filled = get_bingo_board_filled_diagonal_lines_amount_for_team(team_ID)
    test(
        f"After filling the diagonal line from top-left to bottom-right on the bingo board for team {team_ID + 1}, the function should detect it as filled.",
        expected_amount_of_lines_filled,
        amount_of_lines_filled
    )

    # Clear the filled positions for the next test
    teams_data[team_ID]["bingoBoard"]["filledPositions"].clear()

    # Fill the top-right to bottom-left diagonal line
    for i in range(bingo_board_size):
        teams_data[team_ID]["bingoBoard"]["filledPositions"].add((i, bingo_board_size - 1 - i))

    # Test whether the function detects the filled top-right to bottom-left diagonal line correctly
    expected_amount_of_lines_filled = 1
    amount_of_lines_filled = get_bingo_board_filled_diagonal_lines_amount_for_team(team_ID)
    test(
        f"After filling the diagonal line from top-right to bottom-left on the bingo board for team {team_ID + 1}, the function should detect it as filled.",
        expected_amount_of_lines_filled,
        amount_of_lines_filled
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_bingo_board_filled_diagonal_lines_amount_for_team()