from random import shuffle
import pygame

#Starts Pygame
pygame.init()

#Window resolution
window_width = 1280
window_height = 1000

#Sets the window resoloution
global window
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

#Card size is adaptive to window size
card_width = int(window_height / 12)
card_height = int(card_width * 3.5/2.5)

#Hand size is adaptive to window size
hand_width = int(window_width / 12)
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
        #The value is the numerical value used for calculations
        self.value = value_pair[0]
        #The face value is the number or letter shown to user
        self.face = value_pair[1]
        self.suit = suit
        #Sets the color of the card
        if self.suit == '\u2660' or self.suit == '\u2663':
            self.color = black
        else:
            self.color = red
        self.flipped = False
    def display_card(self, x_cord, y_cord):
        text = self.face + self.suit
        #TODO: Make font size adaptive to window size 
        font = pygame.font.Font('./ibm.ttf', 50)
        #Makes the textbox an object
        text_box = font.render(text, True, self.color, white)
        #Renders the object on the screen
        window.blit(text_box, (x_cord,y_cord))

#Generates every combination of suit and value


#Creates list of users. 0 is player, 1 is opponent. The values are words in RAM.
users = {0:None, 1:None}
class User:
    def __init__(self, user):
        users[user] = self
        #Generates the 5 piles for user
        self.piles = []
        self.make_piles()
        #User's hands start as empty
        self.hands = {0:None, 1:None}
        #Draws card for the starting center pile
        self.center_pile = [deck[0]]
        del deck[0]
        #These are used to tell if user is moving their hands
        self.hand_mods = {0:0, 1:0}
        
    def make_piles(self):
        #For each of the five piles
        for pile_number in range(5):
            #Originally there are no cards in the pile
            pile = []
            #Then it adds the respective amount of cards based on what pile is iterating
            for card in range(pile_number + 1):
                pile.append(deck[0])
                del deck[0]
            #Sets the card on top of the pile face up
            pile[-1].flipped = True
            #Makes self.piles a list of piles, which are lists of cards
            self.piles.append(pile)

    def display_piles(self):
        #Vertical pile spacing is adaptive to screen size
        if users[0] == self:
            y_frac = 6/8
        else:
            y_frac = 2/8
        piles = self.piles
        #Horizontal pile spacing is adaptive to screen size
        pile_spacing = window_width / 6
        #All user's piles have the same y value
        y_cord = int(window_height * y_frac - card_height / 2)
        #Spaces and centers the piles evenly
        for pile in range(5):
            x_cord = int(pile_spacing * pile + pile_spacing - card_width / 2)
            #Only displays the pile if there is a card in it
            if piles[pile]:
                #Only shows the card if it is flipped up
                if piles[pile][-1].flipped:
                    pygame.draw.rect(window, white, [x_cord, y_cord, card_width, card_height])
                    piles[pile][-1].display_card(x_cord, y_cord)
                else:
                    pygame.draw.rect(window, light_blue, [x_cord, y_cord, card_width, card_height])
    def display_hands(self):
        hands = self.hands
        #Horizontal hand spacing is adaptive to window size
        hand_spacing = window_width / 3
        #Changes the vertial postion of the hand to show that is is selected
        hand_mods = self.hand_mods
        for hand in hands:
            #Evenly spaces and centers hands horizontally
            x_cord = int(hand_spacing * hand + hand_spacing - hand_width / 2)
            #Displays the hands on the respective side of the screen for each user
            if users[0] == self:
                y_cord = int( -1 * hand_height / 2 - hand_mods[hand])
            else:
                y_cord = int(window_height - hand_height / 2 - hand_mods[hand])
            #Draws the hand
            pygame.draw.rect(window, black, [x_cord, y_cord, hand_width, hand_height])
            #Displays a card in the hand if there is one
            if hands[hand]:
                hands[hand].display_card(x_cord, y_cord)
    def display_center_pile(self):
        #Displays the center pile on the correct side of the screen, respectively
        if users[0] == self:
            y_frac = 3/5
        else:
            y_frac = 2/5
        #Horizontal center pile position is adaptive to the screen size
        x_cord = int(window_width / 2 - card_width / 2)
        #Vertical center pile position is adaptive to the screen size
        y_cord = int(window_height * y_frac - card_height / 2)
        #Only displays the center pile if there is a card in it
        if self.center_pile:
            pygame.draw.rect(window, white, [x_cord, y_cord, card_width, card_height])
            self.center_pile[-1].display_card(x_cord, y_cord)

playing = True
while playing:
    deck = []
    for suit in suits:
        for value_pair in value_pairs:
            deck.append(Card(value_pair, suit))
    shuffle(deck)
    player = User(0)
    opponent = User(1)
    while 1:
        #Listens for every event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Stops Pygame
                pygame.quit()
                #Stops Python
                exit()

        #These are self explanatory
        window.fill(grey)

        player.display_piles()
        opponent.display_piles()

        player.display_hands()
        opponent.display_hands()

        player.display_center_pile()
        opponent.display_center_pile()

        #Makes the changes made above actually show on screen
        pygame.display.update()
        #Framerate locked to 60
        pygame.time.Clock().tick(60)