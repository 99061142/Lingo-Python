from termcolor import colored

from app.bingo.bingo_settings.bingo_settings_utils import get_bingo_board_size, get_bingo_number_colors
from ..app_constants import GAP_BETWEEN_BOARD_COLUMNS
from ..teams_data import teams_data
from random import choice
from typing import List


###
### GETTERS
###


"""
    Returns a list of even numbers within the given range
"""
def get_even_numbers_list(start: int, end: int) -> List[int]:
    even_numbers = []
    
    # If the start isn't even, we add 1 to make it even
    start = start if start % 2 == 0 else start + 1
    
    for number in range(start, end + 1, 2):
        even_numbers.append(number)
    return even_numbers

"""
    Returns a list of uneven numbers within the given range
"""
def get_uneven_numbers_list(start: int, end: int) -> List[int]:
    uneven_numbers = []

    # If the start isn't uneven, we add 1 to make it uneven
    start = start if start % 2 != 0 else start + 1

    for number in range(start, end + 1, 2):
        uneven_numbers.append(number)
    return uneven_numbers

"""
    Returns a bingo board with randomized numbers for the specified team.
"""
def get_randomized_bingo_board_for_team(team_ID: int) -> List[List[int]]:
    # Hardcoded range for bingo numbers
    start = 1
    end = 99

    # If the ID of the team is even, we use even numbers for the bingo board.
    # Otherwise, we use uneven numbers.
    if team_ID % 2 == 0:
        available_numbers = get_even_numbers_list(start, end)
    else:
        available_numbers = get_uneven_numbers_list(start, end)

    # Create the bingo board with randomized numbers.
    bingo_board = []
    bingo_board_size = get_bingo_board_size()
    for _ in range(bingo_board_size):
        bingo_board_row = []
        for _ in range(bingo_board_size):
            number = choice(available_numbers)
            available_numbers.remove(number)
            bingo_board_row.append(number)
        bingo_board.append(bingo_board_row)

    return bingo_board

"""
    Returns the dictionary which holds the grabbed balls information by the specified team.
"""
def get_balls_grabbed_by_team(team_ID: int) -> dict:
    team_data = teams_data[team_ID]
    balls_grabbed = team_data["balls"]["grabbed"]
    return balls_grabbed

"""
    Returns the amount of color balls grabbed by the specified team.
"""
def get_amount_of_color_balls_grabbed_by_team(team_ID: int, color: str) -> int:
    balls_grabbed = get_balls_grabbed_by_team(team_ID)
    amount_of_color_balls_grabbed = balls_grabbed[color]
    return amount_of_color_balls_grabbed

"""
    Returns the set of filled positions on the bingo board for the specified team.
"""
def get_filled_positions_for_team(team_ID: int) -> set:
    team_data = teams_data[team_ID]
    bingo_board_data = team_data["bingoBoard"]
    filled_positions = bingo_board_data["filledPositions"]
    return filled_positions

"""
    Returns whether the bingo board has a horizontal line for the specified team.
"""
def bingo_board_has_horizontal_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    for row_index in range(bingo_board_size):
        horizontal_line_is_marked = True
        for col_index in range(bingo_board_size):
            position = (row_index, col_index)

            if position not in filled_positions:
                horizontal_line_is_marked = False
                break
        
        if horizontal_line_is_marked:
            return True
    
    return False

"""
    Returns whether the bingo board has a vertical line for the specified team.
"""
def bingo_board_has_vertical_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    for col_index in range(bingo_board_size):
        vertical_line_is_marked = True
        for row_index in range(bingo_board_size):
            position = (row_index, col_index)

            if position not in filled_positions:
                vertical_line_is_marked = False
                break
        
        if vertical_line_is_marked:
            return True
    
    return False

"""
    Returns whether the bingo board has a diagonal line for the specified team.
"""
def bingo_board_has_diagonal_line_for_team(team_ID: int) -> bool:
    filled_positions = get_filled_positions_for_team(team_ID)
    bingo_board_size = get_bingo_board_size()

    # Check top-left to bottom-right diagonal
    diagonal_line_is_marked = True
    for index in range(bingo_board_size):
        position = (index, index)
        if position not in filled_positions:
            diagonal_line_is_marked = False
            break
    if diagonal_line_is_marked:
        return True

    # Check top-right to bottom-left diagonal
    # We default the `diagonal_line_is_marked` variable again to True for the next check
    diagonal_line_is_marked = True
    for index in range(bingo_board_size):
        column_index = bingo_board_size - 1 - index
        position = (index, column_index)
        if position not in filled_positions:
            diagonal_line_is_marked = False
            break
    
    return diagonal_line_is_marked

"""
    Returns whether the bingo board has 1 or more lines marked for the specified team.
"""
def bingo_board_has_filled_line_for_team(team_ID: int) -> bool:
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

"""
    Returns the bingo board for the specified team.
    !Do note that this is a 2D list representing the bingo board.
    !This is not a stringified version of the bingo board for display purposes.
"""
def get_bingo_board_for_team(team_ID: int) -> List[List[int]]:
    team_data = teams_data[team_ID]
    bingo_board = team_data["bingoBoard"]["board"]
    return bingo_board

"""
    Returns the filled positions on the bingo board for the specified team.
"""
def get_filled_bingo_board_positions_for_team(team_ID: int) -> set:
    team_data = teams_data[team_ID]
    filled_positions = team_data["bingoBoard"]["filledPositions"]
    return filled_positions

