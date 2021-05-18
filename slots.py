#!/usr/bin/env python3
# slots.py
# A slot machine!

import pygame
from os import listdir, path
from random import randint

# Use deepcopy when selecting from the list, this way the x, y and
# other attributes can be changed independently
from copy import copy


class SlotSymbol:
    def __init__(self, surface, sym_id, filename, value,
                 size=(75, 75), pos=(0, 0), color_key=(0, 0, 0),
                 margin_color=(221, 215, 50), margin_width=2):
        """
        Generate an image to be used in the slot machine
        :param surface: Pygame surface
        :param sym_id: An integer that is used for comparison
        :param filename: The file name for the image to be loaded
        :param value: The value to be used in calculating scores

        :keyword size: Tuple with size of image in px
        :keyword pos: X,Y position the image will be drawn at
        :keyword color_key: The rgb color to be used as transparency
        :keyword margin_color: RGB color for the margin
        :keyword margin_width: Width in px for the margin
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

        self.margin_color = margin_color  # Gold
        self.margin_width = margin_width

        # To be changed by self.load_images()
        self.image = None
        self.rect = None

        # To be changed by outside code
        self.margin = False

    def __eq__(self, other):
        # Comparison to be done by IDs instead of objects themselves
        if isinstance(other, SlotSymbol):
            return self.sym_id == other.sym_id

        else:
            return False

    def __repr__(self):
        return f"{self.__class__} {self.filename}"

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

    def set_margin(self, boolean):
        """
        Sets whether to display the margin or not
        """
        self.margin = boolean

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

        # Margin
        if self.margin:
            self.draw_margin()

    def draw_margin(self):
        """
        Draws a margin for the image
        """
        # Calculate coordinates
        top_left = self.get_pos()
        top_right = (top_left[0] + self.get_width(), top_left[1])
        bottom_right = (top_right[0], top_right[1] + self.height)
        bottom_left = (top_left[0], top_left[1] + self.height)

        # Draw the lines
        pygame.draw.line(self.surface, self.margin_color,
                         top_left, top_right, self.margin_width)
        pygame.draw.line(self.surface, self.margin_color,
                         top_right, bottom_right, self.margin_width)
        pygame.draw.line(self.surface, self.margin_color,
                         bottom_right, bottom_left, self.margin_width)
        pygame.draw.line(self.surface, self.margin_color,
                         bottom_left, top_left, self.margin_width)

# Subclass
class WildSymbol(SlotSymbol):
    def __eq__(self, other):
        if isinstance(other, WildSymbol):
            # Wild symbols don't match between themselves
            return self.sym_id == other.sym_id

        elif isinstance(other, SlotSymbol):
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
                    wild_val=5, default_val=8,
                    max_val=30, big_vals=3):
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
    # TODO: Support for multiple wilds
    imgs = []
    wilds = []
    # Create symbol objects
    for img in range(len(img_files)):
        # I dont know why pycharm expects an int
        if "wild" in img_files[img]:
            # The wild symbol will be done after
            wilds.append(img_files[img])
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

    # Load all images
    # This is done so that they dont have to be loaded
    # for every copy
    for img in imgs:
        img.load_image()

    # Duplicate items in list to make them more common than the wild
    imgs += imgs

    # Add the wild symbol with a special id
    for wild in range(len(wilds)):
        imgs.append(WildSymbol(screen, -wild - 1, path.join(*directory, wilds[wild]),
                               value=wild_val, size=symbol_size))
        imgs[-1].load_image()

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
    horizontal_bar.y = screen_height - horizontal_width + 2
    vertical_bar.x = screen_width - vertical_width + 2

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
def horizontal_line(columns):
    """
    Generate the coordinates for a horizontal
    :param columns: Amount of columns to generate for
    ------
    :return: List
    """
    # Points along the x axis
    line = [(x, 0) for x in range(columns)]
    return line


def triangle_line(columns):
    """
    Generate the coordinates for a line that goes up and then down
    Odd:
     /\
    /  \

    Even:
     /¯\
    /   \

    :param columns: Amount of columns to generate for
    :return: List
    """
    line = []
    # Create the first half of the triangle, up to the peak
    # Same value is used to make the coords go both up 1 by 1

    # Even lists have 2 peaks so they are handled differently
    # Subtracts 1 from columns if its even. This way the num is
    # always odd. Even nums get their second peak added after the loop
    for i in range(((columns - int(not columns % 2)) // 2) + 1):
        line.append((i, i))

    # Create a second peak if columns is even
    if not columns % 2:
        peak = line[-1]

        # Increase the peak's x by one
        line.append((peak[0] + 1, peak[1]))

    # How many numbers are missing. i.e. The points thatll go down
    rest = columns - len(line)

    # This is to make x values continue from where they left off
    start = len(line)

    downwards_portion = []
    for x in range(rest):
        # Get the y value of the point at the opposite side of the peak
        # I'm not exactly sure why you have to also substract by one
        # but that makes it work
        downwards_portion.append((start + x, line[rest - x - 1][1]))

    # Put them together
    line += downwards_portion

    return line


def dip_line(columns):
    """
    Generate the coordinates for a dip line
    \\____/
    :param columns: Amount of columns to generate for
    :return: List
    """
    # Starting value, raised by 1
    line = [(0, 1)]

    # Generate dip values
    if columns == 1:
        return line

    elif columns > 2:
        # Starting at the second val and ending at the penultimate val
        for x in range(1, columns - 1):
            line.append((x, 0))

    # The ending value, also raised by one
    line.append((columns - 1, 1))

    return line


def saw_line(columns):
    """
    Coordinates for a saw-like line
    /\\/\
    :param columns: Amount of columns to generate for
    :return: List
    """
    line = []

    # Even nums have a y of 0 while odd nums have a y of 1
    # This is way smaller than what i had planned im so proud of it
    # this could even be 1 line compared to the 30ish i had planned
    for x in range(columns):
        line.append((x, x % 2))

    return line


def middle_peak_line(columns):
    """
    Coordinates for a middle peak line, if columns is even, it has 2
    peaks.
    Odd: ___/\\___
    Even: ___/¯\\___
    :param columns: Amount of columns to generate for
    :return: List
    """
    # NOTE: Floor divide by two gets the index of the middle element
    # in odd lists or the index of the element to the right of the
    # middle in even lists.
    #
    # Odd demo:
    # len(ls) == 5
    # 5 // 2 == 2
    # Indexes: 0 1 2 3 4
    #              ^ Middle
    #
    # Even demo
    # len(ls) == 6
    # 6 // 2 == 3
    # Indexes: 0 1 2 3 4 5
    #                ^ Right of middle

    # Get the index of the midpoint
    # This is a list in case theres more than one midpoint.
    mid = [columns // 2]

    # If the # of columns is even, also get the index to the left of
    # the middle
    if not columns % 2:
        mid.append(mid[0] - 1)

    # Make coords at the middle 1 y higher
    line = []
    for x in range(columns):
        line.append(
            (x, 1) if x in mid else (x, 0)
        )

    return line
# --


def flip_line(line):
    """
    Flips a line generated by the line funcs

    :param line: List of (x, y) coords
    :return: List of (x, y coords)
    """
    # Get the highest y value
    max_y = max([point[1] for point in line])

    # Flip along the x axis and then add the biggest y value
    # so it occupies the same space
    flipped_line = [(point[0], point[1] * -1 + max_y) for point in line]

    return flipped_line


def all_horizontal_lines(rows, columns):
    """
    Generate all horizonal lines
    """
    horizontal = horizontal_line(columns)

    # Create one for each row
    all_horizontal = []
    for y in range(rows):
        # Create the same pattern at different y levels
        all_horizontal.append(shift_points(horizontal, (0, y)))

    # This has to be a list for compatibility with the others, sorry
    # my brain is getting fried
    return [all_horizontal]


def all_triangle_lines(rows, columns):
    """
    Generate all possible triangle lines
    """
    triangle = triangle_line(columns)
    flip_triangle = flip_line(triangle)

    # Triangles cover a large area, to get the amount of shifts needed:
    # Rows - highest point
    shifts = rows - triangle[len(triangle) // 2][1]

    all_triangle = []
    all_flip_triangle = []

    # Shift the triangles up
    for y in range(shifts):
        all_triangle.append(shift_points(triangle, (0, y)))
        all_flip_triangle.append(shift_points(flip_triangle, (0, y)))

    return all_triangle, all_flip_triangle


def all_dip_lines(rows, columns):
    """
    Generate all possible dip lines
    """
    dip = dip_line(columns)
    flip_dip = flip_line(dip)  # Hehe

    # The dip at first occupies two rows, so it needs to be shifted
    # one less time to fill up the rows
    all_dips = []
    all_flip_dips = []
    for y in range(rows - 1):
        all_dips.append(shift_points(dip, (0, y)))
        all_flip_dips.append(shift_points(flip_dip, (0, y)))

    return all_dips, all_flip_dips


def all_saw_lines(rows, columns):
    """
    Generate all possible saw lines
    """
    saw = saw_line(columns)
    flip_saw = flip_line(saw)

    # Only need to shift em up by one less
    all_saws = []
    all_flip_saws = []
    for y in range(rows - 1):
        all_saws.append(shift_points(saw, (0, y)))
        all_flip_saws.append(shift_points(flip_saw, (0, y)))

    return all_saws, all_flip_saws


def all_middle_peak_lines(rows, columns):
    middle_peak = middle_peak_line(columns)
    flip_middle_peak = flip_line(middle_peak)

    # Also one less shift
    all_middle_peak = []
    all_flip_middle_peak = []
    for y in range(rows - 1):
        all_middle_peak.append(shift_points(middle_peak, (0, y)))
        all_flip_middle_peak.append(shift_points(flip_middle_peak, (0, y)))

    return all_middle_peak, all_flip_middle_peak


def generate_lines(rows, columns):
    """
    Returns a 3D list of coordinates of the lines used to calculate
    scores. Works regardless of the # of columns or rows
    """
    # There are multiple lines, each is generated by its respective function
    # They then are shifted as many times as needed to fill the screen
    # Turn these into lists for the sake of consistency
    # TODO: turn everything into tuples instead

    # 4 -- horizontals
    all_horizontal = list(all_horizontal_lines(rows, columns))

    # 8 -- triangle
    all_triangle = list(all_triangle_lines(rows, columns))

    # 14 -- dip
    all_dip = list(all_dip_lines(rows, columns))

    # 20 -- saw
    all_saw = list(all_saw_lines(rows, columns))

    # 26 -- middle peak
    all_middle_peak = list(all_middle_peak_lines(rows, columns))

    return all_horizontal, all_triangle, all_dip, all_saw, all_middle_peak


def flip_2d(ls):
    """
    Turn a 2d list the other way
    [[a, b],
     [c, d]]
    to
    [[a, c],
     [b, d]]
    """
    # Create a new list for each one in the provided ls
    new_ls = [list() for _ in ls]

    # Get the lenght of the largest sub list
    biggest = max([len(sub_ls) for sub_ls in ls])

    # Adds the item index from each sub list into the relevant sublist
    # of the new list
    for item in range(biggest):
        for sub_list in range(len(ls)):
            try:
                new_ls[item].append(ls[sub_list][item])

            except IndexError:
                # in case the item doesnt exist
                new_ls[item].append(None)

    return new_ls


def get_values(ls, positions):
    """
    Return values from a 2d list as determined by the position provided
    :param positions: A list of (x, y)
    :param ls: A 2D list
    """
    new_ls = []

    for pos in positions:
        new_ls.append(ls[pos[1]][pos[0]])

    return new_ls


def symbols_equal(ls):
    """
    Check how many items are equal from the start of a list
    :param ls: A list
    :return:
    """
    first = None
    # Obtain the item to compare to, cant be a wild symbol
    for symbol in ls:
        if not isinstance(symbol, WildSymbol):
            first = symbol
            break

    # Idk if this will happen but here it is just in case
    if first is None:
        first = ls[0]

    equal = 0
    # Count how many items are continuously equal
    for symbol in ls:
        if symbol == first:
            equal += 1

        else:
            break
    # return the list up to counter
    return ls[:equal]


def calculate_value(slots, multiplier=1):
    """
    Calculates the total value of the slots given
    """
    return sum([slot.value for slot in slots]) * multiplier


def calculate_score_logic(symbols):
    """
    The logic used to calculate scores
    :param symbols:
    :return:
    """
    # Get the equals
    equal_slots = symbols_equal(symbols)

    # 3 is the minimum amount of consecutive symbols
    score = 0
    if len(equal_slots) >= 3:
        score = calculate_value(equal_slots)

    return score, symbols[:len(equal_slots)]


def calculate_score(slots, lines):
    """
    Calculate the score of the given slots according to the lines
    """
    total_score = 0
    symbols_to_draw = []
    # Horizontal, peak, etc.
    for line_type in lines:

        # Normal or flipped
        for status in line_type:

            # The row in which the line is
            for row in status:
                symbols = get_values(slots, row)

                score, equal_slots = calculate_score_logic(symbols)

                if score > 0:
                    symbols_to_draw.append(equal_slots)

                total_score += score

    return total_score, symbols_to_draw


def main():
    # Cost per lines
    costs = {
        1: 4,
        2: 8,
        3: 14,
        4: 20,
        5: 26
    }

    # Pygame set up
    pygame.init()

    size = width, height = screen_size()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # NOTE: Worth moving into functions or class?
    ROWS = 4
    COLUMNS = 5
    SYMBOL_SIZE = (100, 100)  # px
    SYMBOL_OFFSET = 10  # px

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
    # Yes, a ~5D list. Too bad!
    lines = generate_lines(ROWS, COLUMNS)

    # 0 < selected_lines <= len(lines)
    selected_lines = len(lines)

    # Starting score
    total_score = 100
    score = 0

    # Game status thingies
    # TODO: Find a more efficient way of doing this
    status = 0
    # 0. Nothing
    # 1. rolling
    # 2. calculating score
    # 3. Set slot margins

    # For checking passed time
    time = 0

    # slots for which the margin will be drawn
    slots_to_draw = []

    # The index for slots_to_draw so they are drawn one at a time
    slot_line_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # Only check for keys when a key has been pressed down
            # and when nothing else is happening
            elif event.type == pygame.KEYDOWN and status == 0:
                if event.key == pygame.K_SPACE:
                    # Reduce score
                    if total_score >= costs[selected_lines]:
                        total_score -= costs[selected_lines]
                        print(total_score)

                    # Generate more symbols to add on top of the
                    # Current ones
                    new_rolls = generate_roll(symbols, COLUMNS,
                                              extra_rows)

                    rolls = update_slots(rolls, new_rolls)

                    # Put them into position
                    position_slots(rolls, ROWS, SYMBOL_SIZE,
                                   offset=SYMBOL_OFFSET)

                    # Set status to rolling
                    status = 1

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

        if status == 1:
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
                position_slots(rolls, ROWS, SYMBOL_SIZE, SYMBOL_OFFSET)

                # Update the current status
                status = 2

        # Calculate score
        elif status == 2:
            visible_slots = flip_2d(rolls)
            score, slots_to_draw = calculate_score(visible_slots, lines[:selected_lines])
            status = 3

        # Draw the margins
        elif status == 3:
            time += 1

            if slot_line_index >= len(slots_to_draw):
                # After all of them are done then go back to normal

                # Hide the margins of the last line
                if len(slots_to_draw) != 0:
                    for symbol in slots_to_draw[-1]:
                        symbol.set_margin(False)

                # Reset values
                slot_line_index = 0
                status = 0
                time = 0

                total_score += score

                print(total_score)

            # 60 = 1s
            # 90 = 1.5s
            elif time <= 90:
                # Hide the margins of the previous line
                if slot_line_index != 0:
                    for symbol in slots_to_draw[slot_line_index - 1]:
                        symbol.set_margin(False)

                for symbol in slots_to_draw[slot_line_index]:
                    symbol.set_margin(True)

            else:
                # Increase to the next line
                slot_line_index += 1
                time = 0



        # Draw the symbols
        for column in rolls:
            for symbol in column:
                symbol.draw()

        # Cover up slots
        draw_margins(screen, Color.white, *whitespace)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
