import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from lingo.teams_data import teams_data
from lingo.lingo_settings.lingo_settings_utils import get_starting_team_ID
from lingo.lingo_utils import initialize_teams_data
from test_lib import report, test
from lingo.wordle.wordle_utils import add_guess_to_current_round_for_team, add_single_initial_rounds_info_for_team, get_random_word, has_team_guessed_word_correctly_in_current_round

"""
    Test whether the function which would return a random word raises an exception when all available words have been used.
"""
def test_random_word_error_handling():
    words = [
        "test_word"
    ]
    used_words = set()

    for _ in range(len(words)):
        get_random_word(words, used_words)


    throws_exception = False
    try:
        get_random_word(words, used_words)
    except Exception:
        throws_exception = True

    expected = True
    test(
        "Getting a random word when all words have been used should raise an exception.",
        expected,
        throws_exception,
    )
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
        "If the team has guessd the correct word in the current round, the function should return True.",
        expected,
        result,
    )
test_whether_team_has_guessed_word_in_round()

# Run the report when this file is executed directly instead of within the tests.py file
if __name__ == "__main__":
    report()