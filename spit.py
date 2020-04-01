import pygame
from random import shuffle

pygame.init()

#window dimensions, used for calculations too
width = 1280
height = 720

#sets up window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open-Spit')

#Colors, each have a red green and blue value up to 255
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
    
#the \u266* numbers are unicode characters for the suits
suits = [
    '\u2660',
    '\u2663',
    '\u2665',
    '\u2666'
]

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

piles = {
    0:[],
    1:[],
    2:[],
    3:[],
    4:[],
}

hands = {
    'r':None,
    'l':None,
}



#Framework to make cards, each has a numerical value, a face value, a suit, and is flipped up/down
class MakeCard:
    def __init__(self, value_pair, suit):
    #Makes variables that only apply to the class equal the parameters
        #Numerical value for calculations
        self.value = value_pair[0]
        #Face value for player to see
        self.face = value_pair[1]
        self.suit = suit
        #Whether the face of the card is visible
        self.flipped = False
        
    def get_value(self):
        return self.value
    
    def get_face(self):
        return self.face
    
    def get_suit(self):
        return self.suit

    def get_flipped(self):
        return self.flipped
    
    #Takes paramater input later on
    def set_flipped(self, flipped):
        self.flipped = flipped
        
deck = []
#Makes the deck a list of objects
for suit in suits:
    for value in value_pairs:
        deck.append(MakeCard(value, suit))
        
shuffle(deck)

#Makes the piles. Inside the main dictionary, there are lists, while inside those there are card objects
for pile in piles:
    #Makes it so that every pile has one more card than the last.
    for card in range(pile + 1):
        piles[pile].append(deck[0])
        del deck[0]
    #Sets the card on the top of the pile face up
    piles[pile][-1].set_flipped(True)
    

def display_card(text, x_cord, y_cord):
    if text[1] == '\u2660' or text[1] == '\u2663':
        color = black
    else:
        color = red
    font = pygame.font.Font('./ibm.ttf', 18)
    text_object = font.render(text, True, color, white)
    window.blit(text_object, (x_cord, y_cord))
    
def display_hand(x_mod, y_mod, hand):
    x_cord = int(width * x_mod)
    y_cord = (height - y_mod - 25)
    pygame.draw.rect(window, black, [x_cord, y_cord, 100, 100])
    if hands[hand]:
        if hands[hand].get_flipped:
            text = hands[hand].get_face() + hands[hand].get_suit()
            display_card(text, x_cord, y_cord)
    
def display_piles(y_cord):   
    for pile in piles:
        pile_spacing = width / (len(piles) + 1)
        x_cord = int((pile_spacing * pile) + pile_spacing)
        if piles[pile]:
            pygame.draw.rect(window, black, [x_cord, y_cord, 100, 100])
            if piles[pile][-1].get_flipped():
                text = piles[pile][-1].get_face() + piles[pile][-1].get_suit()
                display_card(text, x_cord, y_cord)

#Adds the top card of the selected deck to the selected hand
def pick_up(pile, hand):
    hands[hand] = piles[pile][-1]
    del piles[pile][-1]

#Removes the card from the selected hand ands puts it on top of the selected pile
def put_down(pile, hand):
    piles[pile].append(hands[hand])
    hands[hand] = None

    
quit = False

def game_loop():
    #makes the hand_mod vars global so they can be used in other functions
    global y_hand_mod_left
    global y_hand_mod_right
    global key
    key = False
    
    #listens for every event
    for event in pygame.event.get():
        
        #quits when the user x's out of the window
        if event.type == pygame.QUIT:
            quit = True
            
        #stores what keys are currently held down
        held_keys = pygame.key.get_pressed()
        
        if held_keys[pygame.K_a]:
            key = True
            pile = 0
        elif held_keys[pygame.K_s]:
            key = True
            pile = 1
        elif held_keys[pygame.K_d]:
            key = True
            pile = 2
        elif held_keys[pygame.K_f]:
            key = True
            pile = 3
        elif held_keys[pygame.K_SPACE]:
            key = True
            pile = 4
        
        if held_keys[pygame.K_LEFT] and not held_keys[pygame.K_RIGHT]:
            #moves the hand up when the button is held
            hand = 'l'
            y_hand_mod_left = 50
            if key:
                if hands[hand]:
                    put_down(pile, hand)
                elif not hands[hand]:
                    if piles[pile]:
                        pick_up(pile, hand)
            elif held_keys[pygame.K_KP0]:
                if hands[hand]:
                    if hands[hand].get_flipped == True:
                        hands[hand].set_flipped(False)
                    elif hands[hand].get_flipped == False:
                        hands[hand].set_flipped(True)
        else:
            y_hand_mod_left = 0

        if held_keys[pygame.K_RIGHT] and not held_keys[pygame.K_LEFT]:
            #moves the hand up when the button is held
            hand = 'r'
            y_hand_mod_right = 50
            if key:
                if hands[hand]:
                    put_down(pile, hand)
                elif not hands[hand]:
                    if piles[pile]:
                        pick_up(pile, hand)
            elif held_keys[pygame.K_KP0]:
                if hands[hand]:
                    if hands[hand].get_flipped:
                        hands[hand].set_flipped(False)
                    else:
                        hands[hand].set_flipped(True)
        else:
            y_hand_mod_right = 0

            
    #makes the background white
    window.fill(white)
    #draws the piles of cards
    display_piles(5/7 * height)
    #draws the player's hands
    display_hand(1/3, y_hand_mod_left, 'l')
    display_hand(2/3, y_hand_mod_right, 'r')
    
    if piles[0]:
        print(piles[0][-1].get_flipped())
    if hands['l']:
        print(hands['l'].get_flipped())

    #updates screen
    pygame.display.update()
    #frame rate locked to 60
    pygame.time.Clock().tick(60)

while not quit:
    game_loop()

pygame.quit()
quit()