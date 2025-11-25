import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from lingo.teams_data import teams_data
from lingo.lingo_utils import initialize_teams_data
from test_lib import report, test
from lingo.lingo_settings.lingo_settings_utils import get_starting_team_ID
from lingo.bingo.bingo_utils import bingo_board_has_horizontal_line_for_team, bingo_board_has_vertical_line_for_team, get_even_numbers_list_from_range, get_odd_numbers_list_from_range, get_randomized_bingo_board_for_team, has_team_won_bingo_game, increase_grabbed_color_balls_for_team, mark_number_on_bingo_board_for_team, bingo_board_has_diagonal_line_for_team, unmark_number_on_bingo_board_for_team
from lingo.bingo.bingo_settings.bingo_settings_utils import get_bingo_board_size

"""
    Test whether the bingo board size constant is set to 5.
"""
def test_whether_bingo_board_is_correct_size():
    expected_size = get_bingo_board_size()

    starting_team_id = get_starting_team_ID()
    bingo_board = get_randomized_bingo_board_for_team(starting_team_id)

    # If the bingo board doesn't have the correct number of rows,
    # we report the error and return early.
    bingo_board_rows_amount = len(bingo_board)
    if bingo_board_rows_amount != expected_size:
        test(
            f"The bingo board should have {expected_size} rows. It currently has {bingo_board_rows_amount} rows.",
            expected_size,
            bingo_board_rows_amount,
        )
        return

    # If the bingo board doesn't have the correct number of columns,
    # we report the error and return early.
    bingo_board_columns_amount = len(bingo_board[0])  
    if bingo_board_columns_amount != expected_size:
        test(
            f"The bingo board should have {expected_size} columns. It currently has {bingo_board_columns_amount} columns.",
            expected_size,
            bingo_board_columns_amount,
        )
        return

    # If we reach this point, the bingo board has the correct size
    # In this case, we report the test as successful
    test(
        f"The bingo board should be of size {expected_size}.",
        expected_size,
        expected_size,
    )
test_whether_bingo_board_is_correct_size()

"""
    Test whether the get_even_numbers_list_from_range function returns only a list of even numbers within a specified range.
"""
def test_whether_bingo_board_contains_only_even_numbers():
    start = 1
    end = 10
    numbers = get_even_numbers_list_from_range(start, end)
    expected_numbers = [2, 4, 6, 8, 10]

    test(
        f"The list of numbers from {start} to {end} should contain only even numbers when calling the `get_even_numbers_list_from_range` function.",
        expected_numbers,
        numbers,
    )
test_whether_bingo_board_contains_only_even_numbers()

"""
    Test whether the get_odd_numbers_list_from_range function returns only a list of odd numbers within a specified range.
"""
def test_whether_bingo_board_contains_only_odd_numbers():
    start = 1
    end = 10
    numbers = get_odd_numbers_list_from_range(start, end)
    expected_numbers = [1, 3, 5, 7, 9]
    test(
        f"The list of numbers from {start} to {end} should contain only odd numbers when calling the `get_odd_numbers_list_from_range` function.",
        expected_numbers,
        numbers,
    )
test_whether_bingo_board_contains_only_odd_numbers()

"""
    Test whether the bingo_board_has_horizontal_line_for_team function correctly identifies a horizontal line on the bingo board for the specified team.
"""
def test_whether_bingo_board_has_horizontal_line():
    # First we initialize the teams data to ensure we have the bingo board to work with
    initialize_teams_data()
    
    team_ID = get_starting_team_ID()

    # Check for each possible horizontal line
    bingo_board_size = get_bingo_board_size()
    for row_index in range(bingo_board_size):
        marked_numbers = []
        for col_index in range(bingo_board_size):
            number_to_mark = teams_data[team_ID]["bingoBoard"]["board"][row_index][col_index]
            
            mark_number_on_bingo_board_for_team(team_ID, number_to_mark)
            marked_numbers.append(number_to_mark)

        result = bingo_board_has_horizontal_line_for_team(team_ID)
        
        # If the result is indicating that there is no horizontal line, we break out of the loop early.
        # We do this so that we can report which specific horizontal line check failed.
        if not result:
            break
        
        # Unmark the numbers for the next iteration
        for marked_number in marked_numbers:
            unmark_number_on_bingo_board_for_team(team_ID, marked_number)

    if not result:
        test_message = f"The bingo board should return that the user has a horizontal line after marking all numbers within 1 of the possible horizontal lines (row {row_index + 1}).",
    else:
        test_message = "The bingo board should return that the user has a horizontal line after marking all numbers within any of the possible horizontal lines."
    
    expected = True
    test(
        test_message,
        expected,
        result,
    )


test_whether_bingo_board_has_horizontal_line()

