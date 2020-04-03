import pygame
from random import shuffle
import socket

#Initiallizes Pygame
pygame.init()

#Window resolution
width = 1280
height = 960

#Sets the window resoloution
window = pygame.display.set_mode((width, height))
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

#Framework for cards
class Card:
    #Makes local variables equal the parameters
    def __init__(self, value_pair, suit):    
        #Numerical value for calcs
        self.value = value_pair[0]
        #Face value for graphics
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

#In the future this will simplify the mechanics and graphics
class User:
    def __init__(self, piles, hands, center_pile):
        self.piles = piles
        self.hands = hands
        self.center_pile = center_pile
    def get_piles(self):
        return self.piles
    def get_hands(self):
        return self.hands
    def get_center_pile(self):
        return self.center_pile


def make_user_data():
    #deck is a list of Card objects made from the values and suits
    deck = []
    for suit in suits:
        for value_pair in value_pairs:
            deck.append(Card(value_pair, suit))
    shuffle(deck)

    #Creates two users with respective data, one for host and one for client
    for is_host in [True, False]:
        piles = []
        #Every sequential pile in the list of piles has one more card Obj. than the last
        for pile_number in range(5):
            pile = []
            for card in range(pile_number + 1):
                pile.append(deck[0])
                del deck[0]
            #The last card in every pile is flipped up
            pile[-1].set_flipped(True)
            piles.append(pile)
            
        #For both users, both hands start empty
        hands = {0:None, 1:None}
        center_pile = [deck[0]]
        del deck[0]
        
        #TODO: Wrap this in a function?
        if is_host:
            global host
            host = User(piles, hands, center_pile)
        elif not is_host:
            global client
            client = User(piles, hands, center_pile)
            
make_user_data()
quit = False

def display_card(text, x_cord, y_cord):
    font = pygame.font.Font('./ibm.ttf', 40)
    if text[1] == '\u2660' or text[1] == '\u2663':
        foreground_color = black
    else:
        foreground_color = red
    text_object = font.render(text, True, foreground_color, white)
    window.blit(text_object, (x_cord,y_cord))
    
def display_hand(x_frac, y_mod, hand):
    x_cord = int(width * x_frac)
    y_cord = (height - y_mod - 25)
    pygame.draw.rect(window, black, [x_cord, y_cord, 100, 100])
    if hand:
        text = hand.get_face() + hand.get_suit()
        display_card(text, x_cord, y_cord)
    
def display_piles(y_cord, piles):   
    for pile in range(len(piles)):
        pile_spacing = width / (len(piles) + 1)
        x_cord = int(pile_spacing * pile + pile_spacing)
        if piles[pile]:  
            if piles[pile][-1].get_flipped():
                pygame.draw.rect(window, white, [x_cord, y_cord, 100, 100])
                text = piles[pile][-1].get_face() + piles[pile][-1].get_suit()
                display_card(text, x_cord, y_cord)
            else:
                pygame.draw.rect(window, light_blue, [x_cord, y_cord, 100, 100])
                
#Eventually, you will be able to play a card on a center pile.
def display_center_pile(x_frac, y_frac, user):
    if user.get_center_pile():
        x_cord = int(width * x_frac)
        y_cord = int(height * y_frac)
        pygame.draw.rect(window, white, [x_cord, y_cord, 100, 100])
        text = user.get_center_pile()[-1].get_face() + user.get_center_pile()[-1].get_suit()
        display_card(text, x_cord, y_cord)
        
def play_mechanics(user, hand, play_pile):
    if user.get_hands()[hand]:
        if abs(user.get_hands()[hand].get_value() - play_pile.get_center_pile()[0].get_value()) == 1 or abs(user.get_hands()[hand].get_value() - play_pile.get_center_pile()[0].get_value()) == 12:
            play_pile.get_center_pile().append(user.get_hands()[hand])
            user.get_hands()[hand] = None

