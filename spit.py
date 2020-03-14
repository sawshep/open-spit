import pygame as pg
import socket
from threading import Thread
from random import shuffle
pg.init()

#window dimensions
width = 1280
height = 720

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)

suits = {
    'SPADES':'\u2660',
    'CLUBS':'\u2663',
    'HEARTS':'\u2665',
    'DIAMONDS':'\u2666'
    }

values = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}

deck = []
for s in suits:
    for v in values:
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

window = pg.display.set_mode((width, height))
pg.display.set_caption('Open-Spit')
clock = pg.time.Clock()

quit = False

def display_text(text, x_cord, y_cord):
    if text[len(text) - 1] == '\u2660' or '\u2663':
        color = black
    elif text[len(text) - 1] == '\u2665' or '\u2666':
        color = red
    font = pg.font.Font('freesansbold.ttf', 18)
    text_object = font.render(text, True, color, white)
    window.blit(text_object, (x_cord, y_cord))

def main_menu():
    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            pygame.quit()
            quit()

def draw_hands(x_mod, y_mod):
    x_cord = int(width * x_mod)
    y_cord = (height - y_mod - 25)
    pg.draw.rect(window, black, [x_cord, y_cord, 100, 100])

def draw_piles(y_cord):
    for pile in pile_numbers:
        x_cord = int(((width / (len(pile_numbers) + 1)) * pile) + (width / (len(pile_numbers) + 1)))
        #int(width * (pile / (len(pile_numbers) + 1)) + 50)
        pg.draw.rect(window, black, [x_cord, y_cord, 100, 100])
        display_text(pile_numbers[pile][len(pile_numbers[pile]) - 1][0], x_cord, y_cord)

def pick_up(pile):
    a = pile_numbers[pile][len(pile_numbers[pile]) - 1]
    print(a)

def game_loop():
    global y_hand_mod_left
    global y_hand_mod_right
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True
            pg.quit()
            quit()
        held_keys = pg.key.get_pressed()
        if held_keys[pg.K_LEFT] and not held_keys[pg.K_RIGHT]:
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

        else:
            y_hand_mod_left = 0

        if held_keys[pg.K_RIGHT] and not held_keys[pg.K_LEFT]:
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
        else:
            y_hand_mod_right = 0

    window.fill(white)

    draw_piles(5/7 * height)
    draw_hands(1/3, y_hand_mod_left)
    draw_hands(2/3, y_hand_mod_right)

    pg.display.update()
    clock.tick(60)

while not quit:
    game_loop()
