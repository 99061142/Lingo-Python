from termcolor import colored
from app.constants import BINGO_BOARD_SIZE, GAP_BETWEEN_LETTERS
from ..teams_data import teams_data
from random import choice
from typing import List

"""
    Returns a random number from the given list of numbers.
"""
def get_random_number(numbers: List[int]) -> int:
    if not numbers:
        raise ValueError("The list of numbers to select a random number with is empty.")

    random_number = choice(numbers)
    return random_number

"""
    Creates and returns a list of even numbers within the given range
"""
def create_even_numbers_list(start: int, end: int) -> List[int]:
    even_numbers = []
    
    # If the start isn't even, we add 1 to make it even
    start = start if start % 2 == 0 else start + 1
    
    for number in range(start, end + 1, 2):
        even_numbers.append(number)
    return even_numbers

"""
    Creates and returns a list of uneven numbers within the given range
"""
def create_uneven_numbers_list(start: int, end: int) -> List[int]:
    uneven_numbers = []

    # If the start isn't uneven, we add 1 to make it uneven
    start = start if start % 2 != 0 else start + 1

    for number in range(start, end + 1, 2):
        uneven_numbers.append(number)
    return uneven_numbers

"""
    Returns a 4x4 bingo board with randomized numbers for the given team_ID.
    The team_ID can only be 0 or 1 in our current implementation.
"""
def create_randomized_bingo_board(team_ID: int) -> List[List[int]]:
    # Hardcoded range for bingo numbers
    start = 1
    end = 100

    # Team 0 gets even numbers, team 1 gets uneven numbers
    if team_ID == 0:
        available_numbers = create_even_numbers_list(start, end)
    else:
        available_numbers = create_uneven_numbers_list(start, end)

    # Create and return the bingo board
    bingo_board = []
    for _ in range(BINGO_BOARD_SIZE):
        bingo_board_row = []
        for _ in range(BINGO_BOARD_SIZE):
            number = get_random_number(available_numbers)
            available_numbers.remove(number)
            bingo_board_row.append(number)
        bingo_board.append(bingo_board_row)

    return bingo_board

"""
    Returns the dictionary which holds the grabbed balls information for the given team_ID.
"""
def get_balls_grabbed(team_ID: int) -> dict:
    team_data = teams_data[team_ID]
    balls_grabbed = team_data["balls"]["grabbed"]
    return balls_grabbed

"""
    Returns the amount of green balls grabbed by the given team_ID.
"""
def get_amount_of_green_balls_grabbed(team_ID: int) -> int:
    balls_grabbed = get_balls_grabbed(team_ID)
    green_balls_grabbed = balls_grabbed["green"]
    return green_balls_grabbed

"""
    Returns the amount of red balls grabbed by the given team_ID.
"""
def get_amount_of_red_balls_grabbed(team_ID: int) -> int:
    balls_grabbed = get_balls_grabbed(team_ID)
    red_balls_grabbed = balls_grabbed["red"]
    return red_balls_grabbed

"""
    Returns the set of filled positions on the bingo board for the given team_ID.
"""
def get_filled_positions_for_team(team_ID: int) -> set:
    team_data = teams_data[team_ID]
    bingo_board_data = team_data["bingoBoard"]
    filled_positions = bingo_board_data["filledPositions"]
    return filled_positions

"""
    Returns whether the bingo board has a horizontal line for the given team_ID.
"""
def bingo_board_has_horizontal_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)

    for row_index in range(BINGO_BOARD_SIZE):
        horizontal_row_is_filled = True
        for col_index in range(BINGO_BOARD_SIZE):
            position = (row_index, col_index)

            if position not in filled_positions:
                horizontal_row_is_filled = False
                break
        
        if horizontal_row_is_filled:
            return True
    
    return False

"""
    Returns whether the bingo board has a vertical line for the given team_ID.
"""
def bingo_board_has_vertical_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)

    for col_index in range(BINGO_BOARD_SIZE):
        vertical_row_is_filled = True
        for row_index in range(BINGO_BOARD_SIZE):
            position = (row_index, col_index)

            if position not in filled_positions:
                vertical_row_is_filled = False
                break
        
        if vertical_row_is_filled:
            return True
    
    return False

"""
    Returns whether the bingo board has a diagonal line for the given team_ID.
"""
def bingo_board_has_diagonal_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)

    # Check top-left to bottom-right diagonal
    diagonal_row_is_filled = True
    for index in range(BINGO_BOARD_SIZE):
        position = (index, index)
        if position not in filled_positions:
            diagonal_row_is_filled = False
            break
    if diagonal_row_is_filled:
        return True

    # Check top-right to bottom-left diagonal
    # We default the `diagonal_row_is_filled` variable again to True for the next check
    diagonal_row_is_filled = True
    for index in range(BINGO_BOARD_SIZE):
        column_index = BINGO_BOARD_SIZE - 1 - index
        position = (index, column_index)
        if position not in filled_positions:
            diagonal_row_is_filled = False
            break
    
    return diagonal_row_is_filled

"""
    Returns whether the bingo board has 1 or more lines for the given team_ID.
"""
def bingo_board_has_line_for_team(team_ID: int) -> bool:
    has_horizontal_line = bingo_board_has_horizontal_line_for_team(team_ID)
    if has_horizontal_line:
        return True

    has_vertical_line = bingo_board_has_vertical_line_for_team(team_ID)
    if has_vertical_line:
        return True

    has_diagonal_line = bingo_board_has_diagonal_line_for_team(team_ID)
    if has_diagonal_line:
        return True

    return False

def get_bingo_board_for_team(team_ID: int) -> List[List[int]]:
    team_data = teams_data[team_ID]
    bingo_board = team_data["bingoBoard"]["board"]
    return bingo_board

def get_filled_bingo_board_positions_for_team(team_ID: int) -> set:
    team_data = teams_data[team_ID]
    filled_positions = team_data["bingoBoard"]["filledPositions"]
    return filled_positions

""""
    Returns a stringified version of the bingo board for the given team_ID.
"""
def get_stringified_bingo_board_for_team(team_ID: int) -> str:
    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_bingo_board_positions_for_team(team_ID)

    stringified_board = ""
    for row_index in range(BINGO_BOARD_SIZE):
        for col_index in range(BINGO_BOARD_SIZE):
            number = bingo_board[row_index][col_index]
            position = (row_index, col_index)

            # Center the number within the defined gap
            # E.g. if the GAP_BETWEEN_LETTERS is 2, 
            # * The number 7 would be formatted as " 7 "
            # * The 23, it would be "23 "
            # * And 100 would be "100"
            # What we see here is that it first centers the number in a field of width GAP_BETWEEN_LETTERS,
            # and if it increases the length of the number, it first adds spaces to the left until it reaches the width,
            # and then adds spaces to the right until it reaches the width.
            number_str = f"{number:^{GAP_BETWEEN_LETTERS}}"
            
            if position in filled_positions:
                number_str = colored(number_str, "green")
            
            stringified_board += f"{" " * GAP_BETWEEN_LETTERS}{number_str}{" " * GAP_BETWEEN_LETTERS}"

        stringified_board += "\n\n"

    return stringified_board