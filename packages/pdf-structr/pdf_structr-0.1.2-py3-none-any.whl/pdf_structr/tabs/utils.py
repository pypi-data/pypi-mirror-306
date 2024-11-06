# utils.py
'''
Module to encapsulate usefull functions for other modules.

'''

import logging

import pymupdf  # type: ignore

#####################
# Logging stack
#####################


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
)
logger.info("logger initialized")


def in_clip(
    clip: pymupdf.Rect, bbox: tuple[float, float, float, float]
) -> bool:
    '''
    Returns True if a bbox is in a clip and False otherwise.
    '''
    return (
        False
        if (
            bbox[0] >= clip.x1
            or bbox[2] <= clip.x0
            or bbox[1] >= clip.y1
            or bbox[3] <= clip.y0
        )
        else True
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
