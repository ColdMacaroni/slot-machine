#!/usr/bin/env python3
# slots.py
# A slot machine!

import pygame
from os import listdir, path
from random import randint, choice

# Use deepcopy when selecting from the list, this way the x, y and
# other attributes can be changed independently
from copy import copy


class SlotSymbol:
    def __init__(self, surface, sym_id, filename, value,
                 size=(75, 75), pos=(0, 0), color_key=(0, 0, 0)):
        """
        Generate an image to be used in the slot machine
        :param surface: Pygame surface
        :param sym_id: An integer that is used for comparison
        :param filename: The file name for the image to be loaded
        :param value: The value to be used in calculating scores

        :keyword size: Tuple with size of image in px
        :keyword pos: X,Y position the image will be drawn at
        :keyword color_key: The rgb color to be used as transparency
        """
        # Params
        self.surface = surface
        self.sym_id = sym_id
        self.filename = filename
        self.value = value

        # Key words
        self.width, self.height = size
        self.x, self.y = pos
        self.color_key = color_key

        # To be changed by self.load_images()
        self.image = None
        self.rect = None

    def __eq__(self, other):
        # Comparison to be done by IDs instead of objects themselves
        if isinstance(other, SlotSymbol):
            return self.sym_id == other.sym_id

        else:
            return False

    # -- Set Methods
    # X
    def set_x(self, x):
        """
        Updates the object's x coordinate
        :param x: A number, any number
        """
        self.x = x

        # Also update rect if defined
        if self.rect is not None:
            self.rect.x = self.x

    # Y
    def set_y(self, y):
        """
        Updates the object's y coordinate
        :param y: A number, any number
        """
        self.y = y

        # Also update rect if defined
        if self.rect is not None:
            self.rect.y = self.y

    # X, Y
    def set_pos(self, pos):
        """
        A shortcut to set_x and set_y
        :param pos: Tuple
        """
        if type(pos) == tuple and len(pos) == 2:
            self.set_x(pos[0])
            self.set_y(pos[1])

        else:
            raise ValueError('Position should be a tuple consisting '
                             'of x and y coordinates')

    # These are pretty much the same as the x, y ones
    # Width
    def set_width(self, width):
        """
        Updates the object's width
        :param width: Width in px
        """
        self.width = width

        if self.rect is not None:
            self.rect.width = self.width

    # Height
    def set_height(self, height):
        """
        Updates the object's height
        :param height: height in px
        """
        self.height = height

        if self.rect is not None:
            self.rect.height = self.height

    # Width, Height
    def set_size(self, size):
        """
        A shortcut to set_width and set_height
        :param size: Tuple
        """
        if type(size) == tuple and len(size) == 2:
            self.set_height(size[0])
            self.set_width(size[1])

        else:
            raise ValueError('Size should be a tuple consisting '
                             'of width and height values in px')

    # Value
    def set_value(self, value):
        """
        Setting the value!
        """
        self.value = value

    # -- Get methods
    # X
    def get_x(self):
        """
        Returns the object's x value
        :return: Number
        """
        return self.x

    # Y
    def get_y(self):
        """
        Returns the object's y value
        :return: Number
        """
        return self.y

    # X, Y
    def get_pos(self):
        """
        Shortcut to get_x and get_y
        :return: Tuple
        """
        return self.get_x(), self.get_y()

    # Width
    def get_width(self):
        return self.width

    # Height
    def get_height(self):
        return self.height
    # Width, Height
    # Value
    # --

    def load_image(self):
        """
        Loads this objects pygame image into its variables
        """
        # Convert transforms the image into a faster-to-draw format
        self.image = pygame.image.load(self.filename).convert()

        # Scales the image to the specified size
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

        # Treat the given color key as transparent
        self.image.set_colorkey(self.color_key)

        # Get rect object
        self.rect = self.image.get_rect()

        # Update rect obj
        self.rect.update((self.x, self.y), (self.width, self.height))

    def draw(self):
        """
        Blits the image into the surface
        """
        # These updates are handled by the set methods but i am
        # Also including them here in case they are set directly
        # (Which you shouldn't do!)

        # Update rect obj
        self.rect.update((self.x, self.y), (self.width, self.height))

        # Resize img
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

        # Draw image
        self.surface.blit(self.image, self.rect)


# Subclass
class WildSymbol(SlotSymbol):
    def __eq__(self, other):
        if isinstance(other, SlotSymbol):
            # A Wild card will always match with others
            return True

        else:
            return False


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


def create_values(amount,
                  wild_val=5, default_val=10,
                  max_val=60, big_vals=3):
    """
    Create a list of values according to the amount given and
    parameters
    :return:
    """
    values = []

    # Reduce the amount
    if big_vals > amount:
        big_vals = amount

    # Generate big values
    for i in range(big_vals):
        values.append(max_val - wild_val * i)

    # Generate default values
    for _ in range(amount - len(values)):
        values.append(default_val)

    if len(values) != amount:
        raise ValueError("Amount and values arent the same.\n"
                         "Amount: {}, Values: {}. {}".format(amount, len(values), values))

    return wild_val, values


