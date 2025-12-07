from random import choice
from ...teams_data import teams_data
from ...lingo_settings.lingo_settings_utils import get_amount_of_teams
from .five_letter_words import words as five_letter_words

# A dictionary which holds all the words lists.
#! Do note that the values must be a list, and not a set, as we need to be able to use choice() to get a random word within the list
_words = {
    5: five_letter_words,
}
_words_lengths = list(_words.keys())

def get_words_of_length(length: int) -> list[str]:
    """
        Returns a list of words of the specified length.
    """

    # If there are no words of the specified length, return an empty list.
    if length not in _words_lengths:
        return []
    
    # If there are words of the specified length, return them.
    words_of_length = _words[length]
    return words_of_length

def get_random_word_of_length(length: int) -> str:
    """
        Returns a random word of the specified length.
    """

    words_of_length = get_words_of_length(length)
    random_word = choice(words_of_length)
    return random_word

def get_random_word() -> str:
    """
        Returns a random word of any length.
    """

    while True:
        random_length = choice(_words_lengths)
        random_word_of_length = get_random_word_of_length(random_length)
        
        # If the random word has not been used yet, return it.
        words_used_of_length = get_used_wordle_words_of_length(random_length)
        if random_word_of_length not in words_used_of_length:
            return random_word_of_length

def get_used_wordle_words_of_length(length: int) -> set:
    """
        Return a set of all used Wordle words of a specific length across all teams and rounds.
    """
    
    used_wordle_words = set()
    
    # If the teams data is empty, we return an empty set
    if len(teams_data) == 0:
        return used_wordle_words
    
    teams_amount = get_amount_of_teams()
    for team_ID in range(teams_amount):
        team_data = teams_data[team_ID]
        rounds_info = team_data["roundsInfo"]
        for round_info in rounds_info:
            word_to_guess = round_info["wordToGuess"]
            if len(word_to_guess) == length:
                used_wordle_words.add(word_to_guess)
    
    return used_wordle_words

def get_used_wordle_words() -> set:
    """
        Return a set of all used Wordle words across all teams and rounds.
    """
    
    used_wordle_words = set()
    
    # If the teams data is empty, we return an empty set
    if len(teams_data) == 0:
        return used_wordle_words
    
    teams_amount = get_amount_of_teams()
    for team_ID in range(teams_amount):
        team_data = teams_data[team_ID]
        rounds_info = team_data["roundsInfo"]
        for round_info in rounds_info:
            word_to_guess = round_info["wordToGuess"]
            used_wordle_words.add(word_to_guess)
    
    return used_wordle_words