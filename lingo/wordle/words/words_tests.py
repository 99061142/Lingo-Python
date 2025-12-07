from test_lib import test
from .words_utils import *
from ...lingo_utils import initialize_teams_data, remove_teams_data
from ...teams_data import teams_data

def test_get_random_word() -> None:
    """
        Test whether the function which returns a random word works correctly.
    """

    result = get_random_word()
    expected = result is not None 
    test(
        f"Getting a random word should return a word in one of the possible words lists.",
        expected,
        True,
    )
test_get_random_word()

def test_get_random_word_of_length() -> None:
    """
        Test whether the function which gets words of a specific length works correctly.
    """

    # Test whether if we call the function with the length of 5 as argument, we get a word of length 5
    length = 5
    word_of_length = get_random_word_of_length(length)
    result_length = len(word_of_length)
    test(
        f"Getting a random word of length {length} should return a word of length {length}.",
        length,
        result_length,
    )
test_get_random_word_of_length()

def test_get_used_wordle_words_of_length() -> None:
    """
        Test whether the function which gets the used Wordle words of a specific length works correctly.
    """

    # Test whether we get an empty set when no words have been used yet when calling the function with length 5
    length = 5
    expected = set()
    result = get_used_wordle_words_of_length(length)
    test(
        f"Getting all used Wordle words of length {length} when no words of length {length} have been used in the Wordle minigame should return an empty set.",
        expected,
        result,
    )

    # Test whether we only get the words of length 5 when not all used words are of length 5
    initialize_teams_data()
    team_ID = 0
    teams_data[team_ID]["roundsInfo"].append({
        "wordToGuess": "12345",
    })
    teams_data[team_ID]["roundsInfo"].append({
        "wordToGuess": "123456",
    })
    expected = set(["12345"])
    result = get_used_wordle_words_of_length(length)
    test(
        f"When calling `get_used_wordle_words_of_length` with length {length} when 1 of the 2 rounds used a word of length {length}, the function should only return the set with that 1 word of length {length}.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_used_wordle_words_of_length()

def test_get_used_wordle_words() -> None:
    """
        Test whether the function which gets all used Wordle words works correctly.
    """

    # Test whether we get an empty set when no words have been used yet
    expected = set()
    result = get_used_wordle_words()
    test(
        f"Getting all used Wordle words when no words have been used in the Wordle minigame should return an empty set.",
        expected,
        result,
    )

    # Test whether we get all used words when words of different lengths have been used
    initialize_teams_data()
    team_ID = 0
    teams_data[team_ID]["roundsInfo"] = [
        {
            "wordToGuess": "12345",
        },
        {
            "wordToGuess": "123456"
        }
    ]
    expected = set(["12345", "123456"])
    result = get_used_wordle_words()
    test(
        f"When calling `get_used_wordle_words` after 2 rounds which used 2 different length words, the function should return the set with both words.",
        expected,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_used_wordle_words()

def test_get_words_of_length() -> None:
    """
        Test whether the function which gets all words of a specific length works correctly.
    """

    # Test whether we get an empty list when we call the function with a length that has no words
    length = 0
    expected = []
    result = get_words_of_length(length)
    test(
        f"Getting all words of length {length} when there are no words of length {length} should return an empty list.",
        expected,
        result,
    )

    # Test whether we get a list of words with a length of 5 when we call the function with 5 as argument
    length = 5
    words_of_length = get_words_of_length(length)
    words_are_of_length = all(len(word) == length for word in words_of_length)
    test(
        f"Getting all words of length {length} should only return words of length {length}.",
        True,
        words_are_of_length,
    )
test_get_words_of_length()