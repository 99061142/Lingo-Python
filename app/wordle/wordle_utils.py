from ..teamsData import teamsData
from .words import five_letter_words
from random import choice

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
def is_valid_guess(guess: str) -> bool:
    if len(guess) != 5:
        return False
    
    if guess not in five_letter_words.words:
        return False
    
    return True