"""
    Test whether the bingo_board_has_horizontal_line_for_team function correctly identifies a vertical line on the bingo board for the specified team.
"""
def test_whether_bingo_board_has_vertical_line():
    # First we initialize the teams data to ensure we have the bingo board to work with
    initialize_teams_data()
    
    team_ID = get_starting_team_ID()

    # Check for each possible vertical line
    bingo_board_size = get_bingo_board_size()
    for row_index in range(bingo_board_size):
        marked_numbers = []
        for col_index in range(bingo_board_size):
            number_to_mark = teams_data[team_ID]["bingoBoard"]["board"][col_index][row_index]
            
            mark_number_on_bingo_board_for_team(team_ID, number_to_mark)
            marked_numbers.append(number_to_mark)

        result = bingo_board_has_vertical_line_for_team(team_ID)
        
        # If the result is indicating that there is no vertical line, we break out of the loop early.
        # We do this so that we can report which specific vertical line check failed.
        if not result:
            break
        
        # Unmark the numbers for the next iteration
        for marked_number in marked_numbers:
            unmark_number_on_bingo_board_for_team(team_ID, marked_number)

    if not result:
        test_message = f"The bingo board should return that the user has a vertical line after marking all numbers within 1 of the possible vertical lines (column {row_index + 1}).",
    else:
        test_message = "The bingo board should return that the user has a vertical line after marking all numbers within any of the possible vertical lines."

    expected = True
    test(
        test_message,
        expected,
        result,
    )

test_whether_bingo_board_has_vertical_line()

"""
    Test whether the bingo_board_has_diagonal_line_for_team function correctly identifies a diagonal line on the bingo board for the specified team.
"""
def test_whether_bingo_board_has_diagonal_line():
    # First we initialize the teams data to ensure we have the bingo board to work with
    initialize_teams_data()
    
    team_ID = get_starting_team_ID()
    board_size = get_bingo_board_size()

    # Mark the numbers on the diagonal from top-right to bottom-left
    for row_index in range(board_size):
        col_index = board_size - 1 - row_index
        number_to_mark = teams_data[team_ID]["bingoBoard"]["board"][row_index][col_index]
        mark_number_on_bingo_board_for_team(team_ID, number_to_mark)
    result = bingo_board_has_diagonal_line_for_team(team_ID)

    expected = True

    if not result:
        test(
            "The bingo board should return that the team has a diagonal line after marking all numbers from top-right to bottom-left.",
            expected,
            result,
        )
        return

    # Now we mark the numbers on the diagonal from top-left to bottom-right
    for i in range(board_size):
        number_to_mark = teams_data[team_ID]["bingoBoard"]["board"][i][i]
        mark_number_on_bingo_board_for_team(team_ID, number_to_mark)
    result = bingo_board_has_diagonal_line_for_team(team_ID)
    
    if not result:
        test(
            "The bingo board should return that the team has a diagonal line after marking all numbers from top-left to bottom-right.",
            expected,
            result,
        )
        return

    test(
        "The bingo board should return that the team has a diagonal line after marking all numbers from top-left to bottom-right OR top-right to bottom-left.",
        expected,
        result,
    )
test_whether_bingo_board_has_diagonal_line()

"""
    Test whether the function which returns if a team won the bingo game works correctly.
"""
def test_whether_team_has_won_bingo_game():
    # First we initialize the teams data to ensure we have the team data to work with
    initialize_teams_data()
    
    team_ID = get_starting_team_ID()
    expected = True

    bingo_board_size = get_bingo_board_size()
    marked_numbers = []

    # We simulate the team winning by marking all numbers in the first row
    for col_index in range(bingo_board_size):
        number_to_mark = teams_data[team_ID]["bingoBoard"]["board"][0][col_index]
        mark_number_on_bingo_board_for_team(team_ID, number_to_mark)

    result = has_team_won_bingo_game(team_ID)
    if not result:
        test(
            "The team should have won the bingo game after marking all numbers in a horizontal line.",
            expected,
            result,
        )

    # Unmark the numbers for the next test.
    for marked_number in marked_numbers:
        unmark_number_on_bingo_board_for_team(team_ID, marked_number)

    # Simulate the team having 3 green balls
    for _ in range(3):
        increase_grabbed_color_balls_for_team(team_ID, "green")

    result = has_team_won_bingo_game(team_ID)

    if not result:
        test(
            "The team should have won the bingo game after grabbing 3 green balls.",
            expected,
            result,
        )
        return

    test(
        "The team should have won the bingo game if they have a marked line on their bingo board OR have grabbed 3 green balls.",
        expected,
        result,
    )
test_whether_team_has_won_bingo_game()


# Run the report when this file is executed directly instead of within the tests.py file
if __name__ == "__main__":
    report()