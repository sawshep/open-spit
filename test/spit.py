'''The main module that actually runs the game'''

import sys
import pygame

#My modules
import constants
import config
import client
import gamedata

pygame.init()

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

class Spit:
    '''Controls whether to display Menu or Game'''
    playing = True
    def __init__(self):
        self.running = True
        if self.running:
            Game()
        pygame.quit()
        exit()

class Screen:
    '''Creates and updates the display'''
    width = config.WINDOW_WIDTH
    height = config.WINDOW_HEIGHT
    def __init__(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Spit')
    def display(self, users):
        '''Displays things'''
        self.window.fill(constants.GRAY)
        for user in users:
            cards = users[user].center_pile.cards
            if cards:
                x_coord = int(self.width / 2 - gamedata.Card.width / 2)
                y_coord = int((abs((self.height * user) - (self.height * 4/7))) - gamedata.Card.height / 2)
                card = cards[-1]
                font = pygame.font.Font('./ibm.ttf', card.font_size)
                text = card.face + card.suit
                textbox = font.render(text, True, card.color, constants.WHITE)
                pygame.draw.rect(self.window, constants.WHITE, [x_coord, y_coord, card.width, card.height])
                self.window.blit(textbox, (x_coord, y_coord))
            
            piles = users[user].piles
            pile_spacing = self.width / (len(piles) + 1)
            for pile in piles:
                cards = piles[pile].cards
                if cards:
                    x_coord = int((pile_spacing * (pile + 1)) - gamedata.Card.width / 2)
                    y_coord = int((abs((self.height * user) - (self.height * 5/7))) - gamedata.Card.height / 2)
                    card = cards[-1]
                    if card.flipped:
                        font = pygame.font.Font('./ibm.ttf', card.font_size)
                        text = card.face + card.suit
                        textbox = font.render(text, True, card.color, constants.WHITE)
                        pygame.draw.rect(self.window, constants.WHITE, [x_coord, y_coord, card.width, card.height])
                        self.window.blit(textbox, (x_coord, y_coord))
                    else:
                        pygame.draw.rect(
                            self.window, constants.BLUE,
                            [x_coord, y_coord, card.width, card.height]
                        )
            hands = users[user].hands
            hand_spacing = self.width / (len(hands) + 1)
            for hand in hands:
                x_coord = int(hand_spacing * (hand + 1))
                y_coord = int(((abs(self.height * user - self.height)) - gamedata.Hand.height / 4) + (gamedata.Hand.height * user - gamedata.Hand.y_mod) * hands[hand].selected)
                pygame.draw.rect(
                    self.window, constants.BLACK,
                    [x_coord, y_coord, gamedata.Hand.width, gamedata.Hand.height]
                )
                card = hands[hand].card
                if card:
                    text = card.face + card.suit
                    font = pygame.font.Font('./ibm.ttf', card.font_size)
                    textbox = font.render(text, True, card.color, constants.WHITE)
                    pygame.draw.rect(
                        self.window, constants.WHITE,
                        [x_coord, y_coord, card.width, card.height]
                    )
                    self.window.blit(textbox, (x_coord, y_coord))
        pygame.display.update()

class Game:
    '''Controls mechanics and high level display of the game'''
    def __init__(self):
        self.screen = Screen()
        self.networker = client.Client()
        self.deck = self.networker.deck
        self.users = gamedata.make_users(self.deck)
        self.main()
    def main(self):
        '''The main user control loop.
        Sends deck changes to the opponent.
        Calls the display of both User's elements.'''
        timer = pygame.time.Clock()
        while True: 
            for event in pygame.event.get():
                # Detects quitting
                if event.type == pygame.QUIT:
                    self.networker.close()
                    pygame.quit()
                    sys.exit()

                # Detects pile keypresses
                if event.type == pygame.KEYDOWN:
                    for pile in range(5):
                        if PRESSED_CONTROLS[pile] == event.key:
                            self.users[0].keys.pressed.append(pile)

            # Detects hand keyholds
            for hand in range(3):
                if pygame.key.get_pressed()[HANDS[hand]]:
                    self.users[0].keys.held.append(hand)

            self.users[1].keys = self.networker.network_io(self.users[0].keys)
            for hand in self.users[0].hands:
                self.users[0].hands[hand].selected = False
            #Runs game logic/mechanics for each user
            for user in self.users:
                keys = self.users[user].keys
                if len(keys.held) == 1:
                    hand = keys.held[0]
                    if hand == 2:
                        for hand in range(2):
                            self.users[user].hands[hand].selected = True
                        hands = self.users[user].hands
                        if hands[0].card is None or hands[1].card is None:
                            if len(keys.pressed) == 1:
                                pile = keys.pressed[0]
                                self.users[user].piles[pile].cards[-1].flipped = True
                    else:
                        self.users[user].hands[hand].selected = True
                        if len(keys.pressed) == 1:
                            pile = keys.pressed[0]
                            if self.users[user].piles[pile].cards:
                                if self.users[user].hands[hand].card is None:
                                    if self.users[user].piles[pile].cards[-1].flipped:
                                        self.users[user].hands[hand].card = self.users[user].piles[pile].cards[-1]
                                        del self.users[user].piles[pile].cards[-1]
                                else:
                                    if self.users[user].piles[pile].cards[-1].value == self.users[user].hands[hand].card.value:
                                        self.users[user].piles[pile].cards.append(self.users[user].hands[hand].card)
                                        self.users[user].hands[hand].card = None
                            elif self.users[user].hands[hand].card:
                                self.users[user].piles[pile].cards.append(self.users[user].hands[hand].card)
                                self.users[user].hands[hand].card = None
                else:
                    for hand in self.users[user].hands:
                        self.users[user].hands[hand].selected = False
                self.users[user].keys.clear()
            self.screen.display(self.users)
            timer.tick(60)

Spit()
