'''gamedata.py
Holds game data that does not rely on Pygame'''

# From the Python standard library
import random

# My modules
import config
import constants

def make_deck():
    '''Server side. Creates the deck of cards to be distributed among the users.'''
    deck = []
    for suit in constants.SUITS:
        for value_pair in constants.VALUE_PAIRS:
            deck.append(Card(value_pair, suit))
    random.shuffle(deck)
    return deck

def make_users(deck):
    '''Creates user objects from a server-provided deck'''
    temp_deck = deck
    users = {0: User(deck[:len(deck) // 2]), 1: User(deck[len(deck) // 2:])}
    for user in users:
        users[user] = User(deck[:26])
        del temp_deck[:26]
    return users

class User:
    '''Holds all the objects that can hold cards'''
    def __init__(self, cards):
        self.deck = cards
        self.piles = self.make_piles()
        self.center_pile = Pile()
        self.hands = {0:Hand(), 1:Hand()}
        self.keys = Keys()
        self.ready = False
    def make_piles(self):
        '''Distributes the cards assigned to the users among the piles.
        There are five piles.
        Each pile has one more card than the last (starting at one).
        The top card of each pile is flipped face up.'''
        piles = {0:Pile(), 1:Pile(), 2:Pile(), 3:Pile(), 4:Pile()}
        # Makes each pile have one more card than the last.
        for pile in piles:
            # The variable in this loop is '_' because it is purposely never used.
            for _ in range(pile + 1):
                piles[pile].cards.append(self.deck[0])
                del self.deck[0]
            # Flips the card on top of each pile.
            piles[pile].cards[-1].flipped = True
        return piles

class Pile:
    '''A place holder for a list of cards.
    Mainly exists so the main pile and center pile
    in User can exist via the same class.
    Prevents lots of nested lists and dicts in User.'''
    def __init__(self):
        self.cards = []

class Hand:
    '''Each hand can hold a max of one and a min of zero cards.
    They can either be selected or not.
    If they are selected, they display offset from their
    default position'''
    width = int(config.WINDOW_WIDTH / 10)
    height = width
    y_mod = int(height / 2)
    def __init__(self):
        self.card = None
        self.selected = False
# ABSTRACTION
#####################################################
class Card:
    '''Each card has a value, a suit, and a color.'''
    width = int(config.WINDOW_HEIGHT / 12)
    height = int(width * 3.5/2.5)
    font_size = int(config.WINDOW_HEIGHT / 21)
    def __init__(self, value_pair, suit):
        # Value is the actual numeric value for each card, so a Jack would be 11
        self.value = value_pair[0]
        # This is the character that is displayed on the actual card (A-K)
        self.face = value_pair[1]
        self.suit = suit
        self.flipped = False
        # The \u things are unicode characters for spades and clubs
        if self.suit == '\u2660' or self.suit == '\u2663':
            self.color = constants.BLACK
        else:
            self.color = constants.RED
#####################################################

class Keys:
    '''Hold the pressed keys for each User'''
    def __init__(self):
        self.held = []
        self.pressed = []
    def clear(self):
        '''Resets each list of keys to be empty'''
        self.held = []
        self.pressed = []
