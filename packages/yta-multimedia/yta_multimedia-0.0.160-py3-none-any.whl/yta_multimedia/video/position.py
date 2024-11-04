from yta_general_utils.programming.enum import YTAEnum as Enum


class Position(Enum):
    """
    Enum class that represents a position inside the screen
    scene. This is used to position a video or an image inside
    the scene in an specific position defined by itself. It is
    useful with Manim and Moviepy video positioning and has
    been prepared to work with those engines.
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
    # TODO: Add more positions maybe (?)

    @classmethod
    def outside_positions_as_list(cls):
        """
        Returns the Position enums that are located out of
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
    def inside_positions_as_list(cls):
        """
        Returns the Position enums that are located inside
        the screen limits.
        """
        return list(set(cls.get_all()) - set(cls.outside_positions_as_list()) - set([cls.RANDOM_INSIDE]) - set([cls.RANDOM_OUTSIDE]))