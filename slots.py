#!/usr/bin/env python3
# slots.py
# A slot machine!

import pygame

def screen_size():
    """
    Set screen size
    """
    return 600, 600


def main():
    pygame.init()

    size = width, height = screen_size()

    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
