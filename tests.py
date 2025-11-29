from test_lib import report

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for this application
import lingo.lingo_tests

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Wordle minigame
import lingo.wordle.wordle_tests

#! DO NOT DELETE THIS IMPORT, EVEN IF PYLANCE SAYS IT IS UNUSED.
#! This import runs all the tests for the Bingo minigame
import lingo.bingo.bingo_tests

# Report all test results for this application
report()