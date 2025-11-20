from app.app_utils import print_message, set_winning_team
from .bingo_utils import *
from time import sleep
from typing import Union

"""
    Print the bingo board for the specified team.
"""
def print_bingo_board_for_team(team_ID: int) -> None:
    stringified_bingo_board = get_stringified_bingo_board_for_team(team_ID)
    print_message(stringified_bingo_board)

"""
    Grab a single ball for the specified team.
    The ball can either be a colored ball (red or green) or a number from the bingo board.
    It handles updating the team's data accordingly.
"""
def grabble_single_ball(team_ID: int) -> Union[str, int]:
    available_balls = get_available_bingo_board_pit_balls_for_team(team_ID)
    grabbed_ball = get_random_number(available_balls)
    
    print_message(f"Team {team_ID + 1} is grabbing a ball...")
    sleep(1)  # Simulate time taken to grab a ball

    # If the parameter is a string, it means the team grabbed a colored ball (red or green).
    # We print the grabbed color ball and decrease the remaining color balls for the team, and increase the grabbed color balls.
    if type(grabbed_ball) is str:
        print_message(f"Team {team_ID + 1} grabbed a {grabbed_ball} colored ball!")
        decrease_remaining_color_balls_for_team(team_ID, grabbed_ball)
        return grabbed_ball

    # If not, it means the team grabbed a number from the bingo board.
    # We print the grabbed number and mark it on the bingo board.
    print_message(f"Team {team_ID + 1} grabbed ball number {grabbed_ball}!")
    mark_number_on_bingo_board(team_ID, grabbed_ball)
    return grabbed_ball

"""
    Play a bingo round for the specified team.
"""
def play_bingo_round_for_team(team_ID: int) -> None:
    # Hardcoded maximum grab attempts per bingo round
    max_grab_attempts = 2

    # Print the initial message and bingo board for the team
    print_message(f"Team {team_ID + 1}, it's your turn to try to create a line on your bingo board, or grab 3 green balls (current green balls: {get_amount_of_color_balls_grabbed(team_ID, 'green')})!")
    print_bingo_board_for_team(team_ID)

    # Loop for the maximum grab attempts
    for attempt in range(1, max_grab_attempts + 1):
        print_message(f"Team {team_ID + 1}, it's your {attempt} attempt to grab a ball! Attempt {attempt}/{max_grab_attempts}.")
        
        # Grab a single ball for the team
        grabbled_ball = grabble_single_ball(team_ID)
    
        # If the grabbed ball is red, and it's not the last attempt, end the bingo turn early.
        if grabbled_ball == "red" and attempt != max_grab_attempts:
            print_message(f"Team {team_ID + 1} grabbed a red ball and ends their bingo turn early!")
            break
        
        print_bingo_board_for_team(team_ID)

        # If the player has won the bingo game, we return early.
        if did_team_win_bingo_game(team_ID):
            return