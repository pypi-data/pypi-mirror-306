from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from yta_multimedia.video.generation.manim.utils.dimensions import width_to_manim_width, height_to_manim_height
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.random import randrangefloat
from random import random, choice as randchoice


class ManimScreenPosition(Enum):
    """
    Enum class that represents a position inside the screen
    scene. This can be used to position a video in one of
    these different regions.
    """
    OUT_TOP_LEFT = 'out_top_left'
    """
    Out of the screen, on the top left corner, just one pixel
    out of bounds.
    """
    IN_EDGE_TOP_LEFT = 'in_edge_top_left'
    """
    The center of the video is on the top left corner, so only
    the bottom right quarter part of the video is shown (inside
    the screen).
    """
    TOP_LEFT = 'top_left'
    """
    The video is completely visible, just at the top left 
    corner of the screen.
    """
    OUT_TOP = 'out_top'
    IN_EDGE_TOP = 'in_edge_top'
    TOP = 'top'
    OUT_TOP_RIGHT = 'out_top_right'
    IN_EDGE_TOP_RIGHT = 'in_edge_top_right'
    TOP_RIGHT = 'top_right'
    CENTER = 'center'
    OUT_RIGHT = 'out_right'
    IN_EDGE_RIGHT = 'in_edge_right'
    RIGHT = 'right'
    OUT_BOTTOM_RIGHT = 'out_bottom_right'
    IN_EDGE_BOTTOM_RIGHT = 'in_edge_bottom_right'
    BOTTOM_RIGHT = 'bottom_right'
    OUT_BOTTOM = 'out_bottom'
    IN_EDGE_BOTTOM = 'in_edge_bottom'
    BOTTOM = 'bottom'
    OUT_BOTTOM_LEFT = 'out_bottom_left'
    IN_EDGE_BOTTOM_LEFT = 'in_edge_bottom_left'
    BOTTOM_LEFT = 'bottom_left'
    OUT_LEFT = 'out_left'
    IN_EDGE_LEFT = 'in_edge_left'
    LEFT = 'left'

    HALF_TOP = 'half_top'
    HALF_TOP_RIGHT = 'half_top_right'
    HALF_RIGHT = 'half_right'
    HALF_BOTTOM_RIGHT = 'half_bottom_right'
    HALF_BOTTOM = 'half_bottom'
    HALF_BOTTOM_LEFT = 'half_bottom_left'
    HALF_LEFT = 'half_left'
    HALF_TOP_LEFT = 'half_top_left'

    QUADRANT_1_TOP_RIGHT_CORNER = 'quadrant_1_top_right_corner'
    QUADRANT_1_BOTTOM_RIGHT_CORNER = 'quadrant_1_bottom_right_corner'
    QUADRANT_1_BOTTOM_LEFT_CORNER = 'quadrant_1_bottom_left_corner'
    QUADRANT_2_TOP_LEFT_CORNER = 'quadrant_2_top_left_corner'
    QUADRANT_2_BOTTOM_RIGHT_CORNER = 'quadrant_2_bottom_right_corner'
    QUADRANT_2_BOTTOM_LEFT_CORNER = 'quadrant_2_bottom_left_corner'
    QUADRANT_3_TOP_RIGHT_CORNER = 'quadrant_3_top_right_corner'
    QUADRANT_3_TOP_LEFT_CORNER = 'quadrant_3_top_left_corner'
    QUADRANT_3_BOTTOM_LEFT_CORNER = 'quadrant_3_bottom_left_corner'
    QUADRANT_4_TOP_RIGHT_CORNER = 'quadrant_4_top_right_corner'
    QUADRANT_4_TOP_LEFT_CORNER = 'quadrant_4_top_left_corner'
    QUADRANT_4_BOTTOM_RIGHT_CORNER = 'quadrant_4_bottom_right_corner'

    RANDOM_INSIDE = 'random_inside'
    """
    A random position inside the screen with no pixels out of bounds.
    It is randomly chosen from one of all the options inside the limits
    we have.
    """
    RANDOM_OUTSIDE = 'random_outside'
    """
    A random position out of the screen limits. It is randomly chosen 
    from one of all the options outside the limits we have.
    """
    # TODO: Add more positions

    @classmethod
    def out_positions_as_list(cls):
        """
        Returns the ManimScreenPosition enums that are located out of
        the screen limits.
        """
        return [
            cls.OUT_TOP_LEFT,
            cls.OUT_TOP,
            cls.OUT_RIGHT,
            cls.OUT_BOTTOM_RIGHT,
            cls.OUT_BOTTOM,
            cls.OUT_BOTTOM_LEFT,
            cls.OUT_LEFT
        ]
    
    @classmethod
    def in_positions_as_list(cls):
        """
        Returns the ManimScreenPosition enums that are located inside
        the screen limits.
        """
        return list(set(cls.get_all()) - set(cls.out_positions_as_list()) - set([cls.RANDOM_INSIDE]) - set([cls.RANDOM_OUTSIDE]))

    def get_limits(self):
        """
        Return the left, right, top and bottom limits for this
        screen position. This edges represent the limits of the
        region in which the video should be placed to fit this
        screen position.

        We consider each screen region as a limited region of
        half of the scene width and height.

        Corner limits:
        [-7-1/9,  4, 0]   [0,  4, 0]   [7+1/9,  4, 0]
        [-7-1/9,  0, 0]   [0,  0, 0]   [7+1/9,  0, 0]
        [-7-1/9, -4, 0]   [0, -4, 0]   [7+1/9, -4, 0]
        """
        # TODO: I think I should consider regions of 1/8 of width and height
        # so 1 quadrant is divided into 4 pieces and I build all the positions
        # for also those quadrants
        # TODO: I'm missing the QUADRANT_1_HALF_TOP and HALF_TOP_OUT, ...
        if self == ManimScreenPosition.TOP:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.BOTTOM:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.LEFT:
            return -HALF_SCENE_WIDTH, 0, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        elif self == ManimScreenPosition.RIGHT:
            return 0, HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        # TODO: Add missing

    def get_position(self, width: float, height: float):
        """
        Return the position in which the mobject must be placed to
        be exactly in this position.
        """
        # TODO: 'width' and 'height' must be manim

        if self == ManimScreenPosition.TOP:
            return 0, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.TOP_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.RIGHT:
            return HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == ManimScreenPosition.BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.BOTTOM:
            return 0, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.LEFT:
            return -HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == ManimScreenPosition.TOP_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.CENTER:
            return 0, 0, 0
        elif self == ManimScreenPosition.IN_EDGE_TOP_LEFT:
            return -HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_TOP_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_TOP:
            return 0, HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_TOP:
            return 0, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_TOP_RIGHT:
            return HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_TOP_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_RIGHT:
            return HALF_SCENE_WIDTH, 0, 0
        elif self == ManimScreenPosition.OUT_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == ManimScreenPosition.IN_EDGE_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == ManimScreenPosition.OUT_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.IN_EDGE_LEFT:
            return -HALF_SCENE_WIDTH, 0, 0
        elif self == ManimScreenPosition.OUT_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == ManimScreenPosition.HALF_TOP:
            return 0, HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.HALF_TOP_RIGHT:
            return HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.HALF_RIGHT:
            return HALF_SCENE_WIDTH / 2, 0, 0
        elif self == ManimScreenPosition.HALF_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.HALF_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.HALF_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.HALF_LEFT:
            return -HALF_SCENE_WIDTH / 2, 0, 0
        elif self == ManimScreenPosition.HALF_TOP_LEFT:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == ManimScreenPosition.QUADRANT_1_TOP_RIGHT_CORNER:
            return -width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            return -width / 2, height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_1_BOTTOM_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_2_TOP_LEFT_CORNER:
            return width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_2_BOTTOM_LEFT_CORNER:
            return width / 2, height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_3_TOP_LEFT_CORNER:
            return width / 2, -height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_3_TOP_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, -height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_3_BOTTOM_LEFT_CORNER:
            return width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_4_TOP_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, -height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_4_TOP_RIGHT_CORNER:
            return -width / 2, -height / 2, 0
        elif self == ManimScreenPosition.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            return -width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == ManimScreenPosition.RANDOM_INSIDE:
            return randchoice(ManimScreenPosition.in_positions_as_list()).get_position(width, height)
        elif self == ManimScreenPosition.RANDOM_OUTSIDE:
            return randchoice(ManimScreenPosition.out_positions_as_list()).get_position(width, height)
        
    def get_random_position(self, width: float, height: float):
        """
        Calculate the position in which the center of the element 
        with the provided 'width' and 'height' must be placed to
        obtain this position.

        The position will be provided as a 3D vector but the z
        axis will be always 0.

        The provided 'width' and 'height' must be in pixels.
        """
        # TODO: Check if the provided 'width' and 'height' are in
        # in pixels and valid or if not

        # TODO: By now I'm just using the limits as numeric limits
        # for random position that will be used as the center of the
        # video, but we will need to consider the video dimensions 
        # in a near future to actually position it well, because the
        # video can be out of the scene right now with this approach
        left, right, top, bottom = self.get_limits()

        x, y = randrangefloat(left, right, width_to_manim_width(1)), randrangefloat(top, bottom, height_to_manim_height(1))

        # If video is larger than HALF/2 it won't fit correctly.
        if width > HALF_SCENE_WIDTH or height > HALF_SCENE_HEIGHT:
            # TODO: Video is bigger than the region, we cannot make
            # it fit so... what can we do (?)
            return x, y

        if x - width / 2 < left:
            x += left - (x - width / 2)
        if x + width / 2 > right:
            x -= (x + width / 2) - right
        if y - height / 2 < bottom:
            y += bottom - (y - height / 2)
        if y + height / 2 > top:
            y -= (y + height / 2) - top

        return x, y, 0
        

