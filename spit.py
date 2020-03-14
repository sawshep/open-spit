import pygame as pg
import socket
from threading import Thread
from random import shuffle
pg.init()

#window dimensions, used for calculations too
width = 1280
height = 720

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)

#the \u266- numbers are unicode characters for the suits
suits = {
    'SPADES':'\u2660',
    'CLUBS':'\u2663',
    'HEARTS':'\u2665',
    'DIAMONDS':'\u2666'
    }

#make this a list of tuples to preserve the key for future calculations?
values = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}


deck = []
#fills deck with cards, shuffles
for s in suits:
    for v in values:
        #the values from both values and suits. Might change to a list of tuples in order to preserve numerical value
        deck.append(values[v] + suits[s])
shuffle(deck)
print(deck)

pile_numbers = {}
cards_in_pile = []
#number of piles in front of player
for p in range(5):
    #number of face down cards in each pile
    for c in range(p):
        cards_in_pile.append((deck[0], False))
        del deck[0]
    #one face up card on top
    cards_in_pile.append((deck[0], True))
    del deck[0]
    #assigns the cards to a pile and moves to the next
    pile_numbers[p] = cards_in_pile
    cards_in_pile = []

print(pile_numbers)

#sets up window
window = pg.display.set_mode((width, height))
pg.display.set_caption('Open-Spit')

quit = False

def display_text(text, x_cord, y_cord):
    if text[len(text) - 1] == '\u2660' or '\u2663':
        color = black
    elif text[len(text) - 1] == '\u2665' or '\u2666':
        color = red
    font = pg.font.Font('freesansbold.ttf', 18)
    text_object = font.render(text, True, color, white)
    window.blit(text_object, (x_cord, y_cord))

#Does nothing as of now
def main_menu():
    main_menu = True
    while main_menu:
        pass

#Draws the player's hands
def draw_hands(x_mod, y_mod):
    #the x coordinate is the width times a fraction rounded to a whole number
    x_cord = int(width * x_mod)
    #the y coordinate is the height minus the y coordinate modifier (this is what makes the hand move) minus 25.
    y_cord = (height - y_mod - 25)
    pg.draw.rect(window, black, [x_cord, y_cord, 100, 100])

def draw_piles(y_cord):
    for pile in pile_numbers:
        #the x coordinate is the width divided by the number of piles plus the width divided by the number of piles (to even out spacing)
        x_cord = int(((width / (len(pile_numbers) + 1)) * pile) + (width / (len(pile_numbers) + 1)))
        #int(width * (pile / (len(pile_numbers) + 1)) + 50)
        pg.draw.rect(window, black, [x_cord, y_cord, 100, 100])
        #displays the numerical value and suit of the card on the top of the pile
        display_text(pile_numbers[pile][len(pile_numbers[pile]) - 1][0], x_cord, y_cord)

#For now this prints the card value and suit in CLI. In the future, this will move the card from the top of the pile to one of the player's hands
def pick_up(pile):
    #gets the top card
    a = pile_numbers[pile][len(pile_numbers[pile]) - 1]
    print(a)

def game_loop():
    #makes the hand_mod vars global so they can be used in other functions
    global y_hand_mod_left
    global y_hand_mod_right
    #listens for every event
    for event in pg.event.get():
        #quits when the user x's out of the window
        if event.type == pg.QUIT:
            quit = True
        #stores what keys are currently held down
        held_keys = pg.key.get_pressed()

    #Put this whole thing in a function?:
        #Detects the modifier key of <
        #Need to make it so the values are only printed when the card is True
        if held_keys[pg.K_LEFT] and not held_keys[pg.K_RIGHT]:
            #moves the hand up when the button is held
            y_hand_mod_left = 50
            if held_keys[pg.K_a]:
                pick_up(0)
            elif held_keys[pg.K_s]:
                pick_up(1)
            elif held_keys[pg.K_d]:
                pick_up(2)
            elif held_keys[pg.K_f]:
                pick_up(3)
            elif held_keys[pg.K_SPACE]:
                pick_up(4)
        #keeps hand still when not holding <
        else:
            y_hand_mod_left = 0

        #Detects the modifier key of >
        #Need to make it so the values are only printed when the card is True
        if held_keys[pg.K_RIGHT] and not held_keys[pg.K_LEFT]:
            #moves the hand up when the button is held
            y_hand_mod_right = 50
            if held_keys[pg.K_a]:
                pick_up(0)
            elif held_keys[pg.K_s]:
                pick_up(1)
            elif held_keys[pg.K_d]:
                pick_up(2)
            elif held_keys[pg.K_f]:
                pick_up(3)
            elif held_keys[pg.K_SPACE]:
                pick_up(4)
        #keeps hand still when not holding >
        else:
            y_hand_mod_right = 0

    #makes the background white
    window.fill(white)

    #draws the piles of cards
    draw_piles(5/7 * height)
    #draws the player's hands
    draw_hands(1/3, y_hand_mod_left)
    draw_hands(2/3, y_hand_mod_right)

    #updates what is draws on screen 60 times every second
    pg.display.update()
    #frame rate locked to 60
    pg.time.Clock().tick(60)

while not quit:
    game_loop()

#quits the game
pg.quit()
quit()

#TODO: complete pick_up() so the card is del from pile_numbers[pile]
    #del pile_numbers[pile][len(pile_numbers) - 1] to get rid of card on top
    #ALSO: make it so cards only show the numerical value when they are True
    #ALSO ALSO: make it so the cards are colored properly with their suit in the game window
