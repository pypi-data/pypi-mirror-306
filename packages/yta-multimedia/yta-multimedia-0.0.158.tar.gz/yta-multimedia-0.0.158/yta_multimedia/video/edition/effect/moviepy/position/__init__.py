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