def load_images(screen, directory, symbol_size):
    """
    Load all images from a directory into a list so that they can be
    then drawn by pygame
    """
    img_files = listdir(path.join(*directory))
    # TODO: Pass img_files through isfile()

    imgs = []
    wild = None
    # Create symbol objects
    for img in range(len(img_files)):
        # I dont know why pycharm expects an int
        if "wild" in img_files[img]:
            # The wild symbol will be done after
            wild = img_files[img]
            continue

        imgs.append(SlotSymbol(screen, img,
                               path.join(*directory, img_files[img]),
                               value=None, size=symbol_size))

    # -- Load values
    # Create values
    # Idk about actual values so uh yeah
    wild_val, values = create_values(len(imgs))

    # Assign the values
    for i in range(len(imgs)):
        imgs[i].value = values[i]

    # Add the wild symbol with a special id
    if wild is not None:
        imgs.append(WildSymbol(screen, -1, wild, wild_val))

    # Load all images
    # This is done so that they dont have to be loaded
    # for every copy
    for img in imgs:
        img.load_image()

    return imgs


# TODO: Change this to support the class
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
        column_rolls = []
        for j in range(rolls):
            # Create a copy of a random item from the list
            item = copy(ls[randint(0, len(ls) - 1)])

            # Add to the rolls
            column_rolls.append(item)

        # Add to the columns
        generated.append(column_rolls)

    return generated


def move_symbols(slots, y_diff):
    """
    Move the slots based on the y axis by the diff given
    """
    pass


def position_slots(slots, rows, slot_size,
                   offset=15, return_whitespace=False):
    """"
    Position the slots spaced out and centered on the screen in a grid
    Calculating the whitespace is a by-product that actually proves
    useful

    """
    # Add together the width of each column, same for row
    grid_width = slot_size[0] * len(slots)
    grid_height = slot_size[1] * rows

    # Add the offsets to the width, same for row
    grid_width += (len(slots) - 1) * offset
    grid_height += (rows - 1) * offset

    screen_width, screen_height = screen_size()

    # Move all the items by the offset so that the grid is centered
    x_offset = (screen_width / 2) - (grid_width / 2)
    vertical_whitespace_width = x_offset

    horizontal_whitespace_width = (screen_height / 2) - (grid_height / 2)
    y_offset = horizontal_whitespace_width + grid_height

    # Having this here avoids affecting all the images
    if return_whitespace:
        return horizontal_whitespace_width, vertical_whitespace_width

    # This spaces out the elements
    for column in range(len(slots)):
        # In each column
        for symbol in range(len(slots[column])):
            # Per row
            # Get the obj in a variable for easier method access
            current_symbol = slots[column][symbol]

            # Get an offset based on the size of the symbol
            x = column * (current_symbol.get_width() + offset)
            y = symbol * (current_symbol.get_height() + offset)

            current_symbol.set_pos((x, y))

    # This moves each element by the offset
    for column in range(len(slots)):
        # Each column may have a different amount of rows, why? Idk lmao
        # The amount of columns though is ok to be handled by the other ones.
        # First get the total height of the rows
        num_rows = len(slots[column])
        total_column_height = num_rows * slot_size[1] + (num_rows - 1) * offset

        # Then to move the columns up, their y should have substracted total_column_height
        # This will position the lowest y at 0. The top edge of the screen
        # Then move each element down (add to y) by the y offset
        # This can be simplified to the following math thing
        final_y_offset = -total_column_height + y_offset

        for symbol in range(len(slots[column])):
            # Per row
            # Get the obj in a variable for easier method access
            current_symbol = slots[column][symbol]

            current_symbol.set_x(current_symbol.get_x() + x_offset)
            current_symbol.set_y(current_symbol.get_y() + final_y_offset)


def create_margins(screen, color, horizontal_width, vertical_width):
    """
    Draws margins on the given pygame surface
    :param screen: Pygame Surface
    :param color: RGB color value
    :param horizontal_width: Width of the horizontal in px
    :param vertical_width: Width of the vertical in px
    """
    pass

def main():
    # Pygame set up
    pygame.init()

    size = width, height = screen_size()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # NOTE: Worth moving into functions or class?
    ROWS = 3
    COLUMNS = 4
    SYMBOL_SIZE = (100, 100)  # px

    # Load symbols
    # Path is a list to be used with path.join()
    symbols = load_images(screen, ["images", "symbols"], SYMBOL_SIZE)

    # 20 is a totally arbitrary number so uh feel free to change
    rolls = generate_roll(symbols, COLUMNS, ROWS + 20)

    running = True
    while running:
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
                    rolls = generate_roll(symbols, COLUMNS, ROWS + 20)

            # Check for mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # If ANY mouse button has been pressed, print if the
                # cursor was inside the image
                #for i in range(len(symbols)):
                #    print(pos_inside_rect(symbols[i][1], pygame.mouse.get_pos()))

        screen.fill(Color.white)

        position_slots(rolls, ROWS, SYMBOL_SIZE)

        for column in rolls:
            for symbol in column:
                symbol.draw()
        # TODO: Update to work with the class
        # Use blit to draw images
        # screen.blit(img, rect)
        #for i in range(len(symbols)):
        #    screen.blit(symbols[i][0], symbols[i][1])

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
