# pp_main.py
"""
Module to encapsulate the post-processing functions for multi_column.
"""

import logging

from pymupdf import IRect, Rect  # type: ignore

from pdf_structr.multicol.pp_clean import clean_column_blocks
from pdf_structr.multicol.pp_join import (
    join_rects_phase1,
    join_rects_phase2,
    join_rects_phase3,
    sort_rects,
)

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
# Main post processing function
#####################


def post_process_column_blocks(
    column_blocks: list[Rect | IRect],
    path_rects: list[IRect],
    join_distant_y_rect: bool,
) -> list[IRect]:
    '''
    Do some postprocessing (reordering, joining contiguous blocks, etc.)
    on the built-up column block list.

    :returns: a list of IRect corresponding to the post-processed
        column blocks.

    :param column_blocks: list[IRect]: the identified text column blocks.

    :param path_rects: list[IRect]: the identified vg clusters rectangles.

    :param join_distant_y_rect: bool = True: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    # do some elementary cleaning
    column_blocks = clean_column_blocks(column_blocks)

    # final joining of overlapping rectangles
    column_blocks = join_rects_phase1(column_blocks)
    column_blocks = join_rects_phase2(column_blocks)
    if join_distant_y_rect is True:
        column_blocks = join_rects_phase3(
            column_blocks,
            path_rects,
        )
    else:
        column_blocks.sort(key=lambda _rect: (_rect.y0, _rect.x0))
    column_blocks = sort_rects(column_blocks)

    return column_blocks


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