"""
    Returns a stringified version of the bingo board for the specified team.
"""
def get_stringified_bingo_board_for_team(team_ID: int) -> str:
    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_bingo_board_positions_for_team(team_ID)
    bingo_board_size = get_bingo_board_size()

    stringified_board = ""
    for row_index in range(bingo_board_size):
        for col_index in range(bingo_board_size):
            number = bingo_board[row_index][col_index]

            # Center the number within the defined gap
            # E.g. if the GAP_BETWEEN_BOARD_COLUMNS is 2, 
            # * The number 7 would be formatted as " 7 "
            # * The 23, it would be "23 "
            # * And 100 would be "100"
            # What we see here is that it first centers the number in a field of width GAP_BETWEEN_BOARD_COLUMNS,
            # and if it increases the length of the number, it first adds spaces to the left until it reaches the width,
            # and then adds spaces to the right until it reaches the width.
            number_str = f"{number:^{GAP_BETWEEN_BOARD_COLUMNS}}"
            
            position = (row_index, col_index)
            if position in filled_positions:
                number_color = get_bingo_number_colors().get("marked")
            else:
                number_color = get_bingo_number_colors().get("unmarked")
            number_str = colored(number_str, number_color)
            
            stringified_board += f"{" " * GAP_BETWEEN_BOARD_COLUMNS}{number_str}{" " * GAP_BETWEEN_BOARD_COLUMNS}"

        stringified_board += "\n\n"

    return stringified_board

"""
    Returns a dictionary which holds the remaining balls information for the specified team.
"""
def get_remaining_balls_for_team(team_ID: int) -> dict:
    team_data = teams_data[team_ID]
    balls_remaining = team_data["balls"]["remaining"]
    return balls_remaining

"""
    Returns how many remanining color balls there are for the specified team, and color.
"""
def get_remaining_color_balls_for_team(team_ID: int, color: str) -> int:
    balls_remaining = get_remaining_balls_for_team(team_ID)
    remaining_color_balls = balls_remaining[color]
    return remaining_color_balls

"""
    Returns a list of remaining numbers on the bingo board for the specified team.
"""
def get_remaining_bingo_board_numbers_for_team(team_ID: int) -> List[int]:
    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_bingo_board_positions_for_team(team_ID)
    bingo_board_size = get_bingo_board_size()
    
    remaining_numbers = []
    for row_index in range(bingo_board_size):
        for col_index in range(bingo_board_size):
            position = (row_index, col_index)
            if position not in filled_positions:
                number = bingo_board[row_index][col_index]
                remaining_numbers.append(number)
    
    return remaining_numbers

"""
    Return a list which represents the bingo board pit for the specified team.
    It contains the remaining colored balls (red and green), as well as the remaining numbers on the specified team's bingo board.
"""
def get_available_bingo_board_pit_balls_for_team(team_ID: int) -> List:
    bingo_board_pit_balls = []
    
    # Add the remaining red balls
    remaining_red_balls_in_pit = get_remaining_color_balls_for_team(team_ID, "red")
    for _ in range(remaining_red_balls_in_pit):
        bingo_board_pit_balls.append("red")

    # Add the remaining green balls
    remaining_green_balls_in_pit = get_remaining_color_balls_for_team(team_ID, "green")
    for _ in range(remaining_green_balls_in_pit):
        bingo_board_pit_balls.append("green")

    # Add the remaining numbers on the bingo board
    remaining_numbers_in_pit = get_remaining_bingo_board_numbers_for_team(team_ID)
    for number in remaining_numbers_in_pit:
        bingo_board_pit_balls.append(number)

    return bingo_board_pit_balls

"""
    Returns whether the specified team has won the bingo game.
"""            
def has_team_won_bingo_game(team_ID: int) -> bool:
    # If the team has grabbed 3 or more green balls, they win the game.
    green_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "green")
    if green_balls_grabbed >= 3:
        return True
    
    # If the team has any line on their bingo board, they win the game.
    has_any_filled_lines_on_bingo_board = bingo_board_has_filled_line_for_team(team_ID)
    if has_any_filled_lines_on_bingo_board:
        return True
    
    return False

"""
    Returns whether the specified team has lost the bingo game.
"""            
def has_team_lost_bingo_game(team_ID: int) -> bool:
    # If the team has grabbed 3 or more red balls, they lose the bingo game.
    red_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "red")
    if red_balls_grabbed >= 3:
        return True
    
    return False


###
### SETTERS
###


"""
    Increases the amount of grabbed color balls for the specified team and color by 1.
"""
def increase_grabbed_color_balls_for_team(team_ID: int, color: str) -> None:
    balls_grabbed = get_balls_grabbed_by_team(team_ID)
    balls_grabbed[color] += 1

"""
    Decreases the amount of remaining color balls for the specified team and color by 1.
"""
def decrease_remaining_color_balls_for_team(team_ID: int, color: str) -> None:
    balls_remaining = get_remaining_balls_for_team(team_ID)
    balls_remaining[color] -= 1

"""
    Marks the grabbled number on the bingo board for the specified team.
"""
def mark_number_on_bingo_board(team_ID: int, grabbled_number: int) -> None:
    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_bingo_board_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    for row_index in range(bingo_board_size):
        for col_index in range(bingo_board_size):
            number = bingo_board[row_index][col_index]
            if number == grabbled_number:
                position = (row_index, col_index)
                filled_positions.add(position)
                return