class ManimPosition:
    @staticmethod
    def min_and_max_x(width: float):
        """
        Calculates the minimum and maximum possible 'x' to make the 
        object with the provided 'width' fit the manim screen, that
        means to be inside of it and appear in the video.

        The provided 'width' must be a manim width, not a width in
        pixels.

        This method returns the 'min, max' pair of minimum and
        maximum possible x values.
        """
        return -HALF_SCENE_WIDTH + (width / 2), HALF_SCENE_WIDTH - (width / 2)
    
    @staticmethod
    def min_and_max_y(height: float):
        """
        Calculates the minimum and maximum possible 'y' to make the
        object with the provided 'height' fit the manim screen, that
        means to be inside of it and appear in the video.

        The provided 'height' must be a manim height, not a height
        in pixels.

        This method returns the 'min, max' pair of minimum and
        maximum possible y values.
        """
        return -HALF_SCENE_HEIGHT + (height / 2), HALF_SCENE_HEIGHT - (height / 2)

    @classmethod
    def random_position(width: float, height: float):
        """
        Calculate a random position inside the manim screen limits according
        to the provided 'width' and 'height' that must be 

        Provided 'width' and 'height' must be in manim width and height.

        Calculate a random position inside the manim screen limits according
        to the provided 'width' and 'height' that must be of the element to
        position.
        """
        x_min, x_max = ManimPosition.min_and_max_x(width)
        random_x = x_min + (random() * (x_max - x_min))

        y_min, y_max = ManimPosition.min_and_max_y(height)
        random_y = y_min + (random() * (y_max - y_min))
        
        # TODO: Maybe in this class is as easy as return just 'x, y'
        return random_x, random_y

