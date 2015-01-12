# coding=utf-8
"""
Contains the code for the artwork of hangman.
"""
__author__ = 'Debojeet_Chatterjee'
from colorama import init, Fore, Style

init()

HANGMAN_PICS = [
    """
         +====++
         |    ||
              ||
              ||
              ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
              ||
              ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
         |    ||
              ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
        /|    ||
              ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
        /|\\   ||
              ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
        /|\\   ||
         |    ||
              ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
        /|\\   ||
         |    ||
        /     ||
        ______||
    """,
    """
         +====++
         |    ||
         O    ||
        /|\\   ||
         |    ||
        / \\   ||
        ______||
    """,
]

LIFE = "? "  # "♥ "

POINT = "$ "  # "♦ "

MAX_SCORE_LINE = 7  # max no. of points in a row.


def draw_game_board(word, lives, score):
    """
    redraw each time when a turn begins.
    Note:   tried doing strikethrough but to no avail.
            unable to clear previous output on stdout.
            /r only returns to the head of the current line.
    """
    print Fore.RESET + Style.RESET_ALL,
    print "\n\t**HANGMAN**"
    print "\t(c) debowin"
    print "Hints:\t",
    print Fore.RED + Style.BRIGHT + LIFE * lives + Fore.RESET + Style.RESET_ALL
    print "Score:\t",
    score_lines = score/MAX_SCORE_LINE
    for score_line in range(score_lines):
        print Fore.GREEN + Style.BRIGHT + POINT * MAX_SCORE_LINE
        print "\t",
    print Fore.GREEN + Style.BRIGHT + POINT * (score % MAX_SCORE_LINE)
    print Fore.YELLOW + Style.DIM + HANGMAN_PICS[len(word.misses)] + Fore.RESET + Style.RESET_ALL
    print "Word:\t",
    print Fore.CYAN + Style.BRIGHT + "".join(word.guessed) + Fore.RESET + Style.RESET_ALL
    print "Miss:\t",
    print Fore.YELLOW + Style.BRIGHT + ", ".join(word.misses) + Fore.RESET + Style.RESET_ALL