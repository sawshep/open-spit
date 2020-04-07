from random import shuffle
import pygame

#Initiallizes Pygame
pygame.init()

#Window resolution
window_width = 1280
window_height = 1000

#Sets the window resoloution
window = pygame.display.set_mode((window_width, window_height))
#Sets the caption in the title-bar
pygame.display.set_caption('Spit')

#Colors: Tuples with RGB values from 0 to 255
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
light_blue = (50, 150, 225)
grey = (115, 115, 115)

card_width = window_height * 1/12
card_height = int(card_width * 3.5/2.5)

hand_width = window_width / 12
hand_height = hand_width

#Unicode characters for suits
suits = [
    '\u2660',
    '\u2663',
    '\u2665',
    '\u2666'
]

#A calculation value and a face value for the cards
value_pairs = [
    (1,'A'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
    (8,'8'),
    (9,'9'),
    (10,'10'),
    (11,'J'),
    (12,'Q'),
    (13,'K')
]

class Card:
    def __init__(self, value_pair, suit):
        self.value = value_pair[0]
        self.face = value_pair[1]
        self.suit = suit
        self.flipped = False
    def display_card(self, x_cord, y_cord):
        text = self.face + self.suit
        font = pygame.font.Font('./ibm.ttf', 45)
        if text[1] == '\u2660' or text[1] == '\u2663':
            foreground_color = black
        else:
            foreground_color = red
        text_object = font.render(text, True, foreground_color, white)
        window.blit(text_object, (x_cord,y_cord))

deck = []
for suit in suits:
	for value_pair in value_pairs:
		deck.append(Card(value_pair, suit))
shuffle(deck)

users = {0:None, 1:None}

class User:
    def __init__(self, user):
        users[user] = self
        self.piles = []
        self.make_piles()
        self.hands = {0:None, 1:None}
        self.center_pile = [deck[0]]
        self.hand_mods = {0:0, 1:0}
        del deck[0]
        
    def make_piles(self):
        for pile_number in range(5):
            pile = []
            for card in range(pile_number + 1):
                pile.append(deck[0])
                del deck[0]
            pile[-1].flipped = True
            self.piles.append(pile)

    def display_piles(self):
        if users[0] == self:
            y_frac = 6/8
        else:
            y_frac = 2/8
        piles = self.piles
        pile_spacing = window_width / 6
        y_cord = int(window_height * y_frac - card_height / 2)
        for pile in range(5):
            x_cord = int(pile_spacing * pile + pile_spacing - card_width / 2)
            if piles[pile]:  
                if piles[pile][-1].flipped:
                    pygame.draw.rect(window, white, [x_cord, y_cord, card_width, card_height])
                    piles[pile][-1].display_card(x_cord, y_cord)
                else:
                    pygame.draw.rect(window, light_blue, [x_cord, y_cord, card_width, card_height])
    def display_hands(self):
        hands = self.hands
        hand_spacing = window_width / 3
        hand_mods = self.hand_mods
        for hand in hands:
            if users[0] == self:
                y_cord = int( -1 * (hand_height / 2) - hand_mods[hand])
                
            else:
                y_cord = int(window_height - hand_height / 2 - hand_mods[hand])
            x_cord = int(hand_spacing * hand + hand_spacing - hand_width / 2)
            pygame.draw.rect(window, black, [x_cord, y_cord, hand_width, hand_height])
            if hands[hand]:
                text = hands[hand].face + hands[hand].suit
                #display_card(text, x_cord, y_cord)
    def display_center_pile(self):
        if users[0] == self:
            y_frac = 3/5
        else:
            y_frac = 2/5
        x_cord = int(window_width / 2 - card_width / 2)
        y_cord = int(window_height * y_frac - card_height / 2)
        pygame.draw.rect(window, white, [x_cord, y_cord, card_width, card_height])
        self.center_pile[-1].display_card(x_cord, y_cord)


player = User(0)
opponent = User(1)


def game_loop():
    global window
    #listens for every event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    window.fill(grey)

    player.display_piles()
    opponent.display_piles()

    player.display_hands()
    opponent.display_hands()

    player.display_center_pile()
    opponent.display_center_pile()

    #updates screen
    pygame.display.update()
    #frame rate locked to 60
    pygame.time.Clock().tick(60)

while 1:
    game_loop()