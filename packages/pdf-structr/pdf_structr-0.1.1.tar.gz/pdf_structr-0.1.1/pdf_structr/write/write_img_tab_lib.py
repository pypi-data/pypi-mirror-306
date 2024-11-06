# write_img_tab_lib.py
'''
Encapsulation of functions common to write_image and write_table.
'''


import functools
import logging
from typing import Callable, Literal

from pymupdf import Rect  # type: ignore

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


#####################
# Playground
#####################


def get_relevant_img_or_tab_rects(filtering_func: Callable) -> Callable:
    '''
    Checks whether any image/vg rectangle or table rectangle need to
    processed when it is called. It does so by category: it does not
    check both for the presence of image/vg rectangles and table
    rectangles, but the presence of either image/vg rectangles or
    table rectangles.

    It does so by testing for the presence of any rectangle of the relevant
    type fullfils the conditions passed in the filtering function.

    The wrapped function returns either False or a list of any such rectangles
    if the form of a list of 2-tuples (idx: int - rectangle: Rect).

    :param filtering_func: Callable: the filtering function may be one of:

        - filter_rects_above_text_rect() in `write_lib` module;
        - list(tbl_or_img_rects.items()) making actually no filtering;
        - _filter_rects_above_line_rect_within_clip() in `write_lib` module.
    '''

    @functools.wraps(filtering_func)
    def get_relevant_img_or_tab_rects_wrapper(
        *args,
        **kwargs,
    ) -> list[tuple[int, Rect]] | Literal[False]:
        '''
        See docstring in the decorator.

        Required parameters are:

        :param rect_dict: dict[int, pymupdf.Rect]: Required. An ordered
            dict of img/vg rectangles or table rectangles in the current
            page, sorted by y1 and x0 (the sorting is made at extraction
            time) and where the keys are the index numbers in the table
            finder, when the rect_dicts is a dictionary of table Rectangles
            and or the index numbers at extraction time, when the rect dicts
            is a dictionary of img/vg Rectangles.

        :param text_rect: pymupdf.IRect | pymupdf.Rect | None = None: Optional.
            A text rectangle above which the looked up table rectangles shall
            live.

        :param clip: pymupdf.Rect | Optional: Optional. The zone to parse.
            May be the page clipped off the margins or a text rectangle.
        '''
        # ------------------------------
        # 0. Check if there's anything to be done
        # ------------------------------

        # If there is not any rectangle, just return
        if not kwargs['rect_dict']:
            return False

        # ------------------------------
        # 1. Filter the rectangles to be processed
        # ------------------------------

        # Filter the relevant rectangles out of the table rectangles dict.
        # We get a list containing 2-tuples idx - table rectangle.
        idx_rect_iterable: list[tuple[int, Rect]] = filtering_func(
            *args,
            **kwargs,
        )

        # ------------------------------
        # 2. Return if no table rectangle corresponds
        # ------------------------------

        # If no table filling the filtering_func conditions (ex. above
        # the text_rect, within the clip) have been found, return
        if not idx_rect_iterable:
            return False

        return idx_rect_iterable

    return get_relevant_img_or_tab_rects_wrapper


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
