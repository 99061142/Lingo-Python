from ..teams_data import teams_data
from .words import five_letter_words
from random import choice
from termcolor import colored
from typing import Optional
from ..constants import WORD_TO_GUESS_LENGTH, MAX_ATTEMPTS

# Global Set to keep track of unavailable words.    
# This will be used to avoid repeating words in the game.
_unavailable_words = set()


###
### GETTERS
###


"""
    Return the current round's Wordle board for a specific team.
    Do note that we also return empty rows for remaining attempts.
"""
def get_current_wordle_round_board(team_ID: int) -> list:
    wordle_board = []
    wordle_round_guesses = get_current_wordle_round_guesses(team_ID)
    guessed_amount = len(wordle_round_guesses)

    # Add the rows with the guesses made so far
    if guessed_amount:
        for guess in wordle_round_guesses:
            length_of_guess = len(guess)

            # If the length of the guess is less than the word to guess length, we add remaining underscores.
            # We do this since at the start of the round, we hardcoded the first letter only.
            # Because of this, we do not have 5 values within the guess yet.
            if length_of_guess < WORD_TO_GUESS_LENGTH:
                guess += "_" * (WORD_TO_GUESS_LENGTH - length_of_guess)

            wordle_board.append(list(guess))

    # Add empty rows for the remaining attempts
    missing_guesses_amount = MAX_ATTEMPTS - guessed_amount
    for _ in range(missing_guesses_amount):
        placeholder_guess = []
        for _ in range(WORD_TO_GUESS_LENGTH):
            placeholder_guess.append("_")
        wordle_board.append(placeholder_guess)

    return wordle_board

"""
    Return the color of a specific letter in the current round's Wordle board.
    If the position is out of range, we return None. (Which defaults to the default terminal color.)
    Else we return the color we have stored for that letter.
"""
def get_current_wordle_round_letter_color(team_ID: int, position: tuple) -> Optional[str]:
    row, col = position
    current_wordle_round_guesses_color = get_current_wordle_round_guesses_color(team_ID)

    if row >= len(current_wordle_round_guesses_color) or col >= len(current_wordle_round_guesses_color[row]):
        return None
    return current_wordle_round_guesses_color[row][col]

"""
    Return a stringified version of the Wordle board for display purposes.
"""
def get_stringified_wordle_board(team_ID: int) -> str:
    amount_of_space_between_letters = 2
    col_width = amount_of_space_between_letters * 2 + 1 # Spaces on both sides + letter itself
    board_width = WORD_TO_GUESS_LENGTH * col_width

    # Add text at the top of the board, which we also center
    title = "WORDLE BOARD"
    stringified_board = f"\n{title.center(board_width)}\n\n"

    wordle_board = get_current_wordle_round_board(team_ID)
    for row_index, row in enumerate(wordle_board):
        for col_index, letter in enumerate(row):
            letter_position_on_wordle_board = (row_index, col_index)
            letter_color = get_current_wordle_round_letter_color(team_ID, letter_position_on_wordle_board)
            stringified_board += f"{" " * amount_of_space_between_letters}{colored(letter, letter_color)}{" " * amount_of_space_between_letters}"

        stringified_board += "\n\n"
    
    return stringified_board

"""
    Get the current round information for a specific team.
    We throw an error if the team does not have any rounds info yet.
"""
def get_current_wordle_round_info(team_ID: int) -> dict:
    teamData = teams_data[team_ID]
    current_wordle_round_info = teamData["roundsInfo"]

    if not current_wordle_round_info:
        raise ValueError(f"Team with ID {team_ID} does not have any rounds info initialized.")
    
    current_wordle_round_info = current_wordle_round_info[-1]
    return current_wordle_round_info

"""
    Get the word to guess for the current round of a specific team.
"""
def get_current_wordle_round_word_to_guess(team_ID: int) -> str:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    word_to_guess = current_wordle_round_info["wordToGuess"]
    return word_to_guess

"""
    Get the colors of the guesses made in the current round for a specific team.
"""
def get_current_wordle_round_guesses_color(team_ID: int) -> list:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    guesses_color = current_wordle_round_info["guessesColor"]
    return guesses_color

"""
    Get the guesses made in the current round for a specific team.
"""
def get_current_wordle_round_guesses(team_ID: int) -> int:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    guesses = current_wordle_round_info["guesses"]
    return guesses

"""
    Returns a random five-letter word from the list of words.
"""
def get_random_word() -> str:
    words = five_letter_words.words

    while True:
        word = choice(words)
        if word not in _unavailable_words:
            _unavailable_words.add(word)
            return word

"""
    Return a list of colors for each letter in the guess based on its correctness compared to the word to guess.
"""
def get_guess_letters_color_based_on_word_to_guess(guess: str, word_to_guess: str) -> list:
    # The colors we will use to indicate correctness
    colors = {
        "correct": "green",
        "misplaced": "yellow",
        "incorrect": "red"
    }
    
    # Create and return the list of colors for each letter in the guess
    guess_colors = list(word_to_guess)
    for index, letter in enumerate(guess):
        word_to_guess_letter = word_to_guess[index]
        if letter == word_to_guess_letter:
            guess_colors[index] = colors["correct"]
            continue

        if letter in word_to_guess:
            guess_colors[index] = colors["misplaced"]
            continue

        guess_colors[index] = colors["incorrect"]
    
    return guess_colors

###
### SETTERS
###


"""
    Initialize the roundsInfo for a specific team with the initial round data.
"""
def add_single_initial_rounds_info(team_ID: int) -> None:
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
                "green"
            ]
        ]
    }

    # If the team has no previous rounds played, we set the first guess and its color.
    rounds_played = len(teamData["roundsInfo"])
    if rounds_played == 0:
        initial_rounds_info["guesses"] = [
            [
                word_to_guess[0]
            ]
        ]
        initial_rounds_info["guessesColor"] = [
            [
                "green"
            ]
        ]

    teamData["roundsInfo"].append(initial_rounds_info)

"""
    Add a guess to the current round for a specific team, adding both the guess and its corresponding colors.
"""
def add_guess_to_current_round(team_ID: int, guess: str, round_number: int) -> None:
    word_to_guess = get_current_wordle_round_word_to_guess(team_ID)
    guess_colors = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    current_wordle_round_info["guesses"][round_number] = guess
    current_wordle_round_info["guessesColor"][round_number] = guess_colors


###
### VALIDATORS
###


"""
    Validate if the provided word is a valid five-letter word, and is a word which is an option for the user to guess.
"""
def is_valid_guess(guess: str) -> dict:
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