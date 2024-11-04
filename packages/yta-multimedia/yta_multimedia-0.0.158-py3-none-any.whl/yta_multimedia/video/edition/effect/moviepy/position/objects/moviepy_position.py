from yta_multimedia.video.position import Position


class MoviepyPosition:
    @staticmethod
    def get_position(position: Position, video, background_video):
        position = position.to_enum(position)
        # TODO: Check that video and background_video are moviepy videos (?)

        return position.get_moviepy_position(video, background_video)