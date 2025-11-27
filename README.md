# Lingo
This is my end project assignment for year 1 of my college course in Software Developer.

## Why didn't I make use of classes?
Because of the rule that I can only make use of whatever the class did learn within Python in our first year, I can't use classes. Even if I understand classes, it still isn't allowed. This is because the class have only learned up to the use of functions/lambda's.

## Win conditions (One or more of the following options:)
* The team has grabbed 3 green balls within the Bingo ball pit.
* The team has a vertical, horizontal or diagonal line on the Bingo board.
* The team has guessed 10 words correctly within the Wordle game.

## Lose conditions (One or more of the following options:)
* The team has grabbed 3 red balls within the Bingo ball pit.
* The team didn't guess the Wordle word for 3 rounds straight.

## Functionality
* The Wordle game generates a random word within the given 5 letter word list. This word needs to be guessed by the current team.
* The Wordle game shows the first letter for the word that needs to be guessed.
* The team gets 5 attempts to guess the word within the Wordle game.
* After each attempt the user can see if some letters within the guessed word are on the correct position (green), incorrect position (yellow) or not in the word which needs to be guessed at all (red).
* After each attempt to guess the Wordle word, the correctly guessed letters are shown on the row of the next round. EXCEPT when the user guessed the word correctly.
* When a player guessed the Wordle word, they need to rummuge in the Bingo ball pit for 2 balls to try to get a vertical, horizontal or diagonal line on the 4x4 bingo board.
  * The Bingo ball pit has 3 green balls, 3 red balls, and 16 numbers (based on the 4x4 bingo board). The numbers on the Bingo board are even for team 1, and uneven for team 2.
  * If the player grabbed a red ball on the first attempt, they can not grab a second ball.
* At the end of the Lingo game (when a team lost or won), we ask if they want to play again.