# TODO: Remove this below when refactored and unneeded
def get_random_position(width: float, height: float):
    """
    Returns a random position inside the screen according to the provided element width and
    height to fit in. If you are trying to position a text inside screen limits, you must
    provide text width and height to let this method calculate that random position.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_upper_left_position(width: float, height: float):
    """
    Returns a random position in the upper left corner according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = -(width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_upper_right_position(width: float, height: float):
    """
    Returns a random position in the upper right corner according to the 
    provided element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_upper_center_position(width: float, height: float):
    """
    Returns a random position in the upper center according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH / 2 + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH / 2 - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_upper_position(width: float, height: float):
    """
    Returns a random position in the upper section according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_center_position(width: float, height: float):
    """
    Returns a random position in the center according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH / 2 + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH / 2 - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT / 2 + (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT / 2 - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_center_left_position(width: float, height: float):
    """
    Returns a random position in the center left according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = -(width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT / 2 + (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT / 2 - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_center_right_position(width: float, height: float):
    """
    Returns a random position in the center right according to the 
    provided element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT / 2 + (height / 2)
    Y_MAXIMUM = HALF_SCENE_HEIGHT / 2 - (height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_lower_left_position(width: float, height: float):
    """
    Returns a random position in the lower left corner according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = -(width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = -(height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_lower_right_position(width: float, height: float):
    """
    Returns a random position in the lower right corner according to the 
    provided element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = -(height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_lower_center_position(width: float, height: float):
    """
    Returns a random position in the lower center according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH / 2 + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH / 2 - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = -(height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

def get_random_lower_position(width: float, height: float):
    """
    Returns a random position in the upper section according to the provided
    element 'width' and 'height' to fit in.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X_MINIMUM = -HALF_SCENE_WIDTH + (width / 2)
    X_MAXIMUM = HALF_SCENE_WIDTH - (width / 2)
    random_x = X_MINIMUM + (random() * (X_MAXIMUM - X_MINIMUM))
    Y_MINIMUM = -HALF_SCENE_HEIGHT + (height / 2)
    Y_MAXIMUM = -(height / 2)
    random_y = Y_MINIMUM + (random() * (Y_MAXIMUM - Y_MINIMUM))

    return {
        'x': random_x,
        'y': random_y
    }

# Exact places
HEIGHT_DISTANCE_FROM_EDGES = height_to_manim_height(10)
WIDTH_DISTANCE_FROM_EDGES = width_to_manim_width(10)
def get_upper_left_position(width: float, height: float):
    """
    Returns the exact position of the upper left corner according to
    the provided element 'width' and 'height' to fit in and be placed
    just in the corner.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = -HALF_SCENE_WIDTH + WIDTH_DISTANCE_FROM_EDGES + (width / 2)
    Y = HALF_SCENE_HEIGHT - HEIGHT_DISTANCE_FROM_EDGES - (height / 2)

    return {
        'x': X,
        'y': Y
    }

def get_upper_right_position(width: float, height: float):
    """
    Returns the exact position of the upper right corner according to
    the provided element 'width' and 'height' to fit in and be placed
    just in the corner.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = HALF_SCENE_WIDTH - WIDTH_DISTANCE_FROM_EDGES - (width / 2)
    Y = HALF_SCENE_HEIGHT - HEIGHT_DISTANCE_FROM_EDGES - (height / 2)

    return {
        'x': X,
        'y': Y
    }

def get_upper_center_position(height: float):
    """
    Returns the exact position of the upper center position according 
    to the provided element 'width' and 'height' to fit in and be 
    placed just there.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = 0
    Y = HALF_SCENE_HEIGHT - HEIGHT_DISTANCE_FROM_EDGES - (height / 2)

    return {
        'x': X,
        'y': Y
    }

def get_left_position(width: float):
    """
    Returns the exact position of the left side according to
    the provided element 'width' and 'height' to fit in and be placed
    just in that place

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = -HALF_SCENE_WIDTH + WIDTH_DISTANCE_FROM_EDGES + (width / 2)
    Y = 0

    return {
        'x': X,
        'y': Y
    }

def get_center_position():
    """
    Returns the exact position of the center according to the 
    provided element 'width' and 'height' to fit in and be placed
    just in that place

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = 0
    Y = 0

    return {
        'x': X,
        'y': Y
    }

def get_right_position(width: float):
    """
    Returns the exact position of the right side according to
    the provided element 'width' and 'height' to fit in and be placed
    just in that place

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = HALF_SCENE_WIDTH - WIDTH_DISTANCE_FROM_EDGES - (width / 2)
    Y = 0

    return {
        'x': X,
        'y': Y
    }

def get_lower_left_position(width: float, height: float):
    """
    Returns the exact position of the lower left corner according to
    the provided element 'width' and 'height' to fit in and be placed
    just in the corner.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = -HALF_SCENE_WIDTH + WIDTH_DISTANCE_FROM_EDGES + (width / 2)
    Y = -HALF_SCENE_HEIGHT + HEIGHT_DISTANCE_FROM_EDGES + (height / 2)

    return {
        'x': X,
        'y': Y
    }

def get_lower_right_position(width: float, height: float):
    """
    Returns the exact position of the lower right corner according to
    the provided element 'width' and 'height' to fit in and be placed
    just in the corner.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = HALF_SCENE_WIDTH - WIDTH_DISTANCE_FROM_EDGES - (width / 2)
    Y = -HALF_SCENE_HEIGHT + HEIGHT_DISTANCE_FROM_EDGES + (height / 2)

    return {
        'x': X,
        'y': Y
    }

def get_lower_center_position(height: float):
    """
    Returns the exact position of the lower center position according 
    to the provided element 'width' and 'height' to fit in and be 
    placed just there.

    Provided 'width' and 'height' must be in manim width and height.

    This method returns an object containing 'x' and 'y' random fitting
    coordinates.
    """
    X = 0
    Y = -HALF_SCENE_HEIGHT + HEIGHT_DISTANCE_FROM_EDGES + (height / 2)

    return {
        'x': X,
        'y': Y
    }