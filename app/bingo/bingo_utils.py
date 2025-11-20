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
    board_size = 4 # This is the amount of rows AND columns
    bingo_board = []

    for _ in range(board_size):
        bingo_row = []
        for _ in range(board_size):
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