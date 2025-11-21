from ..teams_data import teams_data
from .words import five_letter_words
from random import choice
from termcolor import colored
from ..app_constants import GAP_BETWEEN_BOARD_COLUMNS
from ..app_settings.app_settings_utils import get_amount_of_teams
from .wordle_settings.wordle_settings_utils import get_max_wordle_guess_attempts, get_empty_column_placeholder_for_wordle_board, get_available_letter_position_colors


# Global set to keep track of used wordle words.
# This will be used to avoid repeating words within the rounds of the wordle game
_used_wordle_words = set()


###
### GETTERS
###


"""
    Return whether the team has guessed the word correctly in the current round.
"""
def has_team_guessed_word_correctly_in_current_round(team_ID: int) -> bool:
    current_wordle_round = get_current_wordle_round_for_team(team_ID)
    word_to_guess = current_wordle_round["wordToGuess"]
    last_guess = current_wordle_round["guesses"][-1]

    if last_guess == word_to_guess:
        return True
    return False

"""
    Return the amount of rounds won within the Wordle game by the specific team.
"""
def amount_of_wordle_rounds_won_by_team(team_ID: int) -> int:
    teamData = teams_data[team_ID]
    roundsInfo = teamData["roundsInfo"]
    
    rounds_won = 0
    for round_info in roundsInfo:
        word_to_guess = round_info["wordToGuess"]
        last_guess = round_info["guesses"][-1]

        if last_guess == word_to_guess:
            rounds_won += 1
    
    return rounds_won

"""
    Return the amount of rounds lost in a row within the Wordle game by the specific team.
"""
def amount_of_wordle_rounds_lost_in_a_row_by_team(team_ID: int) -> int:
    teamData = teams_data[team_ID]
    roundsInfo = teamData["roundsInfo"]
    
    rounds_lost_in_a_row = 0
    for round_info in reversed(roundsInfo):
        word_to_guess = round_info["wordToGuess"]
        last_guess = round_info["guesses"][-1]

        if last_guess == word_to_guess:
            break

        rounds_lost_in_a_row += 1
    
    return rounds_lost_in_a_row

"""
    Return the current round's Wordle board for the specified team.
    !Do note that this is a 2D list representing the wordle board, with placeholders for empty rows and/or letters.
    !This is not a stringified version of the board for display purposes.
"""
def get_current_wordle_round_board_for_team(team_ID: int) -> list:
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    word_to_guess_length = len(word_to_guess)
    
    wordle_board = []
    wordle_round_guesses = get_current_wordle_round_guesses_by_team(team_ID)
    guesses_amount = len(wordle_round_guesses)
    letter_placeholder = get_empty_column_placeholder_for_wordle_board()

    # Add each guess made so far to the board
    if guesses_amount:
        for guess in wordle_round_guesses:
            # If the length of the guess is less than the word to guess, we fill the remaining spaces with the placeholder.
            # We do this since at the start of the each wordle round, we add the first letter of the word to guess as the initial guess.
            length_of_guess = len(guess)
            difference_between_lengths = word_to_guess_length - length_of_guess
            if difference_between_lengths > 0:
                guess += letter_placeholder * (difference_between_lengths)

            wordle_board.append(list(guess))

    # If the amount of guesses made is less than the maximum attempts, we fill the remaining rows with placeholders.
    missing_guesses_amount = get_max_wordle_guess_attempts() - guesses_amount
    for _ in range(missing_guesses_amount):
        placeholder_guess = []
        for _ in range(word_to_guess_length):
            placeholder_guess.append(letter_placeholder)
        wordle_board.append(placeholder_guess)

    return wordle_board

"""
    Return the color of the letter which is at the specified position in the last guessed word of the current round for the specified team.
    If the specified position is out of bounds, we return the default terminal color.
"""
def get_letter_color_for_current_round_last_guessed_word_by_team(team_ID: int, position: tuple) -> str:
    row, col = position
    current_wordle_round_guesses_color = get_current_wordle_round_guesses_color_for_team(team_ID)

    if row >= len(current_wordle_round_guesses_color) or col >= len(current_wordle_round_guesses_color[row]):
        default_color = get_available_letter_position_colors().get("default", None)
        return default_color
    return current_wordle_round_guesses_color[row][col]

