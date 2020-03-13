import pygame as pg
import socket
from threading import Thread
from random import shuffle
pg.init()

x = 800
y = 600

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

pile_number = {}
cards_in_pile = []

#number of piles in front of player
for p in range(1, 6):
    cards_in_pile.append((deck[0], True))
    del deck[0]
    for c in range(1, p):
        cards_in_pile.append((deck[0], False))
        del deck[0]
    pile_number[p] = cards_in_pile
    cards_in_pile = []
#Make the last card on the pile be true^^^^

print(pile_number)

window = pg.display.set_mode((x, y))
pg.display.set_caption('Open-Spit')
clock = pg.time.Clock()

quit = False

#--------------------------------


def main_menu():
    main_menu = True
    while main_menu:
        for event in pygame.event.get():
            pygame.quit()
            quit()

def hands(x_mod, ini_height, y_mod):
    pg.draw.rect(window, black, [int(x * x_mod), ini_height - y_mod, 100, 100])

def piles(x, y):
    for d in range(1, 6):
        pg.draw.rect(window, black, [x - d * 5, y - d * 5, 100, 100])

def pick_up(pile):
    a = pile_number[pile][0]
    print(a)

def game_loop():
    global y_change_right
    global y_change_left
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit = True
            pg.quit()
            quit()

        held_keys = pg.key.get_pressed()
        if held_keys[pg.K_LEFT] and not held_keys[pg.K_RIGHT]:
            y_change_left = 50
            if held_keys[pg.K_a]:
                pick_up(1)
            elif held_keys[pg.K_s]:
                pick_up(2)
            elif held_keys[pg.K_d]:
                pick_up(3)
            elif held_keys[pg.K_f]:
                pick_up(4)
            elif held_keys[pg.K_SPACE]:
                pick_up(5)
        else:
            y_change_left = 0

        if held_keys[pg.K_RIGHT] and not held_keys[pg.K_LEFT]:
            y_change_right = 50
            if held_keys[pg.K_a]:
                pick_up(1)
            elif held_keys[pg.K_s]:
                pick_up(2)
            elif held_keys[pg.K_d]:
                pick_up(3)
            elif held_keys[pg.K_f]:
                pick_up(4)
            elif held_keys[pg.K_SPACE]:
                pick_up(5)
        else:
            y_change_right = 0

    window.fill(white)
    hands(0.25, y - 50, y_change_left)
    hands(0.65, y - 50, y_change_right)
    piles(100, 100)


    pg.display.update()
    clock.tick(60)

#--------------------------------

while not quit:
    game_loop()
