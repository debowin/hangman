"""
Contains the code for playing the hangman game.

GRE Words [ADD]
Multi Input: Quick Entry [DONE]
"""
import random
from colorama import Fore, Style
import re
import sqlite3

__author__ = 'Debojeet_Chatterjee'
import hangman_art

LIVES = 7  # used for hints.
REWARD_SCORE = 3  # For each REWARD_SCORE number of points, player gets a life.
EASY_MODE = True  # If True, the first hint is already known.
WORD_LIST = []

# ****************************************** temp use only ************************************************************
# word_list = ['ant', 'baboon', 'badger', 'bat', 'bear', 'beaver', 'camel', 'cat', 'clam', 'cobra', 'cougar', 'coyote',
# 'crow', 'deer', 'dog', 'koala bear', 'leopard seal', 'mountain lion',
# 'donkey', 'duck', 'eagle', 'ferret', 'fox', 'frog', 'goat', 'goose', 'hawk', 'lion', 'lizard', 'llama',
# 'mole', 'monkey', 'moose', 'bull-dog', 'red ant',
#              'mouse', 'mule', 'newt', 'otter', 'owl', 'panda', 'parrot', 'pigeon', 'python', 'rabbit', 'ram', 'rat',
#              'raven', 'rhino', 'salmon', 'seal',
#              'shark', 'sheep', 'skunk', 'sloth', 'snake', 'spider', 'stork', 'swan', 'tiger', 'toad', 'trout',
#              'turkey', 'turtle', 'weasel', 'whale', 'wolf', 'wombat', 'zebra']
# ****************************************** temp use only ************************************************************


class Word(object):
    """
    the Word class contains all info about current word.
    Note: can't set member variables as private in Python.
    """

    def __init__(self):
        self.name = ""
        self.guessed = []
        self.hits = []  # list of hit letters
        self.misses = []  # list of fail letters
        self.available_hints = []  # year, actor; similar words.
        self.known_hints = []  # all the hints known to player

    def get_hint(self):
        """
        use a hint by popping it from available hints to known hints
        """
        randint = random.randint(0, len(self.available_hints)-1)
        hint = self.available_hints.pop(randint)
        if hint.startswith("Usage"):
            hint %= "_" * len(self.name)
        self.known_hints.append(hint)

    def get_arbitrary(self):
        """
        get a random word from word list.
        also populate hints
        """
        randint = random.randint(0, len(WORD_LIST)-1)
        word = WORD_LIST.pop(randint)
        self.name = word['name']
        self.available_hints = word['hints']
        self.known_hints = []
        self.guessed = list(re.sub(r'[a-zA-Z]', '_', self.name))
        if EASY_MODE:
            self.get_hint()
        self.misses = []
        self.hits = []

    def try_guess(self, guess_letters):
        """
        try out guess letters in the word.
        if it fits, add it in guessed. Return True.
        if not, add it to misses. Return False.
        """
        used = []
        used.extend(self.hits)
        used.extend(self.misses)
        for guess_letter in guess_letters:
            if guess_letter in used:
                continue
            if guess_letter in self.name.lower():
                self.hits.append(guess_letter)
                used.append(guess_letter)
                for i in range(len(self.name)):
                    if self.name[i].lower() == guess_letter:
                        self.guessed[i] = self.name[i]
            else:
                self.misses.append(guess_letter)
                used.append(guess_letter)
                if len(self.misses) == len(hangman_art.HANGMAN_PICS) - 1:
                    return


def player_input(word):
    """
    take input from user.
    """
    used_list = []
    used_list.extend(word.guessed)
    used_list.extend(word.misses)
    used_list = [x.lower() for x in used_list]
    guess_letters = ""
    valid_turn = False  # if not a single letter was accepted, repeat the turn
    while True:
        guess_letters = raw_input("Your guess[? for hint]: ").lower()
        if re.match(r'^[a-zA-Z]+$', guess_letters) is None:
            if guess_letters == '?':
                break
            print "Please enter only alphabets[or ?] as a guess."
            continue
        for guess_letter in guess_letters:
            if guess_letter in used_list:
                print "You have already used %s." % guess_letter
            else:
                valid_turn = True
        if valid_turn:
            break
    return guess_letters


def read_db(table_name):
    """
    reads rows from table_name and adds them to word_list
    """
    conn = sqlite3.connect('im.db')
    sql = "select * from %s" % table_name
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    if table_name == "MOVIES":
        for row in rows:
            word = {
                'name': row[1],
                'hints':
                [
                    "Plot:\t%s" % row[5],
                    "Actors:\t%s" % row[4],
                    "Genre:\t%s" % row[3],
                    "Year:\t%s" % row[2]
                ]
            }
            WORD_LIST.append(word)
    else:
        for row in rows:
            usage = re.sub(r'\{.+\}', '%s', row[4])
            word = {
                'name': row[1],
                'hints':
                [
                    "Type:\t%s" % row[2],
                    "Mean.:\t%s" % row[3],
                    "Usage:\t%s" % usage
                ]
            }
            WORD_LIST.append(word)


def main():
    """
    main function
    """
    read_db('MOVIES')  # MOVIES or WORDS
    word = Word()
    lives = LIVES
    score = 0
    still_playing = True
    while still_playing:
        # Game Loop
        word.get_arbitrary()
        while True:
            # Turn Loop
            if word.name == "".join(word.guessed):
                print "Nice Work!\nIt was\t" + Fore.CYAN + Style.BRIGHT + word.name + Fore.RESET + Style.RESET_ALL
                while len(word.available_hints) > 0:
                    word.get_hint()
                print "\n".join(word.known_hints)
                score += 1
                if score % REWARD_SCORE == 0 and lives < LIVES:
                    print "Congrats! You have been awarded a " + Fore.RED + Style.BRIGHT + "hint"
                    lives += 1
                break
            hangman_art.draw_game_board(word, lives, score)
            if len(word.misses) >= len(hangman_art.HANGMAN_PICS) - 1:
                print "Game Over!\nIt was\t" + Fore.CYAN + Style.BRIGHT + word.name + Fore.RESET + Style.RESET_ALL
                while len(word.available_hints) > 0:
                    word.get_hint()
                print "\n".join(word.known_hints)
                still_playing = False
                break
            print "\n".join(word.known_hints)
            guess_letters = player_input(word)
            if '?' in guess_letters:
                if lives > 0 and word.available_hints != []:
                    word.get_hint()
                    lives -= 1
                elif 'No hints left.' not in word.known_hints:
                    word.known_hints.append('No hints left.')
            else:
                word.try_guess(guess_letters)
    raw_input(Fore.RESET + Style.RESET_ALL + 'Press Enter')

if __name__ == "__main__":
    main()
