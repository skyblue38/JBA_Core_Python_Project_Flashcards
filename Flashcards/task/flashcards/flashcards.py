""" JBA Python Core track
    Project: Flash Cards - Stage 7/7 - IMPORTant.
    Submitted by Chris Freeman"""

from os.path import exists
from random import choice
import argparse


live_log_filename = 'fcLiveLog.txt'     # filename for live logging


class Deck:
    """A dictionary representing a pile of FlashCards containing terms and their definitions"""

    def __init__(self):
        """Initiator for the Class - creates a flashcard deck instance"""
        self.pile = {}
        self.wcount = {}

    def __len__(self):
        """Method that return the number of flashcards in the deck"""
        return len(self.pile)

    def __iter__(self):
        return iter(self)

    def items(self):
        """Method that returns a list of term:defn tuples extracted from the deck"""
        return self.pile.items()

    def add_card(self, x_term, x_defn):
        """Method that will add a new Term:Definition pair to the Deck.
        If the term already exists in the Deck, it's definition will be updated"""
        self.pile[x_term] = x_defn
        self.wcount[x_term] = int(0)

    def remove_card(self, x_term):
        """Method that will remove a Term:Definition pair from the Deck.
        The Definition linked to the Term is returned.
        None is returned if the Term:Definition pair is not present"""
        self.wcount.pop(x_term, None)
        return self.pile.pop(x_term, None)

    def term_exists(self, x_term):
        """Method that will return True if the term is already in the Deck"""
        if x_term in self.pile.keys():
            return True
        return False

    def defn_exists(self, x_defn):
        """Method that will return True if the defn is already in the Deck"""
        if x_defn in self.pile.values():
            return True
        return False

    def get_term(self, x_defn):
        """Method that will return the Term associated with a given Definition,
        or None if Definition is not in the Deck."""
        for v_term, v_defn in self.pile.items():
            if x_defn == v_defn:
                return v_term
        return None


def print_and_log(f, s, end='\n'):
    """Print output to console from string 's' and record in logfile with descriptor 'f'."""
    print(s, end=end)
    try:
        f.write(s + '\n')
    except Exception as e:
        print("Error writing logfile:", e)


def input_and_log(f):
    """Accept input string from console and return it after writing to logfile with descriptor 'f' """
    inp = input()
    try:
        f.write(inp + '\n')
    except Exception as e:
        print('Error during logging input:', e)
    return inp


def m_add(x_deck, x_logf):
    """Handles the menu choice to add a flashcard to the deck"""
    print_and_log(x_logf, "The card:")
    while True:
        term = input_and_log(x_logf)
        if x_deck.term_exists(term):
            print_and_log(x_logf, f'The card "{term}" already exists. Try again:')
        else:
            break
    print_and_log(x_logf, 'The definition of the card:')
    while True:
        defn = input_and_log(x_logf)
        if x_deck.defn_exists(defn):
            print_and_log(x_logf, f'The definition "{defn}" already exists. Try again:')
        else:
            break
    x_deck.add_card(term, defn)
    print_and_log(x_logf, f'The pair ("{term}":"{defn}") has been added.')


def m_remove(x_deck, x_logf):
    """Handles the menu choice to remove a flashcard from the deck"""
    print_and_log(x_logf, "Which card:")
    x_term = input_and_log(x_logf)
    if x_deck.term_exists(x_term):
        x_deck.remove_card(x_term)
        print_and_log(x_logf, "The card has been removed.")
    else:
        print_and_log(x_logf, f'Can\'t remove "{x_term}": there is no such card.')


def m_import(x_deck, x_logf, import_file=None):
    """Read lines from a file, split lines into comma-separated term and definition
    and add them to the deck as a new flashcard. Existing terms are overwritten.
    If --import_from argument is not supplied, prompt for a filename"""
    if import_file is None:
        print_and_log(x_logf, "File name:")
        filename = input_and_log(x_logf)
    else:
        filename = import_file
    nc = 0
    if not exists(filename):
        print_and_log(x_logf, 'File not found.')
    else:
        try:
            with open(filename, 'r', encoding='utf-8') as fo:
                for line in fo:
                    term, defn, errors = line.strip().split(",")
                    x_deck.add_card(term, defn.strip())
                    x_deck.wcount[term] = int(errors)
                    nc += 1
        except Exception as e:
            print_and_log(x_logf, "File import error:" + str(e))
        print_and_log(x_logf, f'{nc} cards have been loaded.')


def m_export(x_deck, x_logf, export_file=None):
    if export_file is None:
        print_and_log(x_logf, "File name:")
        filename = input_and_log(x_logf)
    else:
        filename = export_file
    nc = 0
    try:
        fo = open(filename, 'w', encoding='utf-8')
        for item, defn in x_deck.items():
            outline = f'{item}, {defn}, {x_deck.wcount[item]}\n'
            fo.write(outline)
            nc += 1
        fo.close()
    except Exception as e:
        print_and_log(x_logf, 'File export error:', str(e))
    print_and_log(x_logf, f'{nc} cards have been saved.')


