from yta_multimedia.video.edition.effect.moviepy.position import get_center
from yta_multimedia.video.position import Position
from random import choice as randchoice


class MoviepyPosition(Position):
    """
    Enum class to encapsulate and simplify the way we work with
    positions in the moviepy video scene system.
    """
    def get_moviepy_position(self, video, background_video):
        """
        This method will calculate the (x, y) tuple position for the provided
        'video' over the also provided 'background_video' that would be,
        hypothetically, a 1920x1080 black color background static image. The
        provided 'position' will be transformed into the (x, y) tuple according
        to our own definitions.
        """
        # TODO: Do 'video' and 'background_video' checkings
        position_tuple = None

        if self == Position.CENTER:
            position_tuple = (get_center(video, background_video))

        #           Edges below
        # TOP
        elif self == Position.OUT_TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), -video.h)
        elif self == Position.IN_EDGE_TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), -(video.h / 2))
        elif self == Position.TOP:
            position_tuple = ((background_video.w / 2) - (video.w / 2), 0)
        # TOP RIGHT
        elif self == Position.OUT_TOP_RIGHT:
            position_tuple = (background_video.w, -video.h)
        elif self == Position.IN_EDGE_TOP_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), -(video.h / 2))
        elif self == Position.TOP_RIGHT:
            position_tuple = (background_video.w - video.w, 0)
        # RIGHT
        elif self == Position.OUT_RIGHT:
            position_tuple = (background_video.w, (background_video.h / 2) - (video.h / 2))
        elif self == Position.IN_EDGE_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), (background_video.h / 2) - (video.h / 2))
        elif self == Position.RIGHT:
            position_tuple = (background_video.w - video.w, (background_video.h / 2) - (video.h / 2))
        # BOTTOM RIGHT
        elif self == Position.OUT_BOTTOM_RIGHT:
            position_tuple = (background_video.w, background_video.h)
        elif self == Position.IN_EDGE_BOTTOM_RIGHT:
            position_tuple = (background_video.w - (video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM_RIGHT:
            position_tuple = (background_video.w - video.w, background_video.h - video.h)
        # BOTTOM
        elif self == Position.OUT_BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h)
        elif self == Position.IN_EDGE_BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM:
            position_tuple = ((background_video.w / 2) - (video.w / 2), background_video.h - video.h)
        # BOTTOM LEFT
        elif self == Position.OUT_BOTTOM_LEFT:
            position_tuple = (-video.w, background_video.h)
        elif self == Position.IN_EDGE_BOTTOM_LEFT:
            position_tuple = (-(video.w / 2), background_video.h - (video.h / 2))
        elif self == Position.BOTTOM_LEFT:
            position_tuple = (0, background_video.h - video.h)
        # LEFT
        elif self == Position.OUT_LEFT:
            position_tuple = (-video.w, (background_video.h / 2) - (video.h / 2))
        elif self == Position.IN_EDGE_LEFT:
            position_tuple = (-(video.w / 2), (background_video.h / 2) - (video.h / 2))
        elif self == Position.LEFT:
            position_tuple = (0, (background_video.h / 2) - (video.h / 2))
        # TOP LEFT
        elif self == Position.OUT_TOP_LEFT:
            position_tuple = (-video.w, -video.h)
        elif self == Position.IN_EDGE_TOP_LEFT:
            position_tuple = (-(video.w / 2), -(video.h / 2))
        elif self == Position.TOP_LEFT:
            position_tuple = (0, 0)

        # HALF POSITIONS
        elif self == Position.HALF_TOP:
            position_tuple = (background_video.w / 2 - video.w / 2, background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
        elif self == Position.HALF_BOTTOM:
            position_tuple = (background_video.w / 2 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 2 - video.h / 2)
        elif self == Position.HALF_TOP_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_BOTTOM_RIGHT:
            position_tuple = (3 * background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_BOTTOM_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, 3 * background_video.h / 4 - video.h / 2)
        elif self == Position.HALF_TOP_LEFT:
            position_tuple = (background_video.w / 4 - video.w / 2, background_video.h / 4 - video.h / 2)

        # QUADRANT CORNERS
        elif self == Position.QUADRANT_1_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, 0)
        elif self == Position.QUADRANT_1_BOTTOM_LEFT_CORNER:
            position_tuple = (0, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_1_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_BOTTOM_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w - video.w, background_video.h / 2 - video.h)
        elif self == Position.QUADRANT_2_TOP_LEFT_CORNER:
            position_tuple = (background_video.w / 2, 0)
        elif self == Position.QUADRANT_3_BOTTOM_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h - video.h)
        elif self == Position.QUADRANT_3_TOP_LEFT_CORNER:
            position_tuple = (background_video.w / 2, background_video.h / 2)
        elif self == Position.QUADRANT_3_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w - video.w, background_video.h / 2)
        elif self == Position.QUADRANT_4_BOTTOM_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h - video.h)
        elif self == Position.QUADRANT_4_TOP_LEFT_CORNER:
            position_tuple = (0, background_video.h / 2)
        elif self == Position.QUADRANT_4_TOP_RIGHT_CORNER:
            position_tuple = (background_video.w / 2 - video.w, background_video.h / 2)

        # RANDOMs
        elif self == Position.RANDOM_INSIDE:
            return randchoice(Position.inside_positions_as_list()).get_moviepy_position(video, background_video)
        elif self == Position.RANDOM_OUTSIDE:
            return randchoice(Position.outside_positions_as_list()).get_moviepy_position(video, background_video)

        return position_tuple

def get_center(video, background_video):
    """
    Returns the x,y coords in which the provided 'video' will
    be centered according to the provided 'background_video' in
    which it will be overlayed.

    This method returns two elements, first one is the x and the
    second one is the y.
    """
    # TODO: Ensure 'video' and 'background_video' are valid videos
    return background_video.w / 2 - video.w / 2, background_video.h / 2 - video.h / 2

# TODO: Import all effects to have them here available (?)