def hand_mechanics(user, hand, pile):
    #And if user has a card in their selected hand...
    if user.get_hands()[hand]:
        #And if there is nothing in the selected pile, or if the value of the card in user's selected hand equals the top card of the selected deck, or the card is face-down
        if not user.get_piles()[pile] or user.get_hands()[hand].get_value() == user.get_piles()[pile][-1].get_value() or not user.get_piles()[pile][-1].get_flipped():
            #Adds the card in a selected hand to the top of the selected deck
            user.get_piles()[pile].append(user.get_hands()[hand])
            #Clears the selected hand
            user.get_hands()[hand] = None
    #And if there is a card in the selected pile, and if the top card on the selected deck is face-up
    elif not user.get_hands()[hand] and user.get_piles()[pile] and user.get_piles()[pile][-1].get_flipped():
        #Makes the selected hand hold the top card of the selected deck
        user.get_hands()[hand] = user.get_piles()[pile][-1]
        #Deletes the top card from the selected
        del user.get_piles()[pile][-1]
        
#All the logic that controls when certain mechanics should take place. Mainly helps with graphics
def hand_logic(user):
    global pile_key
    pile_key = False
    global play_key
    play_key = False
    
    held_keys = pygame.key.get_pressed()
    
    if held_keys[pygame.K_a]:
        pile_key = True
        pile = 0
    elif held_keys[pygame.K_s]:
        pile_key = True
        pile = 1
    elif held_keys[pygame.K_d]:
        pile_key = True
        pile = 2
    elif held_keys[pygame.K_f]:
        pile_key = True
        pile = 3
    elif held_keys[pygame.K_SPACE]:
        pile_key = True
        pile = 4
    
    users = [host, client]
    if held_keys[pygame.K_UP]:
        play_key = True
        users.remove(user)
        play_pile = users[0]
    elif held_keys[pygame.K_DOWN]:
        play_key = True
        play_pile = user
    
    global y_hand_mod_left
    global y_hand_mod_right
    if held_keys[pygame.K_LEFT] and not held_keys[pygame.K_RIGHT] and not held_keys[pygame.K_KP0]:
        #moves the hand up when the button is held
        hand = 0
        y_hand_mod_left = 50
        y_hand_mod_right = 0
        if pile_key:
            hand_mechanics(user, hand, pile)
        elif play_key:
            play_mechanics(user, hand, play_pile)
            
    elif held_keys[pygame.K_RIGHT] and not held_keys[pygame.K_LEFT] and not held_keys[pygame.K_KP0]:
        #moves the hand up when the button is held
        hand = 1
        y_hand_mod_left = 0
        y_hand_mod_right = 50
        if pile_key:
            hand_mechanics(user, hand, pile)
        elif play_key:
            play_mechanics(user, hand, play_pile)
            
    elif held_keys[pygame.K_KP0] and not held_keys[pygame.K_LEFT] and not held_keys[pygame.K_RIGHT]:
        y_hand_mod_left = 50
        y_hand_mod_right = 50
        if pile_key and user.get_piles()[pile]:
            user.get_piles()[pile][-1].set_flipped(True)

    else:
        y_hand_mod_left = 0
        y_hand_mod_right = 0
        
def game_loop():
    global pile_key
    pile_key = False
    
    #listens for every event
    for event in pygame.event.get():
        
        #quits when the user x's out of the window
        if event.type == pygame.QUIT:
            quit = True
            
        hand_logic(host)
        #hand_logic(client)
            
            
    #makes the background grey
    window.fill(grey)
    #draws the users' piles of cards
    
    display_piles(6/8 * height, host.get_piles())
    display_piles(2/8 * height, client.get_piles())

    display_hand(1/3, y_hand_mod_left, host.get_hands()[0])
    display_hand(2/3, y_hand_mod_right, host.get_hands()[1])
    display_hand(1/3, height + 30, client.get_hands()[0])
    display_hand(2/3, height + 30, client.get_hands()[1])
    
    display_center_pile(1/2, 3/5, host)
    display_center_pile(1/2, 2/5, client)

    #updates screen
    pygame.display.update()
    #frame rate locked to 60
    pygame.time.Clock().tick(60)

while not quit:
    game_loop()

pygame.quit()
quit()