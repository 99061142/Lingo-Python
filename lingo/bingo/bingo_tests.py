import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from lingo.lingo_settings.lingo_settings_utils import get_starting_team_ID
from lingo.bingo.bingo_utils import get_randomized_bingo_board_for_team
from lingo.bingo.bingo_settings.bingo_settings_utils import get_bingo_board_size
from test_lib import report, test

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
        f"The bingo board should be of size {expected_size}x{expected_size}.",
        expected_size,
        expected_size,
    )
test_whether_bingo_board_is_correct_size()


if __name__ == "__main__":
    report()