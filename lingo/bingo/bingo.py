from ..lingo_utils import print_message
from .bingo_utils import *
from time import sleep
from typing import Union
from random import choice

"""
    Print the bingo board for the specified team.
"""
def print_bingo_board_for_team(team_ID: int) -> None:
    stringified_bingo_board = get_stringified_bingo_board_for_team(team_ID)
    print_message(stringified_bingo_board)

"""
    Grab a single ball for the specified team.
    The ball can either be a colored ball (red or green) or a number from the specified team's bingo board.
    This function also updates the teams_data structure accordingly based on the grabbed ball.
"""
def grab_bingo_ball_for_team(team_ID: int) -> Union[str, int]:
    available_balls = get_available_bingo_board_pit_balls_for_team(team_ID)
    grabbed_ball = choice(available_balls)
    
    print_message(f"Team {team_ID + 1} is grabbing a ball...")
    sleep(1)  # Simulate time taken to grab a ball

    # If the parameter is a string, it means the team grabbed a colored ball (red or green).
    # In that case, we print the grabbed color, update the teams_data structure for the grabbed and remaining balls, and return the grabbed color
    if type(grabbed_ball) is str:
        print_message(f"Team {team_ID + 1} grabbed a {grabbed_ball} colored ball! (Current {grabbed_ball} balls grabbed: {get_amount_of_color_balls_grabbed_by_team(team_ID, grabbed_ball) + 1})")
        decrease_remaining_color_balls_for_team(team_ID, grabbed_ball)
        increase_grabbed_color_balls_for_team(team_ID, grabbed_ball)
        return grabbed_ball

    # If not, it means the team grabbed a number within their bingo board.
    # In that case, we print the grabbed number, mark the number on the bingo board, and return the grabbed number
    print_message(f"Team {team_ID + 1} grabbed ball number {grabbed_ball}!")
    mark_number_on_bingo_board_for_team(team_ID, grabbed_ball)
    return grabbed_ball

"""
    Play a bingo round for the specified team.
"""
def play_bingo_round_for_team(team_ID: int) -> None:
    # Hardcoded maximum grab attempts per bingo round
    max_grab_attempts = 2

    # Print the initial message and bingo board for the team
    print_message(f"Team {team_ID + 1}, it's your turn to try to create a line on your bingo board, or grab 3 green balls (current green balls: {get_amount_of_color_balls_grabbed_by_team(team_ID, 'green')})!")
    print_bingo_board_for_team(team_ID)

    # Let the team grab the maximum amount of balls for their bingo round
    for attempt in range(1, max_grab_attempts + 1):
        print_message(f"Team {team_ID + 1}, it's your {attempt} attempt to grab a ball! Attempt {attempt}/{max_grab_attempts}.")
        
        grabbed_ball = grab_bingo_ball_for_team(team_ID)
    
        # If the team has grabbed 3 red balls, they lose the bingo game
        if get_amount_of_color_balls_grabbed_by_team(team_ID, "red") >= 3:
            fail_message = f"Team {team_ID + 1} has grabbed 3 red balls and loses the bingo game!"
            print_color = "red"
            print_message(fail_message, print_color)
            return

        # If the grabbed ball is red, and it's not the last attempt, end the bingo turn early
        if grabbed_ball == "red" and attempt != max_grab_attempts:
            fail_message = f"Team {team_ID + 1} grabbed a red ball and ends their bingo turn early!"
            print_color = "red"
            print_message(fail_message, print_color)
            break
        
        # If the grabbed ball is a number, we print the updated bingo board for the team
        if type(grabbed_ball) is int:
            print_bingo_board_for_team(team_ID)

        # If the player has won the bingo game, we print the win message and return early
        if has_team_won_bingo_game(team_ID):
            if grabbed_ball == "green":
                win_message = f"Team {team_ID + 1} has grabbed 3 green balls and wins the bingo game!"
            else:
                win_message = f"Team {team_ID + 1} has completed a line on their bingo board and wins the bingo game!"

            print_color = "green"
            print_message(win_message, print_color)
            return