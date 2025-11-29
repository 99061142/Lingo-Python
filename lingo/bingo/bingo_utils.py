from termcolor import colored
from random import choice
from typing import List
from .bingo_settings.bingo_settings_utils import get_bingo_board_size, get_bingo_lose_conditions, get_bingo_number_colors, get_bingo_win_conditions
from ..lingo_constants import GAP_BETWEEN_BOARD_COLUMNS
from ..teams_data import teams_data

###
### GETTERS
###

def get_even_numbers_list_from_range(start: int, end: int) -> List[int]:
    """
    Returns a list of even numbers within the given range
    """

    even_numbers = []
    
    # If the start isn't even, we add 1 to make it even
    start = start if start % 2 == 0 else start + 1
    
    for number in range(start, end + 1, 2):
        even_numbers.append(number)
    return even_numbers

def get_odd_numbers_list_from_range(start: int, end: int) -> List[int]:
    """
        Returns a list of odd numbers within the given range
    """

    odd_numbers = []

    # If the start isn't odd, we add 1 to make it odd
    start = start if start % 2 != 0 else start + 1

    for number in range(start, end + 1, 2):
        odd_numbers.append(number)
    return odd_numbers

def get_randomized_bingo_board_for_team(team_ID: int) -> List[List[int]]:
    """
        Returns a randomized bingo board for the specified team.
    """

    # Hardcoded range for bingo numbers
    start = 1
    end = 99

    # If the ID of the team is even, we use even numbers for the bingo board.
    # Otherwise, we use uneven numbers.
    if team_ID % 2 == 0:
        available_numbers = get_even_numbers_list_from_range(start, end)
    else:
        available_numbers = get_odd_numbers_list_from_range(start, end)

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

def get_balls_grabbed_by_team(team_ID: int) -> dict:
    """
        Returns a dictionary which holds the grabbed balls information for the specified team.
    """

    team_data = teams_data[team_ID]
    balls_grabbed = team_data["balls"]["grabbed"]
    return balls_grabbed

def get_amount_of_color_balls_grabbed_by_team(team_ID: int, color: str) -> int:
    """
        Returns the amount of color balls grabbed by the specified team.
    """

    balls_grabbed = get_balls_grabbed_by_team(team_ID)
    amount_of_color_balls_grabbed = balls_grabbed[color]
    return amount_of_color_balls_grabbed

def get_filled_positions_for_team(team_ID: int) -> set:
    """
        Returns the set of filled positions on the bingo board for the specified team.
    """

    team_data = teams_data[team_ID]
    bingo_board_data = team_data["bingoBoard"]
    filled_positions = bingo_board_data["filledPositions"]
    return filled_positions

def get_bingo_board_for_team(team_ID: int) -> List[List[int]]:
    """
        Returns the bingo board for the specified team.
        !Do note that this is a 2D list representing the bingo board.
        !This is not a stringified version of the bingo board for display purposes.
    """

    team_data = teams_data[team_ID]
    bingo_board = team_data["bingoBoard"]["board"]
    return bingo_board

def get_stringified_bingo_board_for_team(team_ID: int) -> str:
    """
        Returns a stringified version of the bingo board for the specified team.
    """

    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_positions_for_team(team_ID)
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

def has_team_won_bingo_game(team_ID: int) -> bool:
    """
        Returns whether the specified team has won the bingo game.
    """

    win_conditions = get_bingo_win_conditions()

    # If the team has grabbed the required amount of green balls, they win the game.
    green_balls_needed_to_win = win_conditions["green_balls_grabbed"]
    green_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "green")
    if green_balls_grabbed >= green_balls_needed_to_win:
        return True
    
    # If the team has filled enough lines on their bingo board, they win the game.
    amount_of_lines_filled_on_board = get_bingo_board_total_filled_lines_amount_for_team(team_ID)
    if amount_of_lines_filled_on_board >= win_conditions["lines_needed"]:
        return True
    
    return False

def has_team_lost_bingo_game(team_ID: int) -> bool:
    """
        Returns whether the specified team has lost the bingo game.
    """

    lose_conditions = get_bingo_lose_conditions()

    # If the team has grabbed the required amount of red balls, they lose the game.
    red_balls_needed_to_lose = lose_conditions["red_balls_grabbed"]
    red_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "red")
    if red_balls_grabbed >= red_balls_needed_to_lose:
        return True
    return False

def has_team_won_or_lost_bingo_game(team_ID: int) -> bool:
    """
        Returns whether the specified team has won or lost the bingo game.
    """

    team_has_won_bingo_game = has_team_won_bingo_game(team_ID)
    if team_has_won_bingo_game:
        return True
    
    team_has_lost_bingo_game = has_team_lost_bingo_game(team_ID)
    if team_has_lost_bingo_game:
        return True
    
    return False

def get_remaining_balls_for_team(team_ID: int) -> dict:
    """
        Returns a dictionary which holds the remaining balls information for the specified team.
    """

    team_data = teams_data[team_ID]
    balls_remaining = team_data["balls"]["remaining"]
    return balls_remaining

def get_remaining_color_balls_for_team(team_ID: int, color: str) -> int:
    """
        Returns the amount of remaining color balls for the specified team.
    """

    balls_remaining = get_remaining_balls_for_team(team_ID)
    remaining_color_balls = balls_remaining[color]
    return remaining_color_balls

