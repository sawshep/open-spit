# TODO: Make a textbox object for Menu.display() and for Card.display()

from threading import Thread
from random import shuffle
import pygame
import pickle
import socket

# Libs made by me
import mechanics
import networking
from constants import *

# Starts Pygame
pygame.init()

# Window resolution
window_width = 1280
window_height = 720
# Sets the window resoloution
window = pygame.display.set_mode((window_width, window_height))
# Sets the caption in the title-bar
pygame.display.set_caption('Spit')

# Run this in the main control loop in Menu() or Game()
# TODO: Take the logic statement out of the loop?
def detect_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Main class of the game. Determines whether or not the program is running, and then if the user is in the menu or game.
class Spit:
    # This isn't in __init__() because then the child classes couldn't use it.
    playing = True
    def __init__(self):
        # TODO: Move self.running, self.menu, next to self.playing
        self.running = True
        self.menu = False
        self.main()
    def main(self):
        if self.running:
            if self.menu:
                Menu()
            elif self.playing:
                Game()
        pygame.quit()
        exit()

# TODO: Make the menu after networking is implemented.
class Menu(Spit):
    pass

# Sets up Users and window, manages game mechanics too.
class Game(Spit):
    def __init__(self):
        self.make_deck()
        self.make_users()
        self.main()
    def make_deck(self):
        self.deck = []
        for suit in SUITS:
            for value_pair in VALUE_PAIRS:
                self.deck.append(Card(value_pair, suit))
        shuffle(self.deck)
    def make_users(self):
        self.users = {0:None, 1:None}
        for user in self.users:
            self.users[user] = User(self.deck[:31])
            del self.deck[:31]
    def main(self):
        self.multiplayer_thread = Thread(target=self.multiplayer)
        self.mechanics_thread = Thread(target=self.mechanics)
        self.display_thread = Thread(target=self.display)

        self.multiplayer_thread.start()
        self.mechanics_thread.start()
        self.display_thread.start()

        self.multiplayer_thread.join()
        self.mechanics_thread.join()
        self.display_thread.join()
    def multiplayer(self):
        self.network = input('Join or host game?')
        if self.network == 'host':
            networking.Host()
        else:
            networking.Client(self.network)
    def mechanics(self):
        pass
        # mechanics.get_keys()
    def display(self):
        window.fill(GRAY)
        # TODO?: Move detect_quit() out of the function for loop and into this loop?
        for dummy_event in pygame.event.get():
            pass
        detect_quit()
        # Displays the game objects of each user.
        for user in self.users:
            self.users[user].display(user)
        # Updates the display 60 times every second.
        pygame.display.update()
        pygame.time.Clock().tick(60)

# Makes the objects that can hold Cards and displays them.
class User:
    pile_spacing = window_width / 6
    hand_spacing = window_width / 3
    def __init__(self, cards):
        self.deck = cards
        self.make_piles()
        self.make_center_pile()
        self.hands = {0:Hand(), 1:Hand()}
    def make_piles(self):
        self.piles = {0:Pile(), 1:Pile(), 2:Pile(), 3:Pile(), 4:Pile()}
        # Makes each pile have one more card than the last.
        for pile in self.piles:
            # The variable in this loop is '_' because it is purposely never used.
            for _ in range(pile + 1):
                self.piles[pile].cards.append(self.deck[0])
                del self.deck[0]
            # Flips the card on top of each pile.
            self.piles[pile].cards[-1].flipped = True
    def make_center_pile(self):
        self.center_pile = Pile()
        self.center_pile.cards.append(self.deck[0])
        self.center_pile.cards[-1].flipped = True
        del self.deck[0]
    def make_hands(self):
        self.hands = {0:Hand(), 1:Hand()}
    def display(self, factor):
        # This formula is very important in maintaining symetry
        # |(Window Height * Factor) - (Window Height * Fraction, not > 1/2)|
        for pile in self.piles:
            self.x_cord = int(self.pile_spacing * (pile + 1))
            self.y_cord = int(abs((window_height * factor) - (window_height * 2/7)))
            self.piles[pile].display(self.x_cord, self.y_cord)
        for hand in self.hands:
            self.x_cord = int(self.hand_spacing * (hand + 1))
            self.y_cord = int(abs((window_height * factor) - (window_height)))
            self.hands[hand].display(self.x_cord, self.y_cord)
        self.x_cord = int(window_width / 2)
        self.y_cord = int(abs((window_height * factor) - (window_height * 3/7)))
        self.center_pile.display(self.x_cord, self.y_cord)

# Mainly just a 'placeholder' so there are not so many nested lists in User.
class Pile:
    def __init__(self):
        # It is easier to set the cards in each pile on a lower level of abstraction than to take them in a parameter.
        self.cards = []
    def display(self, x_cord, y_cord):
        if self.cards:
            self.cards[-1].display(x_cord, y_cord)

class Hand:
    width = int(window_width / 10)
    height = width
    def __init__(self):
        self.card = None
        # y_mod is used to move the hand up/down when one of the arrow keys is pressed.
        self.y_mod = 0
    def display(self, x_cord, y_cord):
        # Centers hand on coords
        self.x_cord = int(x_cord - self.width / 2)
        self.y_cord = int(y_cord - self.height / 2 + self.y_mod)
        pygame.draw.rect(window, BLACK, [self.x_cord, self.y_cord, self.width, self.height])
        if self.card:
            self.card.display(self.x_cord, self.y_cord)

class Card:
    width = int(window_height / 12)
    height = int(width * 3.5/2.5)
    def __init__(self, value_pair, suit):
        self.value = value_pair[0]
        self.face = value_pair[1]
        self.suit = suit
        self.flipped = False
        # Fix for wrong suit color bug.
        # \u266* are unicode characters for the suits.
        if self.suit == '\u2660' or self.suit == '\u2663':
            self.color = BLACK
        else:
            self.color = RED
    def display(self, x_cord, y_cord):
        # Centers card on coords
        self.x_cord = int(x_cord - self.width / 2)
        self.y_cord = int(y_cord - self.height / 2)
        if self.flipped:
            text = self.face + self.suit
            # TODO: Put text stuff in a Textbox class
            font = pygame.font.Font('./ibm.ttf', int(window_height / 21))
            textbox = font.render(text, True, self.color, WHITE)
            pygame.draw.rect(window, WHITE, [self.x_cord, self.y_cord, self.width, self.height])
            window.blit(textbox, (self.x_cord, self.y_cord))
        else:
            pygame.draw.rect(window, BLUE, [self.x_cord, self.y_cord, self.width, self.height])

Spit()