"""
    Return the width of the current round's Wordle board for the specified team.
"""
def get_current_wordle_round_board_width_for_team(team_ID: int) -> int:
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    word_to_guess_length = len(word_to_guess)

    col_width = GAP_BETWEEN_BOARD_COLUMNS * 2 + 1 # Spaces on both sides + letter itself
    board_width = word_to_guess_length * col_width
    return board_width

"""
    Return a stringified version of the Wordle board for display purposes.
"""
def get_stringified_current_wordle_round_board_for_team(team_ID: int) -> str:
    board_width = get_current_wordle_round_board_width_for_team(team_ID)

    # Add the title to show above the board
    title = "WORDLE BOARD"
    stringified_board = f"\n{title.center(board_width)}\n\n"

    # Stringify each letter in the board with its corresponding color
    wordle_board = get_current_wordle_round_board_for_team(team_ID)
    for row_index, row in enumerate(wordle_board):
        for col_index, letter in enumerate(row):
            letter_position_within_guess = (row_index, col_index)
            letter_color = get_letter_color_for_current_round_last_guessed_word_by_team(team_ID, letter_position_within_guess)
            stringified_board += f"{" " * GAP_BETWEEN_BOARD_COLUMNS}{colored(letter, letter_color)}{" " * GAP_BETWEEN_BOARD_COLUMNS}"

        stringified_board += "\n\n"
    
    return stringified_board

"""
    Return the current round information for the specified team.
"""
def get_current_wordle_round_for_team(team_ID: int) -> dict:
    teamData = teams_data[team_ID]
    current_wordle_round = teamData["roundsInfo"][-1]
    return current_wordle_round

"""
    Return the word to guess for the current round for the specified team.
"""
def get_current_wordle_round_word_to_guess_for_team(team_ID: int) -> str:
    current_wordle_round = get_current_wordle_round_for_team(team_ID)
    word_to_guess = current_wordle_round["wordToGuess"]
    return word_to_guess

"""
    Return the colors of the guesses made in the current round for the specified team.
"""
def get_current_wordle_round_guesses_color_for_team(team_ID: int) -> list:
    current_wordle_round = get_current_wordle_round_for_team(team_ID)
    guesses_color = current_wordle_round["guessesColor"]
    return guesses_color

"""
    Return the guesses made in the current round for the specified team.
"""
def get_current_wordle_round_guesses_by_team(team_ID: int) -> int:
    current_wordle_round = get_current_wordle_round_for_team(team_ID)
    guesses = current_wordle_round["guesses"]
    return guesses

"""
    Return a random word within the available words we can use for the Wordle game.
"""
def get_random_word() -> str:
    # Keep picking random words until we find one which hasn't been used yet.
    # If the word isn't used yet, we add it to the used words set and return it
    words = five_letter_words.words
    while True:
        word = choice(words)
        if word not in _used_wordle_words:
            _used_wordle_words.add(word)
            return word

"""
    Return a list of colors for each letter in the guess based on its correctness compared to the word to guess.
"""
def get_guess_letters_color_based_on_word_to_guess(guess: str, word_to_guess: str) -> list:
    wordle_guess_colors = get_available_letter_position_colors()
    
    # Create and return the list of colors for each letter in the guess.
    #! Do note that we use the letters within the word to guess as placeholders initially
    guess_colors = list(word_to_guess)
    for index, letter in enumerate(guess):
        word_to_guess_letter = word_to_guess[index]
        if letter == word_to_guess_letter:
            guess_colors[index] = wordle_guess_colors["correct"]
            continue

        if letter in word_to_guess:
            guess_colors[index] = wordle_guess_colors["misplaced"]
            continue

        guess_colors[index] = wordle_guess_colors["incorrect"]
    
    return guess_colors

"""
    Return whether any team has won or lost the Wordle game.
"""
def any_team_has_won_or_lost_the_wordle_game() -> bool:
    for team_ID in range(get_amount_of_teams()):
        team_has_lost = has_team_lost_wordle_game(team_ID)
        if team_has_lost:
            return True

        team_has_won = has_team_won_wordle_game(team_ID)
        if team_has_won:
            return True
    return False

