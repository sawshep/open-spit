from threading import Thread
from random import shuffle
import sys
import pickle
import socket
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import constants

pygame.init()

users = {0:None, 1:None}

PILES = [
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f,
    pygame.K_SPACE
]
HANDS = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_KP0
]
CENTER_PILES = [
    pygame.K_UP,
    pygame.K_DOWN,
]

PRESSED_CONTROLS = PILES + CENTER_PILES

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
PORT = 31415

class Networker:
    '''Sets up the base for a Client or Server to be created'''
    # The sockets for both Server and Client use UDP.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    username = input('Enter username:\n>')

    def recv(self, return_addr=False):
        '''Waits for data from the connected address.
        It will hang until it receives a packet.'''
        recv_data, addr = self.s.recvfrom(2048)
        recv_msg = pickle.loads(recv_data)
        if return_addr:
            return (recv_msg, addr)
        return recv_msg
    def recv_thread(self):
        '''Intended to be used in a thread.
        This works around the hanging of recv() by multithreading it.'''
        while True:
            users[1] = self.recv()[0]

class Server(Networker):
    '''Hosts a socket server on the local machine using UDP'''
    def __init__(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('127.0.0.1', PORT))

        print('Waiting for opponent...')
        self.opponent, self.addr = self.recv(return_addr=True)
        print(f'{self.opponent} joined the game')
        self.send(self.username)

    def send(self, send_msg):
        '''Encodes and sends data to the connected client'''
        self.s.sendto(pickle.dumps(send_msg), self.addr)

class Client(Networker):
    '''Connects to Server of the user's choice with UDP'''
    def __init__(self):
        self.addr = input('Enter server IP:\n>')
        print('Connecting...')
        self.send(self.username)
        self.s.settimeout(3.0)
        self.opponent = self.recv()
        self.s.settimeout(None)
        print(f'Joined {self.opponent}\'s game')
    def send(self, send_msg):
        '''Encoded and sends data to the connected server.'''
        self.s.sendto(pickle.dumps(send_msg), (self.addr, PORT))

class Spit:
    '''Controls whether to display Menu or Game'''
    playing = True
    def __init__(self):
        self.running = True
        self.menu = False
        if self.running:
            if self.menu:
                self.menu = Menu()
            elif self.playing:
                self.game = Game()
        pygame.quit()
        exit()

class Menu(Spit):
    '''Controls functionality and high level display of the menu'''

class Game:
    '''Controls mechanics and high level display of the game'''
    def __init__(self):
        self.network_setup()
        global WINDOW
        WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Spit')
        self.recv_thread = Thread(target=self.network.recv)
        self.recv_thread.start()
        self.mechanics()
    def network_setup(self):
        '''Controls the differences in setup between the server and the client'''
        while True:
            global users
            self.network = input('Do you want to (join) or (host) a game?\n>')
            if self.network == 'host':
                self.network = Server()
                self.deck = self.make_deck()
                users = self.make_users()
                self.network.send(users)
                break
            elif self.network == 'join':
                try:
                    self.network = Client()
                    self.host_users = self.network.recv()
                    users = {0:self.host_users[1], 1:self.host_users[0]}
                    break
                except socket.timeout:
                    print('Failed to connect to the server')
            else:
                print('Incorrect usage')
    def mechanics(self):
        '''The main user control loop.
        Sends deck changes to the opponent.
        Calls the display of both User's elements.'''
        user = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                pressed_keys = []
                if event.type == pygame.KEYDOWN:
                    for pile in range(5):
                        if PRESSED_CONTROLS[pile] == event.key:
                            pressed_keys.append(pile)
                held_keys = []
                for hand in range(3):
                    if pygame.key.get_pressed()[HANDS[hand]]:
                        held_keys.append(hand)

                for hand in users[user].hands:
                    users[user].hands[hand].selected = False

                # I'm so sorry for the spaghetti beyond this point
                # Control loop
                if len(held_keys) == 1:
                    hand = held_keys[0]
                    if hand == 2:
                        for hand in range(2):
                            users[user].hands[hand].selected = True
                        if users[user].hands[0].card is None or users[user].hands[1].card is None:
                            if len(pressed_keys) == 1:
                                pile = pressed_keys[0]
                                users[user].piles[pile].cards[-1].flipped = True
                    else:
                        users[user].hands[hand].selected = True
                        if len(pressed_keys) == 1:
                            pile = pressed_keys[0]
                            if users[user].piles[pile].cards:
                                if users[user].hands[hand].card is None:
                                    if users[user].piles[pile].cards[-1].flipped:
                                        users[user].hands[hand].card = users[user].piles[pile].cards[-1]
                                        del users[user].piles[pile].cards[-1]
                                else:
                                    if users[user].piles[pile].cards[-1].value == users[user].hands[hand].card.value:
                                        users[user].piles[pile].cards.append(users[user].hands[hand].card)
                                        users[user].hands[hand].card = None
                            elif users[user].hands[hand].card:
                                users[user].piles[pile].cards.append(users[user].hands[hand].card)
                                users[user].hands[hand].card = None
                else:
                    for hand in users[user].hands:
                        users[user].hands[hand].selected = False
            self.network.send(users[user])
            self.display()

    def make_deck(self):
        '''Server side. Creates the deck of cards to be distributed among the users.'''
        deck = []
        for suit in constants.SUITS:
            for value_pair in constants.VALUE_PAIRS:
                deck.append(Card(value_pair, suit))
        shuffle(deck)
        return deck
    def make_users(self):
        '''Server side. Initially creates both the Server and Client users.'''
        for user in users:
            users[user] = User(self.deck[:31])
            del self.deck[:31]
        return users
    def display(self):
        '''Creates background.
        Calls display of all background elements.
        Updates the display.
        Runs at 60 frames per second.'''
        WINDOW.fill(constants.GRAY)
        for user in users:
            users[user].display(user)
        pygame.display.update()
        pygame.time.Clock().tick(60)