def get_remaining_bingo_board_numbers_for_team(team_ID: int) -> List[int]:
    """
        Returns a list of the remaining numbers on the bingo board for the specified team.
    """

    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_positions_for_team(team_ID)
    bingo_board_size = get_bingo_board_size()
    
    remaining_numbers = []
    for row_index in range(bingo_board_size):
        for col_index in range(bingo_board_size):
            position = (row_index, col_index)
            if position not in filled_positions:
                number = bingo_board[row_index][col_index]
                remaining_numbers.append(number)
    
    return remaining_numbers

def get_available_bingo_board_pit_balls_for_team(team_ID: int) -> List:
    """
        Return a list which represents the bingo board pit for the specified team.
        It contains the remaining colored balls (red and green), as well as the remaining numbers on the specified team's bingo board.
    """

    bingo_board_pit_balls = []
    
    # Add the remaining green balls
    remaining_green_balls_in_pit = get_remaining_color_balls_for_team(team_ID, "green")
    for _ in range(remaining_green_balls_in_pit):
        bingo_board_pit_balls.append("green")

    # Add the remaining red balls
    remaining_red_balls_in_pit = get_remaining_color_balls_for_team(team_ID, "red")
    for _ in range(remaining_red_balls_in_pit):
        bingo_board_pit_balls.append("red")


    # Add the remaining numbers on the bingo board
    remaining_numbers_in_pit = get_remaining_bingo_board_numbers_for_team(team_ID)
    for number in remaining_numbers_in_pit:
        bingo_board_pit_balls.append(number)

    return bingo_board_pit_balls

def get_bingo_board_filled_horizontal_lines_amount_for_team(team_ID: int) -> int:
    """
        Returns the amount of filled horizontal lines on the bingo board for the specified team.
    """

    filled_positions = get_filled_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    filled_horizontal_lines_amount = 0
    for row_index in range(bingo_board_size):
        horizontal_line_is_marked = True
        for col_index in range(bingo_board_size):
            position = (row_index, col_index)

            if position not in filled_positions:
                horizontal_line_is_marked = False
                break
        
        if horizontal_line_is_marked:
            filled_horizontal_lines_amount += 1
    
    return filled_horizontal_lines_amount

def get_bingo_board_filled_vertical_lines_amount_for_team(team_ID: int) -> int:
    """
        Returns the amount of filled vertical lines on the bingo board for the specified team.
    """

    filled_positions = get_filled_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    filled_vertical_lines_amount = 0
    for col_index in range(bingo_board_size):
        vertical_line_is_marked = True
        for row_index in range(bingo_board_size):
            position = (row_index, col_index)

            if position not in filled_positions:
                vertical_line_is_marked = False
                break
        
        if vertical_line_is_marked:
            filled_vertical_lines_amount += 1
    
    return filled_vertical_lines_amount

def get_bingo_board_filled_diagonal_lines_amount_for_team(team_ID: int) -> int:
    """
        Returns the amount of filled diagonal lines on the bingo board for the specified team.
    """

    filled_positions = get_filled_positions_for_team(team_ID)
    bingo_board_size = get_bingo_board_size()

    filled_diagonal_lines_amount = 0

    # Check top-left to bottom-right diagonal line
    diagonal_line_is_marked = True
    for index in range(bingo_board_size):
        position = (index, index)
        if position not in filled_positions:
            diagonal_line_is_marked = False
            break
    if diagonal_line_is_marked:
        filled_diagonal_lines_amount += 1

    # Check top-right to bottom-left diagonal line
    diagonal_line_is_marked = True
    for index in range(bingo_board_size):
        column_index = bingo_board_size - 1 - index
        position = (index, column_index)
        if position not in filled_positions:
            diagonal_line_is_marked = False
            break
    
    if diagonal_line_is_marked:
        filled_diagonal_lines_amount += 1

    return filled_diagonal_lines_amount

def get_bingo_board_total_filled_lines_amount_for_team(team_ID: int) -> int:
    """
        Returns the total amount of filled lines on the bingo board for the specified team.
    """

    filled_horizontal_lines_amount = get_bingo_board_filled_horizontal_lines_amount_for_team(team_ID)
    filled_vertical_lines_amount = get_bingo_board_filled_vertical_lines_amount_for_team(team_ID)
    filled_diagonal_lines_amount = get_bingo_board_filled_diagonal_lines_amount_for_team(team_ID)

    total_filled_lines_amount = filled_horizontal_lines_amount + filled_vertical_lines_amount + filled_diagonal_lines_amount
    return total_filled_lines_amount


###
### SETTERS
###


def increase_grabbed_color_balls_for_team(team_ID: int, color: str) -> None:
    """
        Increases the amount of grabbed color balls for the specified team and color by 1.
    """

    balls_grabbed = get_balls_grabbed_by_team(team_ID)
    balls_grabbed[color] += 1

def decrease_remaining_color_balls_for_team(team_ID: int, color: str) -> None:
    """
        Decreases the amount of remaining color balls for the specified team and color by 1.
    """

    balls_remaining = get_remaining_balls_for_team(team_ID)
    balls_remaining[color] -= 1

def mark_number_on_bingo_board_for_team(team_ID: int, grabbed_number: int) -> None:
    """
        Marks the grabbled number on the bingo board for the specified team.
    """
    
    bingo_board = get_bingo_board_for_team(team_ID)
    filled_positions = get_filled_positions_for_team(team_ID)

    bingo_board_size = get_bingo_board_size()
    for row_index in range(bingo_board_size):
        for col_index in range(bingo_board_size):
            number = bingo_board[row_index][col_index]
            if number == grabbed_number:
                position = (row_index, col_index)
                filled_positions.add(position)
                return