"""
    Return whether the specified team has won the Wordle game.
"""
def has_team_won_wordle_game(team_ID: int) -> bool:
    # If the team has won 10 or more rounds, they win the game
    rounds_won = amount_of_wordle_rounds_won_by_team(team_ID)
    if rounds_won >= 10:
        return True
    
    return False

"""
    Return whether the specified team has lost the Wordle game.
"""
def has_team_lost_wordle_game(team_ID: int) -> bool:
    # If the team has lost 3 rounds in a row, they lose the game
    rounds_lost_in_a_row = amount_of_wordle_rounds_lost_in_a_row_by_team(team_ID)
    if rounds_lost_in_a_row >= 3:
        return True
    
    return False


###
### SETTERS
###


"""
    Add the initial round info for the specified team within the global teams_data structure.
    !Do note that we will always add the first letter of the word to guess, and its corresponding color (correct position color) as the initial guess.
    !This is done to give the player a starting point for their guesses.
"""
def add_single_initial_rounds_info_for_team(team_ID: int) -> None:
    wordle_guess_colors = get_available_letter_position_colors() 
    word_to_guess = get_random_word()

    teamData = teams_data[team_ID]
    initial_rounds_info = {
        "wordToGuess": word_to_guess,
        "guesses": [
            [
                word_to_guess[0]
            ]
        ],
        "guessesColor": [
            [
                wordle_guess_colors["correct"]
            ]
        ]
    }
    teamData["roundsInfo"].append(initial_rounds_info)

"""
    Add the provided guess to the current round for the specified team.
    !Do note that this function also adds the guessesColor based on the correctness of the guess.
"""
def add_guess_to_current_round_for_team(team_ID: int, guess: str, attempt_number: int) -> None:
    current_wordle_round = get_current_wordle_round_for_team(team_ID)
    current_wordle_round_guesses = current_wordle_round["guesses"]

    # Add the guess to the current round's guesses
    current_wordle_round_guesses[attempt_number] = guess

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)

    # Add the colors for the guess based on its correctness
    guess_colors = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    current_wordle_round["guessesColor"][attempt_number] = guess_colors

    # If the word is guessed correctly, we do not need to add the letters and colors to the next attempt row
    if guess == word_to_guess:
        return

    # Go through each letter in the guess and add the letter within the `next_attempt_row_guess` list if it's correct, else we add the placeholder letter
    # We do the same for the colors within the `next_attempt_row_colors` list. If the letter is correct, we add the correct color, else we add the default terminal color
    next_attempt_row_guess = []
    next_attempt_row_colors = []

    wordle_guess_colors = get_available_letter_position_colors()
    correct_position_color = wordle_guess_colors["correct"]
    default_letter_color = wordle_guess_colors["default"]
    letter_placeholder = get_empty_column_placeholder_for_wordle_board()
    
    one_or_more_correct_letters_found = False
    for i, guess_color in enumerate(guess_colors):
        if guess_color != correct_position_color:
            next_attempt_row_guess.append(letter_placeholder)
            next_attempt_row_colors.append(default_letter_color)
            continue

        next_attempt_row_guess.append(guess[i])
        next_attempt_row_colors.append(correct_position_color)
        one_or_more_correct_letters_found = True

    # If one or more correct letters of the guess were on the correct position, we add the next attempt row's guess and colors to the current round's data.
    #! Do note that even if we add the next attempt row's guess and colors, after the user makes their next guess, they would just be overwritten.
    #! It is only for display purposes to show the user which letters they got correct in the correct position.
    if one_or_more_correct_letters_found:
        current_wordle_round_guesses.append(next_attempt_row_guess)
        current_wordle_round["guessesColor"].append(next_attempt_row_colors)


###
### VALIDATORS
###


"""
    Validate if the provided word is a valid five-letter word, and is a word which is an option for the user to guess.
"""
def is_valid_wordle_guess(guess: str) -> dict:
    if len(guess) != 5:
        return {
            "isValid": False,
            "message": "The word must be exactly 5 letters long."
        }
    
    if guess not in five_letter_words.words:
        return {
            "isValid": False,
            "message": "The word is not in the list of valid five-letter words."
        }
    
    return {
        "isValid": True,
        "message": ""
    }