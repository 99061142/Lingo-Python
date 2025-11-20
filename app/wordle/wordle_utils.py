from app.bingo.bingo_utils import bingo_board_has_line_for_team, get_amount_of_green_balls_grabbed, get_amount_of_red_balls_grabbed
from ..teams_data import teams_data
from .words import five_letter_words
from random import choice
from termcolor import colored
from ..constants import DEFAULT_EMPTY_LETTER_PLACEHOLDER, DEFAULT_TERMINAL_COLOR, GAP_BETWEEN_LETTERS, MAX_ATTEMPTS

# Global Set to keep track of unavailable words.    
# This will be used to avoid repeating words in the game.
_unavailable_words = set()


###
### GETTERS
###


"""
    Return the amount of rounds won by the specific team.
"""
def amount_of_rounds_won_by_team(team_ID: int) -> int:
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
    Return the amount of rounds lost in a row by the specific team.
"""
def amount_of_rounds_lost_in_a_row(team_ID: int) -> int:
    teamData = teams_data[team_ID]
    roundsInfo = teamData["roundsInfo"]
    rounds_lost_in_a_row = 0

    for round_info in reversed(roundsInfo):
        word_to_guess = round_info["wordToGuess"]
        last_guess = round_info["guesses"][-1]

        if last_guess != word_to_guess:
            rounds_lost_in_a_row += 1
        else:
            break
    
    return rounds_lost_in_a_row

"""
    Return the current round's Wordle board for a specific team.
    Do note that we also return empty rows for remaining attempts.
"""
def get_current_wordle_round_board(team_ID: int) -> list:
    word_to_guess = get_current_wordle_round_word_to_guess(team_ID)
    word_to_guess_length = len(word_to_guess)
    
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
            if length_of_guess < word_to_guess_length:
                guess += DEFAULT_EMPTY_LETTER_PLACEHOLDER * (word_to_guess_length - length_of_guess)

            wordle_board.append(list(guess))

    # Add empty rows for the remaining attempts
    missing_guesses_amount = MAX_ATTEMPTS - guessed_amount
    for _ in range(missing_guesses_amount):
        placeholder_guess = []
        for _ in range(word_to_guess_length):
            placeholder_guess.append(DEFAULT_EMPTY_LETTER_PLACEHOLDER)
        wordle_board.append(placeholder_guess)

    return wordle_board

"""
    Return the color of a specific letter in the current round's Wordle board.
    If the position is out of bounds, we return the default terminal color which we have set as a the constant `DEFAULT_TERMINAL_COLOR`.
"""
def get_current_wordle_round_letter_color(team_ID: int, position: tuple) -> str:
    row, col = position
    current_wordle_round_guesses_color = get_current_wordle_round_guesses_color(team_ID)

    if row >= len(current_wordle_round_guesses_color) or col >= len(current_wordle_round_guesses_color[row]):
        return DEFAULT_TERMINAL_COLOR
    return current_wordle_round_guesses_color[row][col]

def get_wordle_board_width(team_ID: int) -> int:
    word_to_guess = get_current_wordle_round_word_to_guess(team_ID)
    word_to_guess_length = len(word_to_guess)

    amount_of_space_between_letters = GAP_BETWEEN_LETTERS
    col_width = amount_of_space_between_letters * 2 + 1 # Spaces on both sides + letter itself
    board_width = word_to_guess_length * col_width
    return board_width

"""
    Return a stringified version of the Wordle board for display purposes.
"""
def get_stringified_wordle_board(team_ID: int) -> str:
    board_width = get_wordle_board_width(team_ID)

    # Add text at the top of the board, which we also center
    title = "WORDLE BOARD"
    stringified_board = f"\n{title.center(board_width)}\n\n"

    wordle_board = get_current_wordle_round_board(team_ID)
    for row_index, row in enumerate(wordle_board):
        for col_index, letter in enumerate(row):
            letter_position_on_wordle_board = (row_index, col_index)
            letter_color = get_current_wordle_round_letter_color(team_ID, letter_position_on_wordle_board)
            stringified_board += f"{" " * GAP_BETWEEN_LETTERS}{colored(letter, letter_color)}{" " * GAP_BETWEEN_LETTERS}"

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
        raise ValueError(f"Team with ID {team_ID} does not have any rounds info initialized. Call `add_single_initial_rounds_info` to add the first round info.")
    
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
def add_guess_to_current_round(team_ID: int, guess: str, attempt_number: int) -> None:
    current_wordle_round_info = get_current_wordle_round_info(team_ID)
    current_wordle_round_guesses = current_wordle_round_info["guesses"]

    # If this is a new attempt, we need to add empty lists for the new attempt.
    # We check 'is equal' here since attempt_number is 0-indexed.
    # This will be True when the row for the attempt doesn't show letters which are on the correct position yet.
    amount_of_guesses_made_without_current = len(current_wordle_round_guesses)
    if amount_of_guesses_made_without_current == attempt_number:
        current_wordle_round_guesses.append([])
        current_wordle_round_info["guessesColor"].append([])

    current_wordle_round_guesses[attempt_number] = guess

    word_to_guess = get_current_wordle_round_word_to_guess(team_ID)
    guess_colors = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    current_wordle_round_info["guessesColor"][attempt_number] = guess_colors

    # We create a temporary next attempt row to check if we need to add correct letters to it. 
    # If we don't do this, the user won't see which letters were correct in the next attempt row.
    next_attempt_row_guess = []
    next_attempt_row_colors = []
    one_or_more_correct_letters_found = False
    for i, guess_color in enumerate(guess_colors):
        # If the letter is correct, we show it in the next attempt row as well.
        if guess_color == "green":
            next_attempt_row_guess.append(guess[i])
            next_attempt_row_colors.append("green")
            one_or_more_correct_letters_found = True
            continue
        
        # If not, we just add the placeholder and default color.
        # This is done to check if one or more correct letters were found in the current guess.
        next_attempt_row_guess.append(DEFAULT_EMPTY_LETTER_PLACEHOLDER)
        next_attempt_row_colors.append(DEFAULT_TERMINAL_COLOR)

    # If one or more correct letters were found, we add the next attempt row to show the correct letters.
    if one_or_more_correct_letters_found:
        current_wordle_round_guesses.append(next_attempt_row_guess)
        current_wordle_round_info["guessesColor"].append(next_attempt_row_colors)


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

"""
    Returns whether the team has won the Wordle game based on the winning conditions.
"""
def team_has_won_wordle_game(team_ID: int) -> bool:
    # If the team has grabbed 3 or more green balls, they win the game.
    green_balls_grabbed = get_amount_of_green_balls_grabbed(team_ID)
    if green_balls_grabbed >= 3:
        return True
    
    # If the team has any line on their bingo board, they win the game.
    has_any_filled_lines_on_bingo_board = bingo_board_has_line_for_team(team_ID)
    if has_any_filled_lines_on_bingo_board:
        return True
    
    # If the team has won 10 or more rounds, they win the game.
    rounds_won = amount_of_rounds_won_by_team(team_ID)
    if rounds_won >= 10:
        return True
    
    return False

def team_has_lost_wordle_game(team_ID: int) -> bool:
    # If the team has grabbed 3 or more red balls, they lose the game.
    red_balls_grabbed = get_amount_of_red_balls_grabbed(team_ID)
    if red_balls_grabbed >= 3:
        return True
    
    # If the team has lost 3 rounds in a row, they lose the game.
    rounds_lost_in_a_row = amount_of_rounds_lost_in_a_row(team_ID)
    if rounds_lost_in_a_row >= 3:
        return True
    
    return False