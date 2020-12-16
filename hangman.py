# Problem Set 2, hangman.py
# Name: Bogdan Zadorozhny
# Group: KM-02
# Hangman Game
# -----------------------------------
import random
import string

INITIAL_TRIES = 6
INITIAL_WARN = 3
NOT_GUESSED_LETTER = "_"
HINT = "*"
VOWELS_LIST = {"a", "e", "i", "o", "u"}
WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: set (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            return True
    return False


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: set (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    compared_list = []
    for i in secret_word:
        if i in letters_guessed:
            compared_list.append(i)
        elif i not in letters_guessed:
            compared_list.append(NOT_GUESSED_LETTER + " ")
    return "".join(compared_list)


def get_available_letters(letters_guessed):
    """
    letters_guessed: set (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    alphabets = string.ascii_lowercase
    compared_list = [i for i in alphabets if i not in letters_guessed]
    return "".join(compared_list)


def spend_warn(warn, tries):
    """
    warn: integer, amount of warnings
    tries: integer, amount of tries
    This function deletes one warning or a try if there isn't any tries.
    returns: tuple with amount of warnings and tries.
    """
    if warn > 0:
        warn -= 1
    else:
        warn -= 1
        tries -= 1
    return warn, tries


def vowel_check(letter, tries):
    """
        letter: string, entered letter
        warn: integer, amount of warnings
        tries: integer, amount of tries
        This function deletes two tries if entered letter is a vowel, or one if not.
        returns: amount of tries.
    """
    if letter in VOWELS_LIST:
        tries -= 2
    else:
        tries -= 1
    return tries


def check_element(tries, warn, letters_guessed, word, letter):
    """
        tries: integer, amount of tries
        warn: integer, amount of warnings
        letters_guessed: list with elements which have been entered so far
        word: string, comprised of letters, underscores (_), and spaces that represents which letters in secret_word
        have been guessed so far
        letter: string, entered symbol
        This function checks if the entered symbol is a letter. If it's a letter, the program shows if the letter is
        guessed. If entered symbol was entered before or it isn't a letter, program shows a warning.
        returns: tuple with amount of tries and warnings, list with elements which have been entered so far and string,
                 comprised of letters, underscores (_), and spaces that represents which letters in secret_word have
                 been guessed so far
    """
    # If the entered symbol has already been used, this part shows a warning
    if letter in letters_guessed:
        warn, tries = spend_warn(warn, tries)
        # This output changes depending on if the entered symbol is "*" or a letter and how many warnings are left
        print(f"Oops! You've already guessed that letter. You have {warn if warn >= 0 else 'no'} "
              f"warnings left{' so you lose one guess' if warn < 0 else ''}: {word}")

    # If the entered symbol isn't a letter, this part shows a warning
    elif letter not in set(string.ascii_lowercase):
        warn, tries = spend_warn(warn, tries)
        print(f"Oops! That is not a valid letter. You have {warn if warn >= 0 else 'no'} warnings left: {word}")

    # If the entered symbol is a letter and it's in the secret word, the program shows that the letter is guessed
    elif letter in set(secret_word):
        letters_guessed.add(letter)
        word = get_guessed_word(secret_word, letters_guessed)
        print("Good guess:", word)
        letters_guessed.add(letter)

    # If the entered symbol is a letter and it isn't in the secret word, the program shows that the letter
    # isn't guessed and user loses one try if it isn't a vowel letter or two if it's.
    elif letter not in set(secret_word):
        tries = vowel_check(letter, tries)
        print("Oops! That letter is not in my word:", word)
        letters_guessed.add(letter)
    return tries, warn, letters_guessed, word


def start_message(secret_word, hints):
    """
        secret_word: string, the word the user is guessing
        hints: boolean, hints are turned on or off
        This function shows a starting message.
    """
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have 6 warnings left.")
    if hints:
        print('You can also use a hint. Enter "*" to use it.')
    return


def game_round(letters_guessed, tries):
    """
        letters_guessed: list with elements which have been entered so far
        tries: integer, amount of tries
        This function shows a game round message and asks player to guess a letter.
        returns: string, entered symbol
    """
    print("-" * 13)
    print(f"You have {tries} guesses left.")
    print("Available letters:", get_available_letters(letters_guessed))
    letter = input("Please guess a letter: ").lower()
    return letter


def end_message(secret_word, tries):
    """
        secret_word: string, the word the user is guessing
        tries: integer, amount of tries
        This function shows a game over message.
    """
    print("-" * 13)
    if tries == 0:
        print('Sorry, you ran out of guesses. The word was "' + secret_word + '".')
    else:
        print("Congratulations, you won! Your total score for this game is:", tries * len(set(secret_word)))
    return


def hangman(secret_word, hints=False):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    tries = INITIAL_TRIES
    warn = INITIAL_WARN
    # List "letters_guessed" is used as a container for letters which have already been guessed
    letters_guessed = set()
    # Variable "word" shows the length of the secret word and which letters have already been guessed
    word = get_guessed_word(secret_word, letters_guessed)
    start_message(secret_word, hints)

    while tries != 0 and is_word_guessed(secret_word, word):
        letter = game_round(letters_guessed, tries)
        if len(letter) == 1:
            # If the entered symbol is a "*", the program uses a hint and shows all possible matches
            if hints and letter == HINT:
                show_possible_matches(word)
            else:
                tries, warn, letters_guessed, word = check_element(tries, warn, letters_guessed, word, letter)

        # If user enters more or less than one symbol, the program issues a warning
        else:
            warn, tries = spend_warn(warn, tries)
            print(f"Oops! Don't enter more or less than one symbol. You have {warn if warn >= 0 else 'no'} "
                  f"warnings left{' so you lose one guess' if warn < 0 else ''}: {word}")

    end_message(secret_word, tries)
    return


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    # This loop compares my_word, which consists of "_ " and letters which have already been guessed, with words
    # from file "words.txt". If these two words have the same length and letters from my_word have the same
    # position in the compared word, loop returns True. Otherwise, it returns False.
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] != NOT_GUESSED_LETTER and (
                    my_word[i] != other_word[i] or my_word.count(my_word[i]) != other_word.count(other_word[i])):
                return False
        return True
    return False


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    replaced_word = my_word.replace(" ", "")
    matches = [word for word in wordlist if match_with_gaps(replaced_word, word)]
    if not matches:
        print("No matches found.\n")
    else:
        print("Possible word matches are: " + ", ".join(matches), end="." + "\n")
    return


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    hangman(secret_word, True)
    return


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
