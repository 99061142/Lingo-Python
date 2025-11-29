from lingo.bingo.bingo_settings.bingo_settings_utils import get_bingo_lose_conditions, get_bingo_win_conditions, get_maximum_grabs_per_round
from ..lingo_utils import print_message, set_winning_team, get_next_team_ID
from .bingo_utils import *
from time import sleep
from typing import Union
from random import choice

def print_bingo_board_for_team(team_ID: int) -> None:
    """
        Print the Bingo board for the specified team.
    """

    stringified_bingo_board = get_stringified_bingo_board_for_team(team_ID)
    print_message(stringified_bingo_board)

"""
    Grab a single ball for the specified team.
    The ball can either be a colored ball (red or green) or a number from the specified team's Bingo board.
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

    # If not, it means the team grabbed a number within their Bingo board.
    # In that case, we print the grabbed number, mark the number on the Bingo board, and return the grabbed number
    print_message(f"Team {team_ID + 1} grabbed ball number {grabbed_ball}!")
    mark_number_on_bingo_board_for_team(team_ID, grabbed_ball)
    return grabbed_ball

"""
    Play a Bingo round for the specified team.
"""
def play_bingo_round_for_team(team_ID: int) -> None:
    max_grab_attempts = get_maximum_grabs_per_round()
    win_conditions = get_bingo_win_conditions()
    lose_conditions = get_bingo_lose_conditions()

    green_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "green")
    red_balls_grabbed = get_amount_of_color_balls_grabbed_by_team(team_ID, "red")
    print_message(f"Team {team_ID + 1}, it's your turn to try to create a line on your Bingo board, or grab 3 green balls (current green balls: {green_balls_grabbed}. Current red balls: {red_balls_grabbed})!")
    
    print_bingo_board_for_team(team_ID)

    for attempt in range(1, max_grab_attempts + 1):
        print_message(f"Team {team_ID + 1}, it's your {attempt} attempt to grab a ball! Attempt {attempt}/{max_grab_attempts}.")
        
        grabbed_ball = grab_bingo_ball_for_team(team_ID)
    
        # If the team has grabbed the maximum amount of red balls to lose the bingo game, we print the lose message, set the next team as the winning team, and return
        red_balls_needed_to_lose = lose_conditions["red_balls_grabbed"]
        if get_amount_of_color_balls_grabbed_by_team(team_ID, "red") >= red_balls_needed_to_lose:
            message = f"Team {team_ID + 1} has grabbed {red_balls_needed_to_lose} red balls and loses the bingo game!"
            message_color = "red"
            print_message(message, message_color)

            #! Do note that this expects there to be only 2 teams playing the Lingo game
            next_team_ID = get_next_team_ID(team_ID)
            set_winning_team(next_team_ID)
            return

        # If the grabbed ball is red, and it's not the last attempt, end the bingo turn early
        if grabbed_ball == "red" and attempt != max_grab_attempts:
            message = f"Team {team_ID + 1} grabbed a red ball and ends their bingo turn early!"
            message_color = "red"
            print_message(message, message_color)
            break
        
        # If the grabbed ball is a number, we print the updated bingo board for the team
        if type(grabbed_ball) is int:
            print_bingo_board_for_team(team_ID)

            # If the team has completed enough lines to win the bingo game, we print the win message, set the current team as the winning team, and return
            lines_needed_to_win = win_conditions["lines_needed"]
            if get_bingo_board_total_filled_lines_amount_for_team(team_ID) >= lines_needed_to_win:
                message = f"Team {team_ID + 1} has completed {lines_needed_to_win} line(s) on their bingo board and wins the bingo game!"
                message_color = "green"
                print_message(message, message_color)

                set_winning_team(team_ID)
                return

        # Check if the team has grabbed enough green balls to win the bingo game, 
        # and if so, print the win message, set the current team as the winning team, and return
        green_balls_needed_to_win = win_conditions["green_balls_grabbed"]
        if grabbed_ball == "green" and get_amount_of_color_balls_grabbed_by_team(team_ID, "green") >= green_balls_needed_to_win:
            message = f"Team {team_ID + 1} has grabbed {green_balls_needed_to_win} green balls and wins the bingo game!"
            message_color = "green"
            print_message(message, message_color)

            set_winning_team(team_ID)
            return