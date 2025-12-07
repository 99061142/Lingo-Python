from test_lib import report

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Lingo utility functions. Do note that this doesn't include the Wordle or Bingo utility functions
import lingo.lingo_tests

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Wordle minigame
import lingo.wordle.wordle_tests

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Bingo minigame
import lingo.bingo.bingo_tests

#! Do NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Wordle words utility functions
import lingo.wordle.words.words_tests

# Report all test results for this application
report()