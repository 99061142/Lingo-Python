# Lingo
This is my end project assignment for year 1 of my college course in Software Developer.

## Why didn't I make use of classes, or any other 'non-basic' code?
Because of the rule that I can only make use of whatever we have learned within Python, I can't use classes. This is because we have only learned up to the use of functions/lambda's.

## Win conditions (One or more of the following options:)
* The team has grabbed 3 green balls within the bingo ball pit.
* The team has a vertical, horizontal or diagonal line on the bingo board.
* The team has guessed 10 words correctly.

## Lose conditions (One or more of the following options:)
* The team has grabbed 3 red balls within the bingo ball pit.
* The team didn't guess the word for 3 rounds straight.

## Needed functionality
* The letter 'y' is seen as two letters: 'i' and 'j'.
* The game generates a random word within the 5 letter word list, which needs to be guessed by the player.
* The game shows the first letter for the word that needs to be guessed.
* 1 team gets 5 tries to guess the word.
* After each attempt the user can see if their guessed word letters are on the correct position (green) or incorrect position (yellow).
* After each attempt, the correctly guessed letters needs to be filled in for the new row.
* When a player guessed the word, they need to rummuge in the ball pit for 2 balls to try to get a vertical, horizontal or diagonal line on the 4x4 bingo board.
  * The ball pit has 3 green balls, 3 red balls, and 16 numbers. The numbers are even for team 1, and uneven for team 2.
  * If the player grabbed a red ball on the first attempt, they can not grab a second ball.
* At the end of the game (when a team lost or won), we ask if they want to play again.
