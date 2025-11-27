import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from lingo.wordle.wordle_settings.wordle_settings_utils import get_empty_column_placeholder_for_wordle_board, get_max_wordle_guess_attempts
from lingo.lingo_constants import GAP_BETWEEN_BOARD_COLUMNS
from lingo.teams_data import teams_data
from lingo.lingo_settings.lingo_settings_utils import get_starting_team_ID, get_amount_of_teams
from lingo.lingo_utils import initialize_teams_data, remove_teams_data
from test_lib import report, test
from lingo.wordle.wordle_utils import add_guess_to_current_round_for_team, add_single_initial_rounds_info_for_team, get_current_wordle_round_board_width_for_team, get_current_wordle_round_word_to_guess_for_team, get_guess_letters_color_based_on_word_to_guess, get_random_word, has_team_guessed_word_correctly_in_current_round, has_team_lost_wordle_game, has_team_won_wordle_game, is_valid_wordle_guess

"""
    Test whether the function which would return a random word raises an exception when all available words have been used.
"""
async def test_random_word_error_handling():
    # Initialize the teams data to ensure we have a filled Wordle round with the used words set
    initialize_teams_data()

    # Add a single Wordle round for the starting team and simulate that they have used the only word available
    team_ID = get_starting_team_ID()
    add_single_initial_rounds_info_for_team(team_ID)
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    add_guess_to_current_round_for_team(team_ID, word_to_guess, 0)

    words = [
        word_to_guess
    ]

    # Simulate using all words
    for _ in range(len(words)):
        get_random_word(words)

    # Test whether getting a random word now raises an exception
    throws_exception = False
    try:
        get_random_word(words)
    except Exception:
        throws_exception = True

    expected = True
    test(
        "Getting a random word when all words have been used should raise an exception.",
        expected,
        throws_exception,
    )

    # Reset the teams data after the test.
    # This is done to let the other tests run without issues.
    await remove_teams_data()
test_random_word_error_handling()

"""
    Test whether the function correctly identifies when a team has guessed the word in the current round.
"""
def test_whether_team_has_guessed_word_in_round():
    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    # After we initialize the round, we simulate the team guessing the correct word
    attempt_number = 0
    word_to_guess = teams_data[team_ID]["roundsInfo"][attempt_number]["wordToGuess"]
    add_guess_to_current_round_for_team(team_ID, word_to_guess, attempt_number)

    expected = True
    result = has_team_guessed_word_correctly_in_current_round(team_ID)
    test(
        "If the team has guessed the correct word in the current round, the function should return True.",
        expected,
        result,
    )
test_whether_team_has_guessed_word_in_round()

"""
    Test whether the function which returns the Wordle board width returns the correct value based on the word length and the Wordle and Lingo settings.
"""
def test_wordle_board_width_calculation():
    # First we initialize the teams data
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    team_ID = get_starting_team_ID()
    add_single_initial_rounds_info_for_team(team_ID)

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    word_to_guess_length = len(word_to_guess)
    col_width = GAP_BETWEEN_BOARD_COLUMNS * 2 + 1 # Each column has gaps on both sides plus the letter itself
    
    expected_board_width = word_to_guess_length * col_width
    result = get_current_wordle_round_board_width_for_team(team_ID)
    test(
        "The calculated Wordle board width should match the expected width based on the word length and settings.",
        expected_board_width,
        result,
    )
test_wordle_board_width_calculation()

"""
    Test whether some letters are the respective colors when the guessed word has a mix of correct, misplaced, and incorrect letters
"""
def test_letter_position_color_determination():
    word_to_guess = "plant"
    guess = list("plate")
    expected_colors = [
        "green",
        "green",
        "green",
        "yellow",
        "red"
    ]
    result = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    test(
        f"The colors returned should be green, yellow, and red for correct, misplaced, and incorrect letters respectively.",
        expected_colors,
        result,
    )
test_letter_position_color_determination()

"""
    Test whether the function which returns if the team has won the Wordle game works correctly.
"""
def test_team_win_detection_in_wordle():
    # First we initialize the teams data to ensure we have the global dictionary to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Simulate that the team has won 10 rounds
    for _ in range(10):
        add_single_initial_rounds_info_for_team(team_ID)
        word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
        add_guess_to_current_round_for_team(team_ID, word_to_guess, 0)

    expected = True
    result = has_team_won_wordle_game(team_ID)
    test(
        "The function should return True when the team has won 10 rounds.",
        expected,
        result,
    )
test_team_win_detection_in_wordle()

"""
    Test whether the function which returns if the team has lost the Wordle game works correctly.
"""
def test_team_lost_wordle_game():
    # First we initialize the teams data to ensure we have the global dictionary to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Simulate that the team has lost 3 rounds in a row.
    # We do this by adding 3 rounds and filling it with a single incorrect guess.
    # This is done because we check if a round is won/lost based on whether the last guess was correct
    for _ in range(3):
        add_single_initial_rounds_info_for_team(team_ID)
        add_guess_to_current_round_for_team(team_ID, "wrong", 0)

    expected = True
    result = has_team_lost_wordle_game(team_ID)
    test(
        "The function should return False when the team has lost 3 rounds in a row.",
        expected,
        result,
    )
test_team_lost_wordle_game()

"""
    Test whether the function which validate the team's guess works correctly.
"""
def test_wordle_guess_validation():
    # First we initialize the teams data to ensure we have the round to work with
    initialize_teams_data()

    team_ID = get_starting_team_ID()


    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)

    # Test for incorrect length
    guess = word_to_guess[:-1]  # Make the guess one letter shorter
    result = is_valid_wordle_guess(guess, team_ID)
    expected = False
    test(
        "The function should return False for a guess with incorrect length.",
        expected,
        result["isValid"],
    )

    # Test for a word which is not in the allowed words list
    guess = "abcde" # Assuming 'abcde' is not in the allowed words list
    result = is_valid_wordle_guess(guess, team_ID)
    expected = False
    test(
        "The function should return False for a guess which is not in the allowed words list.",
        expected,
        result["isValid"],
    )

    result = is_valid_wordle_guess(word_to_guess, team_ID)
    expected = True
    test(
        "The function should return True for a valid Wordle guess.",
        expected,
        result["isValid"],
    )
test_wordle_guess_validation()

"""
    Test whether if the team guessed a word where 1 or more letters are on the correct position, we also show those letters on the next row of the Wordle board.
"""
def test_wordle_correct_letter_display():
    # First we initialize the teams data to ensure we have the round to work with
    initialize_teams_data()

    team_ID = get_starting_team_ID()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    guess = word_to_guess[:-1] + "x"  # Make the last letter incorrect
    attempt = 0

    # Simulate the team making the guess
    add_guess_to_current_round_for_team(team_ID, guess, attempt)

    # Check the display of the next row on the Wordle board,
    # and return the letters and placeholders shown on that row
    next_row_on_board = teams_data[team_ID]["roundsInfo"][0]["guesses"][attempt + 1]
    empty_column_placeholder = get_empty_column_placeholder_for_wordle_board()
    expected_letters_on_next_row = list(word_to_guess[:-1] + empty_column_placeholder)
    
    test(
        "The next row on the Wordle board should display the correct positioned letters from the previous guess",
        expected_letters_on_next_row,
        next_row_on_board,
    )
test_wordle_correct_letter_display()


# Run the report when this file is executed directly instead of within the tests.py file
if __name__ == "__main__":
    report()