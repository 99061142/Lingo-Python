from .wordle_utils import *

def ask_user_guess() -> str:
    while True:
        guess = input("Enter your 5-letter guess: ").strip().lower()
        if is_valid_guess(guess):
            return guess
        else:
            print("Invalid word. Please try again.")