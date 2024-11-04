from yta_multimedia.video.position import Position


class ManimPosition:
    """
    Class to encapsulate and simplify the way we work with manim
    scene positions.
    """
    @staticmethod
    def get_position(position: Position):
        """
        Returns the x,y,z coord to place a mobject in the provided
        'position'.
        """
        position = position.to_enum(position)

        return position.get_manim_position(position)