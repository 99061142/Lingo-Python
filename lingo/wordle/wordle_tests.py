import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from lingo.wordle.wordle_utils import get_random_word
from test_lib import report, test

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


# Run the report when this file is executed directly instead of within the tests.py file
if __name__ == "__main__":
    report()