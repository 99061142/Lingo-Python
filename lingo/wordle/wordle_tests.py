from test_lib import test
from ..teams_data import teams_data
from ..lingo_utils import initialize_teams_data, remove_teams_data
from ..lingo_settings.lingo_settings_utils import get_starting_team_ID, get_amount_of_teams
from ..lingo_constants import GAP_BETWEEN_BOARD_COLUMNS
from ..wordle.wordle_utils import *

def test_get_current_wordle_round_for_team() -> None:
    """
        Test whether the function which returns the current Wordle round for a specified team works correctly.
    """

    # First we initialize the teams data to ensure we have the global dictionary to work with.
    # This is required since the function being tested relies on there being a current round for the specified team
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Expect that the function raises an exception if there are no Wordle rounds for the team yet
    exception_has_occurred = False
    try:
        get_current_wordle_round_for_team(team_ID)
    except IndexError:
        exception_has_occurred = True
    test(
        "The function should raise an IndexError when there are no Wordle rounds for the specified team yet.",
        True,
        exception_has_occurred,
    )

    # Now we add a single initial round for the specified team and test if the function returns the correct round info.
    # Do note that we do this by just checking if the word to guess matches, since we cannot compare a whole dictionary within this test library
    add_single_initial_rounds_info_for_team(team_ID)
    
    expected_word_to_guess = teams_data[team_ID]["roundsInfo"][-1]["wordToGuess"]
    result_word_to_guess = get_current_wordle_round_for_team(team_ID)["wordToGuess"]
    test(
        "The function should return the correct current Wordle round information for the specified team.",
        expected_word_to_guess,
        result_word_to_guess,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_for_team()

def test_get_current_wordle_round_board_width_for_team() -> None:
    """
        Test whether the function which returns the Wordle board width for the current round for the specified team works correctly.
    """

    # First we initialize the teams data to ensure we have the global dictionary to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Now we add a single initial round for the specified team.
    # This is needed since the function being tested relies on there being a current round for the specified team
    add_single_initial_rounds_info_for_team(team_ID)
    
    word_to_guess = teams_data[team_ID]["roundsInfo"][-1]["wordToGuess"]
    word_to_guess_length = len(word_to_guess)
    expected_board_width = word_to_guess_length * (2 * GAP_BETWEEN_BOARD_COLUMNS) + word_to_guess_length # Each column has gaps on both sides plus the letter itself
    result_board_width = get_current_wordle_round_board_width_for_team(team_ID)
    test(
        "The function should return the correct Wordle board width for the current round for the specified team.",
        expected_board_width,
        result_board_width,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_board_width_for_team()

def test_get_current_wordle_round_word_to_guess_for_team() -> None:
    """
        Test whether the function which returns the word to guess for the current round for the specified team works correctly.
    """

    # First we initialize the teams data to ensure we have the global dictionary to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being a current round for the specified team
    add_single_initial_rounds_info_for_team(team_ID)
    
    expected_word_to_guess = teams_data[team_ID]["roundsInfo"][-1]["wordToGuess"]
    result_word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    test(
        "The function should return the correct word to guess for the current round for the specified team.",
        expected_word_to_guess,
        result_word_to_guess,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_word_to_guess_for_team()

def test_has_team_guessed_word_correctly_in_current_wordle_round() -> None:
    """
        Test whether the function correctly identifies when a team has guessed the word in the current round.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    # After we initialize the rounds, we simulate the team guessing a word that is not correct
    attempt_number = 0
    word_to_guess = teams_data[team_ID]["roundsInfo"][attempt_number]["wordToGuess"]
    guess = word_to_guess[::-1]  # Just reverse the word to ensure it is incorrect, even if it isn't a valid word
    teams_data[team_ID]["roundsInfo"][attempt_number]["guesses"].append(guess)

    # Test that the function returns False since the team has not guessed the correct word yet
    expected = False
    has_guessed_word_in_current_wordle_round = has_team_guessed_word_correctly_in_current_wordle_round(team_ID)
    test(
        "If the team has not guessed the correct word in the current round, the function should return False.",
        expected,
        has_guessed_word_in_current_wordle_round,
    )

    # Now we simulate the team guessing the correct word
    teams_data[team_ID]["roundsInfo"][attempt_number]["guesses"].append(word_to_guess)

    # Test that the function now returns True since the team has guessed the correct word
    expected = True
    has_guessed_word_in_current_wordle_round = has_team_guessed_word_correctly_in_current_wordle_round(team_ID)
    test(
        "If the team has guessed the correct word in the current round, the function should return True.",
        expected,
        has_guessed_word_in_current_wordle_round,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_guessed_word_correctly_in_current_wordle_round()

def test_amount_of_wordle_rounds_won_by_team() -> None:
    """
        Test whether the function correctly returns the amount of Wordle rounds won by the specified team.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being rounds for the specified team
    initialize_teams_data()

    rounds_won = 3
    
    # After we initialize the teams data, we add multiple Wordle rounds for the starting team
    for round_index in range(rounds_won + 1):
        add_single_initial_rounds_info_for_team(team_ID)

        # We simulate that the team has won the first <rounds_won> rounds by guessing the correct word
        if round_index < rounds_won:
            word_to_guess = teams_data[team_ID]["roundsInfo"][round_index]["wordToGuess"]
            teams_data[team_ID]["roundsInfo"][round_index]["guesses"].append(word_to_guess)


    # Test that the function returns the correct amount of rounds won by the specified team
    result = amount_of_wordle_rounds_won_by_team(team_ID)
    test(
        f"The function should return that the team has won {rounds_won} Wordle rounds if they have guessed the correct word in that many rounds.",
        rounds_won,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_amount_of_wordle_rounds_won_by_team()

def test_amount_of_wordle_rounds_lost_in_a_row_by_team() -> None:
    """
        Test whether the function correctly returns the amount of Wordle rounds lost in a row by the specified team.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being rounds for the specified team
    initialize_teams_data()

    rounds_lost_in_a_row = 2
    
    # After we initialize the teams data, we add multiple Wordle rounds for the starting team
    for round_index in range(rounds_lost_in_a_row + 1):
        add_single_initial_rounds_info_for_team(team_ID)


        # We simulate that the team has lost the last <rounds_lost_in_a_row> rounds by guessing incorrect words
        if round_index < rounds_lost_in_a_row:
            word_to_guess = teams_data[team_ID]["roundsInfo"][round_index]["wordToGuess"]
            incorrect_guess = word_to_guess[::-1]  # Just reverse the word to ensure it is incorrect, even if it isn't a valid word
            teams_data[team_ID]["roundsInfo"][round_index]["guesses"].append(incorrect_guess)

    # Test that the function returns the correct amount of rounds lost in a row by the specified team
    result = amount_of_wordle_rounds_lost_in_a_row_by_team(team_ID)
    test(
        f"The function should return that the team has lost {rounds_lost_in_a_row} Wordle rounds in a row if they have guessed incorrectly in that many consecutive rounds.",
        rounds_lost_in_a_row,
        result,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_amount_of_wordle_rounds_lost_in_a_row_by_team()

def test_get_current_wordle_round_guesses_by_team() -> None:
    """
        Test whether the function which returns the guesses made in the current round for the specified team works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being a current round for the specified team
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    # Remove the first empty guess placeholders before simulating the guesses made
    teams_data[team_ID]["roundsInfo"][-1]["guesses"] = []

    # Simulate the guesses made by the team in the current round
    guesses = ["apple", "berry", "cherry"]
    for guess in guesses:
        teams_data[team_ID]["roundsInfo"][-1]["guesses"].append(guess)

    # Test that the function returns the correct list of guesses made in the current round for the specified team
    result_guesses = get_current_wordle_round_guesses_by_team(team_ID)
    test(
        "The function should return the correct list of guesses made in the current round for the specified team.",
        guesses,
        result_guesses,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_guesses_by_team()

def test_get_used_wordle_words() -> None:
    """
        Test whether the function which returns a set of all used Wordle words across all teams and rounds works correctly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being rounds for the teams
    initialize_teams_data()
        
    team_amount = get_amount_of_teams()

    used_words = set()

    # We add multiple rounds for each team and keep track of the words which the team needs to guess
    for team_ID in range(team_amount):
        for _ in range(2):
            add_single_initial_rounds_info_for_team(team_ID)
            word_to_guess = teams_data[team_ID]["roundsInfo"][-1]["wordToGuess"]
            used_words.add(word_to_guess)

    # Test that the function returns the correct set of used Wordle words across all teams and rounds
    result_used_words = get_used_wordle_words()
    test(
        "The function should return the correct set of used Wordle words across all teams and rounds.",
        used_words,
        result_used_words,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_used_wordle_words()

def test_get_random_word() -> None:
    """
        Test whether the function which returns a random Wordle word that hasn't been used yet works correctly.
    """

    # First we initialize the teams data to ensure we have the rounds to work with.
    # This is needed since the function being tested relies on there being used words
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Add a single round to simulate that a random word has been used
    add_single_initial_rounds_info_for_team(team_ID)
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)


    # Test whether the function returns a random word that hasn't been used yet without raising an exception
    test_message = "The function should return a random Wordle word that hasnt been used yet without raising an exception."
    try:
        get_random_word()
        test(
            test_message,
            True,
            True
        )
    except IndexError as e:
        test(
            test_message,
            False,
            True
        )

    # Test whether the function raises an IndexError when all available words have been used
    try:
        get_random_word([word_to_guess])
    except IndexError:
        test(
            "The function should raise an IndexError when all available Wordle words have been used.",
            True,
            True
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_random_word()

def test_get_current_wordle_round_guesses_color_for_team() -> None:
    """
        Test whether the function which returns the colors of the guesses made in the current round for the specified team works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being a current round for the specified team
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)

    wordle_guess_colors = get_available_letter_position_colors()
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)

    # We set an incorrect guess and the expected colors for that guess to simulate a failed attempt
    incorrect_guess = word_to_guess[::-1]
    incorrect_guess_colors = list(incorrect_guess)
    for index, letter in enumerate(incorrect_guess_colors):
        word_to_guess_letter = word_to_guess[index]
        if letter == word_to_guess_letter:
            incorrect_guess_colors[index] = wordle_guess_colors["correct"]
            continue

        if letter in word_to_guess:
            incorrect_guess_colors[index] = wordle_guess_colors["misplaced"]
            continue

        incorrect_guess_colors[index] = wordle_guess_colors["incorrect"]

    # First add the incorrect guess followed by the correct guess to simulate two attempts
    #! Do note that we must ALWAYS add the correct guess last.
    #! This is needed since otherwise we get an IndexError since we usually go to the next round after guessing correctly
    guesses = [
        incorrect_guess,
        word_to_guess
    ]
    guesses_colors = [
        incorrect_guess_colors,
        [wordle_guess_colors["correct"] for _ in word_to_guess]
    ]

    # Add the guesses to the current round for the specified team.
    current_wordle_round = teams_data[team_ID]["roundsInfo"][-1]

    # Clean up any existing guesses and colors before adding our simulated ones
    current_wordle_round["guesses"] = []
    current_wordle_round["guessesColor"] = []

    for attempt_number, guess in enumerate(guesses):
        current_wordle_round["guesses"].append(guess)
        current_wordle_round["guessesColor"].append(guesses_colors[attempt_number])

    # Test that the function returns the correct colors of the guesses made in the current round for the specified team
    result_guesses_colors = get_current_wordle_round_guesses_color_for_team(team_ID)
    test(
        "The function should return the correct colors of the guesses made in the current round for the specified team.",
        guesses_colors,
        result_guesses_colors,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_guesses_color_for_team()

def test_get_letter_color_for_current_round_last_guessed_word_by_team() -> None:
    """
        Test whether the function which returns the colors of the letters in the last guessed word in the current round for the specified team works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being a current round for the specified team
    initialize_teams_data()

    # After we initialize the teams data, we add a single Wordle round for the starting team
    add_single_initial_rounds_info_for_team(team_ID)


    # First we remove any existing guesses and colors to start fresh
    current_wordle_round = teams_data[team_ID]["roundsInfo"][-1]
    current_wordle_round["guesses"] = []
    current_wordle_round["guessesColor"] = []


    # Add the maximum number of guesses with known colors to the current round for the specified team.
    wordle_guess_colors = get_available_letter_position_colors()
    max_attempts = get_max_wordle_guess_attempts()
    
    guesses_colors = []
    for _ in range(max_attempts):
        word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
        
        while True:
            guess = choice(five_letter_words.words)
            teams_data[team_ID]["roundsInfo"][-1]["guesses"].append(guess)

            if guess != word_to_guess:
                break
        
        guess_colors = list(guess)
        for index, letter in enumerate(guess_colors):
            word_to_guess_letter = word_to_guess[index]
            if letter == word_to_guess_letter:
                guess_colors[index] = wordle_guess_colors["correct"]
                continue

            if letter in word_to_guess:
                guess_colors[index] = wordle_guess_colors["misplaced"]
                continue

            guess_colors[index] = wordle_guess_colors["incorrect"]

        guesses_colors.append(guess_colors)
        teams_data[team_ID]["roundsInfo"][-1]["guessesColor"].append(guess_colors)
    

    # Test that the function returns the correct color for the letter at the specified position
    used_test_positions = set()
    for _ in range(max_attempts):
        while True:
            row_index = choice(range(max_attempts))
            col_index = choice(range(len(word_to_guess)))
            position = (row_index, col_index)
            if position not in used_test_positions:
                used_test_positions.add(position)
                break
        
        expected_color = guesses_colors[row_index][col_index]
        result_color = get_letter_color_for_current_round_last_guessed_word_by_team(team_ID, position)
        test(
            f"The function should return the correct color for the letter at position {position} in the current round's last guessed words",
            expected_color,
            result_color,
        )

    # Test whether we return the default color for an out-of-bounds position
    out_of_bounds_position = (max_attempts + 1, 0)  # Row index is out of bounds
    expected_color = wordle_guess_colors['default']
    result_color = get_letter_color_for_current_round_last_guessed_word_by_team(team_ID, out_of_bounds_position)
    test(
        f"The function should return the default color for an out-of-bounds position {out_of_bounds_position}",
        expected_color,
        result_color,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_letter_color_for_current_round_last_guessed_word_by_team()

def test_get_guess_letters_color_based_on_word_to_guess() -> None:
    """
        Test whether the function which returns the colors of the letters in a guess based on the word to guess works correctly.
    """

    wordle_letter_colors = get_available_letter_position_colors()
    word_to_guess = "crane"
    guess = "cater"
    expected_colors = [
        wordle_letter_colors["correct"],
        wordle_letter_colors["misplaced"],
        wordle_letter_colors["incorrect"],
        wordle_letter_colors["misplaced"],
        wordle_letter_colors["misplaced"]
    ]
    result = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    test(
        f"The colors returned should be green, yellow, and red for correct, misplaced, and incorrect letters respectively. for the word 'crane' and guess 'cater'",
        expected_colors,
        result,
    )

    word_to_guess = "magen"
    guess = "meren"
    expected_colors = [
        wordle_letter_colors["correct"],
        wordle_letter_colors["incorrect"],
        wordle_letter_colors["incorrect"],
        wordle_letter_colors["correct"],
        wordle_letter_colors["correct"]
    ]
    result = get_guess_letters_color_based_on_word_to_guess(guess, word_to_guess)
    test(
        f"The colors returned should be green, yellow, and red for correct, misplaced, and incorrect letters respectively. for the word 'magen' and guess 'meren'",
        expected_colors,
        result,
    )


test_get_guess_letters_color_based_on_word_to_guess()

def test_get_current_wordle_round_board_for_team() -> None:
    """
        Test whether the function which returns the Wordle board for the current round for the specified team works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being a current round for the specified team
    initialize_teams_data()

    add_single_initial_rounds_info_for_team(team_ID)

    # Test whether when we show the initial board, it shows the first letter of the word to guess and empty placeholders for the rest of the columns and rows
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    max_attempts = get_max_wordle_guess_attempts()
    empty_column_placeholder = get_empty_column_placeholder_for_wordle_board()
    expected_board = [[word_to_guess[0]] + [empty_column_placeholder] * (len(word_to_guess) - 1)] + [[empty_column_placeholder] * len(word_to_guess) for _ in range(max_attempts - 1)]
    result_board = get_current_wordle_round_board_for_team(team_ID)
    test(
        "The initial Wordle board for the current round should show the first letter of the word to guess and empty placeholders for the rest of the columns and rows.",
        expected_board,
        result_board,
    )

    # Test whether after adding some guesses, the board shows the correct letters in the correct positions
    guesses = ["12345", "67890"]
    for attempt_number, guess in enumerate(guesses):
        add_guess_to_current_round_for_team(team_ID, guess, attempt_number)
        expected_board[attempt_number] = list(guess)

    result_board = get_current_wordle_round_board_for_team(team_ID)
    test(
        "After adding some guesses, the Wordle board for the current round should show the correct letters in the correct positions.",
        expected_board,
        result_board,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_get_current_wordle_round_board_for_team()

def test_add_single_initial_rounds_info_for_team() -> None:
    """
        Test whether the function which adds a single initial Wordle round info for the specified team works correctly.
    """

    # First we initialize the teams data to ensure we have the global dictionary to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # Get the amount of rounds before adding a new one
    initial_rounds_count = len(teams_data[team_ID]["roundsInfo"])

    # Add a single initial round for the specified team
    add_single_initial_rounds_info_for_team(team_ID)

    # Test that the rounds info for the specified team has increased by one
    expected_rounds_count = initial_rounds_count + 1
    result_rounds_count = len(teams_data[team_ID]["roundsInfo"])
    test(
        "After adding a single initial Wordle round info for the specified team, the rounds info count should increase by one.",
        expected_rounds_count,
        result_rounds_count,
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_add_single_initial_rounds_info_for_team()

def test_is_valid_wordle_guess() -> None:
    """
        Test whether the function which checks if a Wordle guess is valid works correctly.
    """

    # First we initialize the teams data to ensure we have the round to work with
    initialize_teams_data()
        
    team_ID = get_starting_team_ID()

    # After we initialize the teams data, we add a single Wordle round for the specified team
    add_single_initial_rounds_info_for_team(team_ID)

    # Test that a valid guess returns True
    word_to_guess = get_current_wordle_round_word_to_guess_for_team(team_ID)
    expected_validation_result = {
        'isValid': True,
        'message': ''
    }
    validation_result = is_valid_wordle_guess(word_to_guess, team_ID)
    for key in expected_validation_result:
        test(
            f"The function should return {expected_validation_result[key]} for a valid Wordle guess for the key '{key}'.",
            expected_validation_result[key],
            validation_result[key],
        )

    # Test that an invalid guess (wrong length) returns False with the correct message
    invalid_length_guess = word_to_guess + "s"
    expected_validation_result = {
        'isValid': False,
        'message': f"The guess must be exactly {len(word_to_guess)} letters long."
    }
    validation_result = is_valid_wordle_guess(invalid_length_guess, team_ID)
    for key in expected_validation_result:
        test(
            f"The function should return {expected_validation_result[key]} for an invalid Wordle guess (wrong length) for the key '{key}'.",
            expected_validation_result[key],
            validation_result[key],
        )

    # Test that an invalid guess (not in word list) returns False with the correct message
    invalid_word_guess = "zzzzz"
    expected_validation_result = {
        'isValid': False,
        'message': "The guess is not a valid Wordle word."
    }
    validation_result = is_valid_wordle_guess(invalid_word_guess, team_ID)
    for key in expected_validation_result:
        test(
            f"The function should return {expected_validation_result[key]} for an invalid Wordle guess (not in word list) for the key '{key}'.",
            expected_validation_result[key],
            validation_result[key],
        )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_is_valid_wordle_guess()

def test_has_team_lost_wordle_game() -> None:
    """
        Test whether the function which checks if a team has lost the Wordle game works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being rounds for the specified team
    initialize_teams_data()

    # After we initialize the teams data, we add multiple Wordle rounds for the specified team
    wordle_lose_conditions = get_wordle_lose_conditions()
    rounds_to_lose = wordle_lose_conditions["rounds_lost_in_a_row"]
    max_guesses = get_max_wordle_guess_attempts()
    for round_index in range(rounds_to_lose):
        add_single_initial_rounds_info_for_team(team_ID)

        # Add the maximum number of incorrect guesses to simulate losing the round
        word_to_guess = teams_data[team_ID]["roundsInfo"][round_index]["wordToGuess"]
        incorrect_guess = word_to_guess[::-1] # Just reverse the word to ensure it is incorrect, even if it isn't a valid word
        for _ in range(max_guesses):
            teams_data[team_ID]["roundsInfo"][round_index]["guesses"].append(incorrect_guess)

    test(
        f"The team should have lost the Wordle game after losing {rounds_to_lose} rounds in a row.",
        True,
        has_team_lost_wordle_game(team_ID),
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_lost_wordle_game()

def test_has_team_won_wordle_game() -> None:
    """
        Test whether the function which checks if a team has won the Wordle game works correctly.
    """

    team_ID = get_starting_team_ID()

    # First we initialize the teams data to ensure we have the round to work with.
    # This is needed since the function being tested relies on there being rounds for the specified team
    initialize_teams_data()

    # After we initialize the teams data, we add multiple Wordle rounds for the specified team
    rounds_to_win = get_wordle_win_conditions()["rounds_won"]
    for round_index in range(rounds_to_win):
        add_single_initial_rounds_info_for_team(team_ID)

        # Simulate that the team has won the round by guessing the correct word
        word_to_guess = teams_data[team_ID]["roundsInfo"][round_index]["wordToGuess"]
        teams_data[team_ID]["roundsInfo"][round_index]["guesses"].append(word_to_guess)

    test(
        f"The team should have won the Wordle game after winning {rounds_to_win} rounds.",
        True,
        has_team_won_wordle_game(team_ID),
    )

    # Remove the teams data after the test to reset the state for other tests
    remove_teams_data()
test_has_team_won_wordle_game()

def test_get_max_wordle_guess_attempts() -> None:
    """
        Test whether the function which returns the maximum number of Wordle guess attempts works correctly.
    """

    expected_max_attempts = 5
    result_max_attempts = get_max_wordle_guess_attempts()
    test(
        "The maximum number of Wordle guess attempts should be 5.",
        expected_max_attempts,
        result_max_attempts,
    )
test_get_max_wordle_guess_attempts()

def test_get_available_letter_position_colors() -> None:
    """
        Test whether the function which returns the available letter position colors for Wordle works correctly.
    """

    expected_colors = {
        "correct": "green",
        "misplaced": "yellow",
        "incorrect": "red",
        "default": "white"
    }
    result_colors = get_available_letter_position_colors()
    for key in expected_colors:
        expected_color = expected_colors[key]
        test(
            f"The color for when a letter is on the '{key}' position should be '{expected_color}'.",
            expected_color,
            result_colors[key],
        )
test_get_available_letter_position_colors()

def test_get_wordle_win_conditions() -> None:
    """
        Test whether the function which returns the Wordle win conditions works correctly.
    """

    expected_win_conditions = {
        "rounds_won": 10
    }
    result_win_conditions = get_wordle_win_conditions()
    for key in expected_win_conditions:
        expected_value = expected_win_conditions[key]
        test(
            f"The Wordle win condition for '{key}' should be {expected_value}.",
            expected_value,
            result_win_conditions[key],
        )
test_get_wordle_win_conditions()

def test_get_wordle_lose_conditions() -> None:
    """
        Test whether the function which returns the Wordle lose conditions works correctly.
    """

    expected_lose_conditions = {
        "rounds_lost_in_a_row": 3
    }
    result_lose_conditions = get_wordle_lose_conditions()
    for key in expected_lose_conditions:
        expected_value = expected_lose_conditions[key]
        test(
            f"The Wordle lose condition for '{key}' should be {expected_value}.",
            expected_value,
            result_lose_conditions[key],
        )
test_get_wordle_lose_conditions()