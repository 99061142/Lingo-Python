from ..teamsData import teamsData
from .words import five_letter_words
from random import choice
from termcolor import colored
from typing import Optional

# Set to keep track of unavailable words.
# This will be used to avoid repeating words in the game.
_unavailable_words = set()

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

"""
    Get the current round information for a specific team.
    We default to an empty dictionary if we haven't yet set the roundsInfo for the team.
"""
def get_current_wordle_round_info(team_ID: int) -> dict:
    teamData = teamsData[team_ID]
    current_wordle_round_info = teamData["roundsInfo"][-1]
    return current_wordle_round_info

"""
    Get the list of guesses made in the current round for a specific team.
    We default to an empty list if no guesses have been made yet, even if we show the first letter of the word that needs to be guessed on the board.
"""
def get_current_wordle_round_guesses(team_ID: int) -> list:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    current_wordle_round_guesses = current_wordle_round_info["guesses"]
    return current_wordle_round_guesses

"""
    Get the current round's Wordle board for a specific team.
    This includes the guesses made so far, as well as empty rows for remaining attempts.
"""
def get_current_wordle_round_board(team_ID: int, max_attempts: int, word_length: int, word_to_guess: str) -> list:
    wordle_board = []
    wordle_round_guesses = get_current_wordle_round_guesses(team_ID)
    guessed_amount = len(wordle_round_guesses)

    # Add the guesses made so far to the board
    if guessed_amount:
        wordle_board.extend(wordle_round_guesses)

    # Add empty rows for the remaining attempts
    empty_guesses_amount = max_attempts - guessed_amount
    if empty_guesses_amount > 0:
        for _ in range(empty_guesses_amount):
            wordle_board.append(["_"] * word_length)

    # Reveal the first letter of the word to guess if no guesses have been made yet.
    if not guessed_amount:
        wordle_board[0][0] = word_to_guess[0]

    return wordle_board

"""
    Get the color of a specific letter in the current round's Wordle board.
    If the position is out of range, we return None. (Which defaults to the default terminal color.)
    Else we return the color we have stored for that letter.
"""
def get_current_wordle_round_letter_color(team_ID: int, row: int, col: int) -> Optional[str]:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    guesses_color = current_wordle_round_info.get("guessesColor", [])
    if row >= len(guesses_color) or col >= len(guesses_color[row]):
        return None
    return guesses_color[row][col]

"""
    Return a stringified version of the Wordle board for display purposes.
"""
def get_stringified_wordle_board(team_ID: int, max_attempts: int, word_length: int, word_to_guess: str) -> str:
    amount_of_space_between_letters = 2
    col_width = amount_of_space_between_letters * 2 + 1 # Spaces on both sides + letter itself
    board_width = word_length * col_width

    # Add text at the top of the board, which we also center
    title = "WORDLE BOARD"
    stringified_board = f"\n{title.center(board_width)}\n\n"

    wordle_board = get_current_wordle_round_board(team_ID, max_attempts, word_length, word_to_guess)
    for row_index, row in enumerate(wordle_board):
        for col_index, letter in enumerate(row):
            letter_color = get_current_wordle_round_letter_color(team_ID, row_index, col_index)
            stringified_board += f"{" " * amount_of_space_between_letters}{colored(letter, letter_color)}{" " * amount_of_space_between_letters}"

        stringified_board += "\n\n"
    
    return stringified_board