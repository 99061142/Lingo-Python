from json import load

with open("lingo/wordle/wordle_settings/wordle_settings.json", "r") as settings_file:
    wordle_settings = load(settings_file)


###
### GETTERS
###


"""
    Return the letter placeholder used for empty letters in the Wordle board.
"""
def get_empty_column_placeholder_for_wordle_board() -> str:
    letter_placeholder = wordle_settings.get("empty_column_placeholder", "")
    return letter_placeholder

"""
    Return the maximum amount of wordle guess attempts allowed.
"""
def get_max_wordle_guess_attempts() -> int:
    max_attempts = wordle_settings.get("max_guess_attempts", float('inf'))
    return max_attempts

"""
    Return the available letter position colors from the wordle settings.
"""
def get_available_letter_position_colors() -> dict:
    available_letter_position_colors = wordle_settings.get("letter_color_for_guess", {})
    return available_letter_position_colors
