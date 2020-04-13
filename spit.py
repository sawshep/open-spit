from random import shuffle
from constants import *
from threading import Thread
import pygame

#Starts Pygame
pygame.init()

#Window resolution
window_width = 1280
window_height = 1000

#Sets the window resoloution
window = pygame.display.set_mode((window_width, window_height))
#Sets the caption in the title-bar
pygame.display.set_caption('Spit')

def detect_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

class Spit:
    playing = True
    def __init__(self):
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

class Menu(Spit):
    pass

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
        while self.playing:
            window.fill(GRAY)
            detect_quit()
            self.display()
            pygame.display.update()
            pygame.time.Clock().tick(60)
    def display(self):
        for user in self.users:
            self.users[user].display(user)

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
        for pile in self.piles:
            for _ in range(pile + 1):
                self.piles[pile].cards.append(self.deck[0])
                del self.deck[0]
            self.piles[pile].flip()
    def make_center_pile(self):
        self.center_pile = Pile()
        self.center_pile.cards.append(self.deck[0])
        self.center_pile.cards[-1].flipped = True
        del self.deck[0]
    def make_hands(self):
        self.hands = {0:Hand(), 1:Hand()}
    def display(self, factor):
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

class Pile:
    def __init__(self):
        self.cards = []
    def flip(self):
        self.cards[-1].flipped = True
    def display(self, x_cord, y_cord):
        if self.cards:
            self.cards[-1].display(x_cord, y_cord)

class Hand:
    width = int(window_width / 10)
    height = width
    def __init__(self):
        self.card = None
        self.y_mod = 0
    def display(self, x_cord, y_cord):

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
        if self.suit == '\u2660' or self.suit == '\u2663':
            self.color = BLACK
        else:
            self.color = RED
    def display(self, x_cord, y_cord):
        self.x_cord = int(x_cord - self.width / 2)
        self.y_cord = int(y_cord - self.height / 2)
        if self.flipped:
            text = self.face + self.suit
            font = pygame.font.Font('./ibm.ttf', 40)
            text_box = font.render(text, True, self.color, WHITE)
            pygame.draw.rect(window, WHITE, [self.x_cord, self.y_cord, self.width, self.height])
            window.blit(text_box, (self.x_cord, self.y_cord))
        else:
            pygame.draw.rect(window, BLUE, [self.x_cord, self.y_cord, self.width, self.height])

Spit().__init__
