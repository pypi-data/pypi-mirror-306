from yta_multimedia.video.position import Position
from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH
from yta_multimedia.video.generation.manim.utils.dimensions import width_to_manim_width, height_to_manim_height
from yta_general_utils.random import randrangefloat
from random import choice as randchoice


class ManimPosition(Position):
    """
    Enum class to encapsulate and simplify the way we work with
    positions in the manim video scene system.
    """
    def get_manim_limits(self):
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
        if self == Position.TOP:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT, 0
        elif self == Position.BOTTOM:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT, 0
        elif self == Position.LEFT:
            return -HALF_SCENE_WIDTH, 0, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        elif self == Position.RIGHT:
            return 0, HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT / 2, -HALF_SCENE_HEIGHT / 2
        # TODO: Add missing

        # TODO: Is this method necessary (?)

    def get_manim_position(self, width: float, height: float):
        """
        Return the position in which the mobject must be placed to
        be exactly in this position.
        """
        # TODO: 'width' and 'height' must be manim

        if self == Position.TOP:
            return 0, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.TOP_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.RIGHT:
            return HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == Position.BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.BOTTOM:
            return 0, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.LEFT:
            return -HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == Position.TOP_LEFT:
            return -HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.CENTER:
            return 0, 0, 0
        elif self == Position.IN_EDGE_TOP_LEFT:
            return -HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_TOP:
            return 0, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP:
            return 0, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_TOP_RIGHT:
            return HALF_SCENE_WIDTH, HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_TOP_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.IN_EDGE_RIGHT:
            return HALF_SCENE_WIDTH, 0, 0
        elif self == Position.OUT_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, 0, 0
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH + width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH, -HALF_SCENE_HEIGHT, 0
        elif self == Position.OUT_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, -HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.IN_EDGE_LEFT:
            return -HALF_SCENE_WIDTH, 0, 0
        elif self == Position.OUT_LEFT:
            return -HALF_SCENE_WIDTH - width / 2, 0, 0
        elif self == Position.HALF_TOP:
            return 0, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_TOP_RIGHT:
            return HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_RIGHT:
            return HALF_SCENE_WIDTH / 2, 0, 0
        elif self == Position.HALF_BOTTOM_RIGHT:
            return HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_BOTTOM:
            return 0, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_BOTTOM_LEFT:
            return -HALF_SCENE_WIDTH / 2, -HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.HALF_LEFT:
            return -HALF_SCENE_WIDTH / 2, 0, 0
        elif self == Position.HALF_TOP_LEFT:
            return -HALF_SCENE_WIDTH / 2, HALF_SCENE_HEIGHT / 2, 0
        elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
            return -width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            return -width / 2, height / 2, 0
        elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, height / 2, 0
        elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
            return width / 2, HALF_SCENE_HEIGHT - height / 2, 0
        elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, height / 2, 0
        elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
            return width / 2, height / 2, 0
        elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
            return width / 2, -height / 2, 0
        elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
            return HALF_SCENE_WIDTH - width / 2, -height / 2, 0
        elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
            return width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
            return -HALF_SCENE_WIDTH + width / 2, -height / 2, 0
        elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
            return -width / 2, -height / 2, 0
        elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            return -width / 2, -HALF_SCENE_HEIGHT + height / 2, 0
        elif self == Position.RANDOM_INSIDE:
            return randchoice(Position.inside_positions_as_list()).get_manim_position(width, height)
        elif self == Position.RANDOM_OUTSIDE:
            return randchoice(Position.outside_positions_as_list()).get_manim_position(width, height)
        
    def get_manim_random_position(self, width: float, height: float):
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
        left, right, top, bottom = self.get_manim_limits()

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
        # TODO: Is this method necessary (?)