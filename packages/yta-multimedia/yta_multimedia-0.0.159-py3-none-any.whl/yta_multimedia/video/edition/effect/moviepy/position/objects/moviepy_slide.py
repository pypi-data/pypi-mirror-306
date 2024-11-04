from yta_multimedia.video.edition.effect.moviepy.position import MoviepyPosition
from random import randrange


class MoviepySlide:
    @staticmethod
    def get_in_and_out_positions_as_list():
        """
        Returns a list of 2 elements containing the out edge from which
        the video will come into the screen, and the opposite edge to get
        out of the screen. This has been created to animate a random slide
        transition effect. The possibilities are horizontal, diagonal and
        vertical linear sliding transitions. The first element in the list
        is the initial position and the second one, the final position. 
        """
        rnd = randrange(0, 8)
        
        if rnd == 0:
            positions = [MoviepyPosition.OUT_RIGHT, MoviepyPosition.OUT_LEFT]
        elif rnd == 1:
            positions = [MoviepyPosition.OUT_TOP, MoviepyPosition.OUT_BOTTOM]
        elif rnd == 2:
            positions = [MoviepyPosition.OUT_BOTTOM, MoviepyPosition.OUT_TOP]
        elif rnd == 3:
            positions = [MoviepyPosition.OUT_TOP_LEFT, MoviepyPosition.OUT_BOTTOM_RIGHT] 
        elif rnd == 4:
            positions = [MoviepyPosition.OUT_TOP_RIGHT, MoviepyPosition.OUT_BOTTOM_LEFT]
        elif rnd == 5:
            positions = [MoviepyPosition.OUT_BOTTOM_LEFT, MoviepyPosition.OUT_TOP_RIGHT]
        elif rnd == 6:
            positions = [MoviepyPosition.OUT_BOTTOM_RIGHT, MoviepyPosition.OUT_TOP_LEFT]
        elif rnd == 7:
            positions = [MoviepyPosition.OUT_LEFT, MoviepyPosition.OUT_RIGHT]

        return positions