def m_ask(x_deck, x_logf):
    """Handles the menu choice that runs a number of randomly selected flashcard challenges"""
    print_and_log(x_logf, "How many times to ask?")
    try:
        n_cards = int(input_and_log(x_logf))
    except ValueError:
        n_cards = 0
    for _ in range(n_cards):
        item, defin = choice(list(x_deck.items()))
        print_and_log(x_logf, f'Print the definition of "{item}":')
        answer = input_and_log(x_logf)
        if answer == defin:
            print_and_log(x_logf, "Correct!")
        else:
            x_term = x_deck.get_term(answer)
            x_deck.wcount[item] += 1
            if x_term is None:
                print_and_log(x_logf,
                              f'Wrong. The right answer is "{defin}".')
            else:
                print_and_log(x_logf,
                              f'Wrong. The right answer is "{defin}", but your definition is correct for "{x_term}".')


def m_log(x_logf):
    print_and_log(x_logf, 'File name:')
    out_log_filename = input_and_log(x_logf)
    reopen_logf = x_logf
    x_logf.close()
    try:
        with open(live_log_filename, 'r', encoding='utf-8') as finp, \
             open(out_log_filename, 'w', encoding='utf-8') as foutp:
            for line in finp:
                foutp.write(line)
    except Exception as e:
        print('Error in transfer of logfile:', e)
    try:
        reopen_logf = open(live_log_filename, 'a', encoding='utf-8')
        print_and_log(reopen_logf, 'The log has been saved.')
    except Exception as e:
        print("unable to re-open live log after log transfer", e)
    return reopen_logf


def m_hardest(x_deck, x_logf):
    error_list = sorted(list(x_deck.wcount.items()), key=lambda tup: tup[1], reverse=True)
    top_error_list = []
    if error_list:
        top_error_list = [error_list[0]]
    if len(error_list) > 1:
        for item, count in error_list[1:]:
            if top_error_list[-1][1] != count:
                break
            else:
                top_error_list.append((item, count))
    if top_error_list == [] or top_error_list[0][1] == 0:
        print_and_log(x_logf, 'There are no cards with errors.')
    elif len(top_error_list) > 1:
        print_and_log(x_logf, f'The hardest cards are "{top_error_list[0][0]}"', end='')
        for term, count in top_error_list[1:]:
            print_and_log(x_logf, f', "{term}"', end='')
        print_and_log(x_logf, '')
    else:
        msg = f'The hardest card is "{top_error_list[0][0]}". You have {top_error_list[0][1]} errors answering it'
        print_and_log(x_logf, msg)


def m_reset(x_deck, x_logf):
    """Do the menu option that resets all error counts in the deck to zero"""
    for item, desc in x_deck.items():
        x_deck.wcount[item] = 0
    print_and_log(x_logf, 'Card statistics have been reset.')


"""The main program provides a menu of actions"""
# process command line arguments
parser = argparse.ArgumentParser(prog='flashcards.py',
                                 description='JBA Core Python project - Flash Cards Part 7 of 7.')
parser.add_argument('--import_from', action='store', default=None, required=False)
parser.add_argument('--export_to', action='store', default=None, required=False)
args = parser.parse_args()

logf = open(live_log_filename, 'w', encoding='utf-8')   # open live logfile - overwrite if already exists
deck = Deck()                                           # create an empty flashcard deck
if args.import_from is not None:                              # import cards if --import_from=...
    m_import(deck, logf, args.import_from)
while True:                                             # menu loop
    print_and_log(logf, "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    while True:
        opt = input_and_log(logf).strip().lower()
        if opt in ["add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats"]:
            break
    if opt == 'reset stats':
        m_reset(deck, logf)           # Clear all flashcard errors
    elif opt == 'hardest card':
        m_hardest(deck, logf)   # show flashcard(s) with most errors
    elif opt == 'log':
        logf = m_log(logf)      # transfer live log to a file (returns reopened live log descriptor)
    elif opt == 'exit':
        print_and_log(logf, "Bye bye!")     # Farewell. Thanks for all the Fish ... cards!
        if args.export_to is not None:
            m_export(deck, logf, args.export_to)
        logf.close()
        break
    elif opt == 'ask':          # ask some flashcard questions
        m_ask(deck, logf)
    elif opt == 'export':       # export flashcards to a file
        m_export(deck, logf)
    elif opt == 'import':       # import flashcards from a file
        m_import(deck, logf)
    elif opt == 'remove':       # remove a flashcard
        m_remove(deck, logf)
    elif opt == 'add':          # add a flashcard
        m_add(deck, logf)
    else:
        raise RuntimeWarning    # should never get here??
