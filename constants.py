'''constants.py
Various constants that are utilized in different modules across the whole program'''

#Unicode characters for suits
SUITS = [
    '\u2660',
    '\u2663',
    '\u2665',
    '\u2666'
]

#A calculation value and a face value for the cards
VALUE_PAIRS = [
    (1, 'A'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, 'J'),
    (12, 'Q'),
    (13, 'K')
]

#Colors: Tuples with RGB values from 0 to 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (50, 150, 255)
GRAY = (115, 115, 115)
GREEN = (0, 255, 0)
