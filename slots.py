#!/usr/bin/env python3
# slots.py
# A slot machine!

import pygame
from os import listdir
from random import randint, choice


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


# Not sure if pygame has a builtin so im creating this
def pos_inside_rect(rect, pos):
    """
    Returns whether or not a position is inside a rect
    :param rect: pygame Rect object
    :param pos: (x, y) coordinate
    :return: bool
    """
    # Get coordinates
    # In a pygame coord system:
    # x, y = top left
    # x1, y2 = top right
    rect_x, rect_y = rect.x, rect.y
    rect_x1, rect_y1 = rect_x + rect.width, rect_y + rect.height

    return (rect_x <= pos[0] <= rect_x1) and (rect_y <= pos[1] <= rect_y1)


def load_images(directory):
    """
    Load all images from a directory into a list so that they can be
    then drawn by pygame
    """
    # Placeholder
    img_files = listdir(directory)

    # TODO: Consider if making imgs a dict is worth it
    # The key would be the filename. This could make debugging and such easier
    # but i dont know if itd have any use in the code

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


def generate_roll(ls, columns, rolls):
    """
    Generate a list for each column consisting of a rolls amount of
    random items picked of syms
    :param ls: a list, any list
    :param columns: the amount of columns to be generated
    :param rolls: the amount of rolls per columns, useful for making
    the roll animation.
    :return: 2D list
    """
    generated = []

    # For each column
    for i in range(columns):
        # Generate a list with rolls amount of random items from ls
        # Then add it to the list of stuff that has been generated
        generated.append([choice(ls) for _ in range(rolls)])

    return generated


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

            # TODO: Maybe key event stuff inside a func? Consider.
            # Simply call it with the event
            #
            # Only check for keys when a key has been pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("SCATTER!")
                    for i in range(len(symbols)):
                        symbols[i][1].update((randint(0, width), randint(0, height)), symbols[i][1].size)

            # Check for mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If ANY mouse button has been pressed, print if the
                # cursor was inside the image
                for i in range(len(symbols)):
                    print(pos_inside_rect(symbols[i][1], pygame.mouse.get_pos()))

        screen.fill(Color.white)

        # Use blit to draw images
        # screen.blit(img, rect)
        for i in range(len(symbols)):
            screen.blit(symbols[i][0], symbols[i][1])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
