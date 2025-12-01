from lingo.lingo import ask_to_play_again, start_game
from lingo.lingo_utils import print_message

def main() -> None:
    """
        Start the Lingo game application.
    """
    want_to_keep_playing = True
    while want_to_keep_playing:
        start_game()
        want_to_keep_playing = ask_to_play_again()
    
    print_message("Thanks for playing the game!")
    exit(0)

if __name__ == "__main__":
    main()