class User:
    '''Holds all the objects that can hold cards'''
    pile_spacing = WINDOW_WIDTH / 6
    hand_spacing = WINDOW_WIDTH / 3
    def __init__(self, cards):
        self.deck = cards
        self.piles = self.make_piles()
        self.center_pile = self.make_center_pile()
        self.hands = {0:Hand(), 1:Hand()}
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
    def make_center_pile(self):
        '''The center pile is the pile that the users can play their cards on.
        It can start with zero or one cards.
        It can have any positive number of cards.'''
        center_pile = Pile()
        center_pile.cards.append(self.deck[0])
        center_pile.cards[-1].flipped = True
        del self.deck[0]
        return center_pile
    def make_hands(self):
        '''Creates two hands.
        Each hand start empty.
        They can have only one or zero cards'''
        self.hands = {0:Hand(), 1:Hand()}
    def display(self, factor):
        '''Calls for the display of all card-holding objects stored in User'''
        # This formula is very important in maintaining symetry:
        # (Window Height * Factor) - (Window Height * Fraction, not > 1/2)|
        for pile in self.piles:
            x_coord = int(self.pile_spacing * (pile + 1))
            y_coord = int(abs((WINDOW_HEIGHT * factor) - (WINDOW_HEIGHT * 5/7)))
            self.piles[pile].display(x_coord, y_coord)
        for hand in self.hands:
            x_coord = int(self.hand_spacing * (hand + 1))
            y_coord = int(abs((WINDOW_HEIGHT * factor) - (WINDOW_HEIGHT)))
            self.hands[hand].display(x_coord, y_coord, factor)
        x_coord = int(WINDOW_WIDTH / 2)
        y_coord = int(abs((WINDOW_HEIGHT * factor) - (WINDOW_HEIGHT * 4/7)))
        self.center_pile.display(x_coord, y_coord)

class Pile:
    '''A place holder for a list of cards.
    Mainly exists so the main pile and center pile
    in User can exist via the same class.
    Prevents lots of nested lists and dicts in User.'''
    def __init__(self):
        self.cards = []
    def display(self, x_coord, y_coord):
        '''Calls for the display of all cards in the pile
        (if there are any)'''
        if self.cards:
            self.cards[-1].display(x_coord, y_coord)

class Hand:
    '''Each hand can hold a max of one and a min of zero cards.
    They can either be selected or not.
    If they are selected, they display offset from their
    default position'''
    width = int(WINDOW_WIDTH / 10)
    height = width
    y_coord_mod = int(height / 2)
    def __init__(self):
        self.card = None
        self.selected = False
    def display(self, x_coord, y_coord, factor):
        '''Draws a black square at selected coordinates.
        Position changes depending on if the hand is selected.
        Calls for the card in the hand to be displayed if there is one.'''
        x_coord = int(x_coord - self.width / 2)
        y_coord = int((y_coord - self.height / 4) + (self.height * factor - self.y_coord_mod) * self.selected)
        pygame.draw.rect(WINDOW, constants.BLACK, [x_coord, y_coord, self.width, self.height])
        if self.card:
            self.card.display(x_coord, y_coord)

class Card:
    '''Each card has a value, a suit, and a color.
    Can be displayed.'''
    width = int(WINDOW_HEIGHT / 12)
    height = int(width * 3.5/2.5)
    def __init__(self, value_pair, suit):
        self.value = value_pair[0]
        self.face = value_pair[1]
        self.suit = suit
        self.flipped = False
        if self.suit == '\u2660' or self.suit == '\u2663':
            self.color = constants.BLACK
        else:
            self.color = constants.RED
    def display(self, x_coord, y_coord):
        '''Displays the card on selected coordinates'''
        x_coord = int(x_coord - self.width / 2)
        y_coord = int(y_coord - self.height / 2)
        if self.flipped:
            text = self.face + self.suit
            font = pygame.font.Font('./ibm.ttf', int(WINDOW_HEIGHT / 21))
            textbox = font.render(text, True, self.color, constants.WHITE)
            pygame.draw.rect(WINDOW, constants.WHITE, [x_coord, y_coord, self.width, self.height])
            WINDOW.blit(textbox, (x_coord, y_coord))
        else:
            pygame.draw.rect(WINDOW, constants.BLUE, [x_coord, y_coord, self.width, self.height])

SPIT = Spit()
