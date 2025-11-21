from json import load

# Load Bingo settings from the JSON file
with open('app/bingo/bingo_settings/bingo_settings.json', 'r') as file:
    bingo_settings = load(file)


###
### GETTERS
###

"""
    Returns the size of the bingo board (amount of rows and columns).
"""
def get_bingo_board_size() -> int:
    board_size = bingo_settings.get("board_size", [])
    return board_size

"""
    Returns the colors used for bingo numbers based on their state (marked/unmarked).
"""
def get_bingo_number_colors() -> dict:
    number_colors = bingo_settings.get("number_color", {})
    return number_colors