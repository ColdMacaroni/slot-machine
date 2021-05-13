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
        if isinstance(other, SlotSymbol) or isinstance(other, WildSymbol):
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


def generate_values(amount,
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


def update_slots(slots, new_slots):
    """
    Adds new rolls to the slots so that they can be rolled again
    """
    for column in range(len(slots)):
        slots[column] = new_slots[column] + slots[column]

    return slots


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

        # TODO: Different amounts depending on the type
        # E.g. Default cards appear more than wilds so there should be
        # twice as many defaults as there are wilds.
        imgs.append(SlotSymbol(screen, img,
                               path.join(*directory, img_files[img]),
                               value=None, size=symbol_size))

    # -- Load values
    # Create values
    # Idk about actual values so uh yeah
    wild_val, values = generate_values(len(imgs))

    # Assign the values
    for i in range(len(imgs)):
        imgs[i].value = values[i]

    # Add the wild symbol with a special id
    if wild is not None:
        imgs.append(WildSymbol(screen, -1, path.join(*directory, wild),
                               value=wild_val, size=symbol_size))

    # Load all images
    # This is done so that they dont have to be loaded
    # for every copy
    for img in imgs:
        img.load_image()

    return imgs


def del_out_of_bounds(slots, lower_bound):
    """
    :param slots: List generated by generate_rolls()
    :param lower_bound: A y coordinate to rm objects beyond it.
    """
    # Cycle through the item
    # Can't del because i'm looping through the list!
    new_slots = []
    for column in range(len(slots)):
        new_column = []

        # Create a new column
        for symbol in range(len(slots[column])):
            if not slots[column][symbol].get_y() > lower_bound:
                new_column.append(slots[column][symbol])

        new_slots.append(new_column)

    return new_slots


def move_symbols(slots, rows, top_fix,
                 speed=2):
    """
    Move the slots based on the y axis by the diff given
    """
    # Create a list of factors to multiply the speed for
    # this will make different columns roll different speeds
    speed_factors = list(range(1, len(slots) + 1))

    # Reverse it so the column at the left is the fastest
    speed_factors.reverse()

    for column in range(len(slots)):
        # Skip columns that are already at the target amount
        if len(slots[column]) == rows:
            # Fix misalignment issues
            # Get the difference between the highest row and the
            # expected top value
            y_diff = top_fix - slots[column][0].get_y()

            # Only run through the loop if the diff isnt 0
            if y_diff:
                for symbol in slots[column]:
                    symbol.set_y(symbol.get_y() + y_diff)

        else:
            # Set the speed for the column
            # Multiplying makes the column slow down as it stops
            column_speed = (speed_factors[column] * speed)\
                           * len(slots[column]) / 4
            for symbol in slots[column]:
                symbol.set_y(symbol.get_y() + column_speed)


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

    if return_whitespace:
        return horizontal_whitespace_width, vertical_whitespace_width


def draw_margins(screen, color, horizontal_width, vertical_width):
    """
    Draws margins on the given pygame surface
    :param screen: Pygame Surface
    :param color: RGB color value
    :param horizontal_width: Width of the horizontal in px
    :param vertical_width: Width of the vertical in px
    """
    screen_width, screen_height = screen_size()

    # Create a horizontal bar
    horizontal_bar = pygame.Rect((0, 0), (screen_width, horizontal_width))

    # Create a vertical bar
    vertical_bar = pygame.Rect((0, 0), (vertical_width, screen_height))

    # Draw em
    pygame.draw.rect(screen, color, horizontal_bar)
    pygame.draw.rect(screen, color, vertical_bar)

    # Shift the bars to the other side
    horizontal_bar.y = screen_height - horizontal_width
    vertical_bar.x = screen_width - vertical_width

    # Draw em again
    pygame.draw.rect(screen, color, horizontal_bar)
    pygame.draw.rect(screen, color, vertical_bar)


def add_xy(xy1, xy2):
    """
    Adds two xy coordinates together
    :param xy1: (x, y)
    :param xy2: (x, y)
    :return: (x, y)
    """
    return xy1[0] + xy2[0], xy1[1] + xy2[1]


def shift_points(points, shift):
    """
    Shifts each point in a list of points by the (x, y) given
    :param points: A list of (x, y) points
    :param shift: (x, y)
    :return: List
    """
    new_points = []
    for point in points:
        new_points.append(add_xy(point, shift))

    return new_points

# -- Line generators


def horizontal_lines(columns):
    """
    Generate the coordinates for a horizontal
    :param columns: Amount of columns to generate for
    :return: List
    """
    # Points along the x axis
    line = [(x, 0) for x in range(columns)]
    return line


def generate_lines(rows, columns):
    """
    Returns a 3D list of coordinates of the lines used to calculate
    scores
    """
    lines = []

    # There are multiple lines, each is generated by its respective function
    # They then are shifted as many times as needed to fill the screen

    # 4
    horizontal = horizontal_lines(columns)

    # Create one for each row
    all_horizontal = []
    for y in range(rows):
        # Create the same pattern at different y levels
        all_horizontal.append(shift_points(horizontal, (0, y)))

    # Add to the finallist
    lines.append(all_horizontal)

    return lines


def main():
    # Pygame set up
    pygame.init()

    size = width, height = screen_size()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # NOTE: Worth moving into functions or class?
    ROWS = 4
    COLUMNS = 5
    SYMBOL_SIZE = (100, 100)  # px
    SYMBOL_OFFSET = 15  # px

    # Load symbols
    # Path is a list to be used with path.join()
    symbols = load_images(screen, ["images", "symbols"], SYMBOL_SIZE)

    # 20 is a totally arbitrary number so uh feel free to change
    extra_rows = 20
    rolls = generate_roll(symbols, COLUMNS, ROWS)

    # Whitespace will be used to cover up images that are
    # drawn out of bounds + this position the images in a grid
    whitespace = position_slots(rolls, ROWS, SYMBOL_SIZE,
                                offset=SYMBOL_OFFSET,
                                return_whitespace=True)

    # Generate the lines used for checking the rolls
    lines = generate_lines(ROWS, COLUMNS)
    print(lines)

    # Game status thingies
    # TODO: Find a more efficient way of doing this
    rolling = False
    calculate_score = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # Only check for keys when a key has been pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not rolling:
                    # Generate more symbols to add on top of the
                    # Current ones
                    new_rolls = generate_roll(symbols, COLUMNS,
                                              extra_rows)

                    rolls = update_slots(rolls, new_rolls)

                    # Put them into position
                    position_slots(rolls, ROWS, SYMBOL_SIZE,
                                   offset=SYMBOL_OFFSET)

                    rolling = True

            # Check for mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Call function for processing the button clicks
                pass
                # If ANY mouse button has been pressed, print if the
                # cursor was inside the image
                #for i in range(len(symbols)):
                #    print(pos_inside_rect(symbols[i][1], pygame.mouse.get_pos()))

        # Clear screen
        screen.fill(Color.white)

        if rolling:
            # Move the columns
            move_symbols(rolls, ROWS, whitespace[0])

            # Delete rolls that are out of the margins
            # By substracting the offset*3, the symbols always end up aligned
            lower_bound = screen_size()[1] - whitespace[1] - SYMBOL_OFFSET * 3
            rolls = del_out_of_bounds(rolls, lower_bound)

            # This will get a list of the amount of rows that need to
            # be removed before reaching the target amount of rolls
            rows_to_target = [len(roll) - ROWS for roll in rolls]

            if sum(rows_to_target) == 0:
                # This condition will trigger when all columns have
                # reached the ROWS amount

                # Re-position slots in case of any misalignment
                position_slots(rolls, ROWS, SYMBOL_SIZE)

                # Update the current status
                rolling = False
                calculate_score = True

        elif calculate_score:
            pass

        # Draw the slots
        for column in rolls:
            for symbol in column:
                symbol.draw()

        # Cover up slots
        draw_margins(screen, Color.white, *whitespace)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
