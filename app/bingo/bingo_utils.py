from app.constants import BINGO_BOARD_SIZE
from ..teams_data import teams_data
from random import choice
from typing import List

"""
    Returns a random number between 1 and 100 that is not in the unavailableNumbers list.
"""
def get_random_number(teamID: int, unavailableNumbers: List[int] = []) -> int:
    start = 1
    end = 100

    # Ensure that the team with the ID of 0 gets even numbers, and the team with the ID of 1 gets odd numbers
    while True:
        number = choice(range(start, end + 1))
        if number % 2 == teamID and number not in unavailableNumbers:
            return number

"""
    Returns a 4x4 bingo board with randomized numbers for the given teamID.
    The teamID can only be 0 or 1 in our current implementation.
"""
def create_randomized_bingo_board(teamID: int) -> List[List[int]]:
    unavailableNumbers = [] # Numbers the team already has on their board
    bingo_board = []

    for _ in range(BINGO_BOARD_SIZE):
        bingo_row = []
        for _ in range(BINGO_BOARD_SIZE):
            number = get_random_number(teamID, unavailableNumbers)
            unavailableNumbers.append(number)
            bingo_row.append(number)
        bingo_board.append(bingo_row)

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
        row_is_filled = True
        for col_index in range(BINGO_BOARD_SIZE):
            position = (row_index, col_index)

            if position not in filled_positions:
                row_is_filled = False
                break
        
        if row_is_filled:
            return True
    
    return False