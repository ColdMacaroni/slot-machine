#!/usr/bin/env python3
# slots.py
# A slot machine!

import pygame
from os import listdir
from random import randint

class Color:
    # This class is for quickly accessing different colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

def screen_size():
    """
    Set screen size
    """
    return 600, 600


def load_images(directory):
    """
    Load all images from a directory into a list so that they can be
    then drawn by pygame
    """
    # Placeholder
    img_files = listdir(directory)

    imgs = []
    for img in img_files:
        # Convert transfors the image into a faster-to-draw format
        image = pygame.image.load(f'{directory}/{img}').convert()

        # Resize
        image = pygame.transform.scale(image, (75, 75))

        # This will treat pure black as transparent
        image.set_colorkey(Color.black)

        # This generates a rectangle object in which the
        # image will be drawn
        # The rectangle can be updated with Rect.update((x, y), (width, height))
        # (x,y) = top left
        #
        # if obj is Rect:
        # obj.update((new_x, new_y), (obj.width), (obj.height))
        # By default created with top-left at 0, 0
        image_rect = image.get_rect()

        imgs.append([image, image_rect])

    return imgs


def main():
    # Pygame set up
    pygame.init()

    size = width, height = screen_size()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # Load symbols
    symbols = load_images("images/symbols")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # Only check for keys when a key has been pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("SCATTER!")
                    for i in range(len(symbols)):
                        symbols[i][1].update((randint(0, width), randint(0, height)), symbols[i][1].size)

        screen.fill(Color.white)

        # Use blit to draw images
        # screen.blit(img, rect)
        for i in range(len(symbols)):
            screen.blit(symbols[i][0], symbols[i][1])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
