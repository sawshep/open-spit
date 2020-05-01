import pygame

# Each pygame.
valid_keys = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_KP0,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f,
    pygame.K_SPACE
]

def get_keys():
    # For some reason pygame.key.get_pressed() only works if it loops for each event
    for _event in pygame.event.get():
        pressed_keys = []
        for valid_key in valid_keys:
            if pygame.key.get_pressed()[valid_key]:
                pressed_keys.append(valid_key)
        return pressed_keys