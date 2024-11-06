# make_columns.py
'''
Module to store the functions that transform a block's list into
columns.
'''

import functools
import logging
from typing import Callable

from pymupdf import IRect, Rect  # type: ignore

from pdf_structr.multicol.make_cols_lowlev import (
    _can_extend,
    _try_extend_one_of_exist_col_with_horiz_bb,
)
from pdf_structr.multicol.pp_main import (
    post_process_column_blocks,
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
# Playground
#####################


def _extend_existing_col_or_make_new_col(
    horiz_bbox: IRect,
    column_bboxes: list[IRect],
    path_bboxes: list[IRect],
    vert_bboxes: list[IRect],
    join_distant_y_rect: bool,
) -> tuple[IRect, int, bool]:
    '''
    For each passed-in horizontal text block bbox Rectangle,
    checks whether the text block rectangle can be used to
    extend one of the existing columns stored in column_bboxes.

    :returns: a 3-tuple comprising an IRect, an integer and a bool.

    The IRect (_temp_union_col) is:
    - either the union of the column to be extend and the
      current horizontal text rectangle
    - or the current horizontal text rectangle, as stored
      as a new column in the column_bboxes list if it cannot
      be used to extend any existing column.

    The integer (_col_idx) is:
    - either the index number of the existing column that can
      be extend
    - or the the index number of the new column.

    The bool is the result of the first call to can_extend(), checking
    whether _temp_union_col is a validly extended column or whether
    it should be assigned horiz_bbox as a new column.

    :param horiz_bbox: IRect: the passed-in horizontal text block
        bbox to be tested and either used to extend a column's bbox
        or append as a new column bbox to column_bboxes.

    :param column_bboxes: list[IRect]: the list of currently identified
        columns bboxes.

    :param path_bboxes: list[IRect]: the list of paths bboxes on the page.

    :param vert_bboxes: list[IRect]: the list of vertical text blocks
        bboxes on the page.

    :param join_distant_y_rect: bool: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    _check_can_extend, _temp_union_col, _col_idx = (
        _try_extend_one_of_exist_col_with_horiz_bb(
            horiz_bbox=horiz_bbox,
            column_bboxes=column_bboxes,
            path_bboxes=path_bboxes,
            vert_bboxes=vert_bboxes,
            join_distant_y_rect=join_distant_y_rect,
        )
    )

    # At this stage:
    # - if _check_can_extend is True: we have an extended column
    #
    #   _temp_union_col does not collide with any existing column
    #   => _temp_union_col can be used as the extended column
    #
    # - _check_can_extend is False: we have a new column
    #
    #   all the _temp_union_col generated in
    #   _try_extend_one_of_exist_col_with_horiz_bb
    #   did collide with an existing existing column.
    #   The returned _temp_union_col and _col_idx are meaningless and
    #   need to be reset.

    if _check_can_extend is False:
        # _horiz_bbox cannot be used to extend any of the existing
        # column bboxes without overlapping another column.
        # => 1. we've got a new column => the current _horiz_bbox is
        #    the beginning of a new column bbox
        # => 2. _temp_union_col has to be reset to the current _horiz_bbox
        #    make a new column and add it to the list of columns bboxes
        column_bboxes.append(horiz_bbox)
        # get its index (the last column_bbox in column_bboxes)
        _col_idx = len(column_bboxes) - 1
        # new column's bbox added
        # reset _temp_union_col
        _temp_union_col = column_bboxes[_col_idx]

    return _temp_union_col, _col_idx, _check_can_extend


def _make_new_extendable_col_or_confirm_new_or_extd_col(
    extended_col: IRect,
    horiz_bbox: IRect,
    col_idx: int,
    column_bboxes: list[IRect],
    horiz_bboxes: list[IRect],
    vert_bboxes: list[IRect],
) -> None:
    '''
    We want to check whether the new or extend column intersects with any
    other remaining horizontal text bbox Rectangles.

    If it does, we'll make another new column with the horiz_bbox.
    If it does not, we'll confirm this new new_or_extd_col.

    :returns: None. The column_bboxes is modified in place and does not
        need to be returned.

    :param extended_col: IRect: the existing column extended by the
        current horizontal text block bbox.

    :param horiz_bbox: IRect: the passed-in current horizontal text block
        bbox that has been used either to make a new column or to extend
        an existing one.

    :param col_idx: int: the index number under which the extended_col
        is stored in column_bboxes.

    :param column_bboxes: list[IRect]: the list of columns bboxes that
        is being built. Initialized with the first horizontal text block
        bbox Rectangle.

    :param horiz_bboxes: list[IRect]: the list of horizontal text block
        bbox Rectangles.

    :param vert_bboxes: list[IRect]: the list of vertical text block
        bbox Rectangles.
    '''
    # Check if the new or extend column collides with any existing remaining
    # horizontal text block bbox
    _check_can_extend: bool = _can_extend(
        extended_rect=extended_col,
        # _horiz_bbox is the current horizontal text block bbox rectangle
        extending_rect=horiz_bbox,
        excluding_bboxlist=horiz_bboxes,  # <-- !!
        vert_bboxes=vert_bboxes,
    )

    # If the new or extend column DOES collide with any remaining text
    # bbox Rect, horiz_bbox is a new column of its own
    if _check_can_extend is False:
        # create a new column
        column_bboxes.append(horiz_bbox)

    # else if it does NOT, we replace the current column
    # in its index in column_bboxes.
    else:
        column_bboxes[col_idx] = extended_col


def _make_column_bbox(
    block_idx: int,
    column_bboxes: list[IRect],
    horiz_bboxes: list[IRect],
    path_bboxes: list[IRect],
    vert_bboxes: list[IRect],
    join_distant_y_rect: bool,
) -> None:
    '''
    For each passed-in block_idx (an index in the list of horizontal
    text block bboxes), either use it to extend one of the existing columns
    stored in column_bboxes or appends it as a new column to the
    column_bboxes list.

    Once treated, the horiz_bbox is marked as None in the horizontal
    text block bboxes list (horiz_bboxes).

    :returns: None because the modified values are stored as elements in
        column_bboxes and horiz_bboxes which are list (mutable).

    :param block_idx: int: the index number of the horizontal
        text block rectangle which bbox might be used to extend an existing
        column or append to the list of column_bboxes as a new column.
    :param column_bboxes: list[IRect]: the list of columns bboxes that
        is being built. Initialized with the first horizontal text block
        bbox Rectangle.
    :param horiz_bboxes: list[IRect]: the list of horizontal text block
        bbox Rectangles.
    :param path_bboxes: list[IRect]: the list of path block bbox Rectangles.
    :param vert_bboxes: list[IRect]: the list of vertical text block
        bbox Rectangles.
    :param join_distant_y_rect: bool: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    # Get the current horizontal text block bbox
    _horiz_bbox: IRect = horiz_bboxes[block_idx]

    # Extend an existing column with the current horizontal text block bbox
    # or make a new column with it
    _new_or_extd_col, _col_idx, _chk_extend_col = (
        _extend_existing_col_or_make_new_col(
            horiz_bbox=_horiz_bbox,
            column_bboxes=column_bboxes,
            path_bboxes=path_bboxes,
            vert_bboxes=vert_bboxes,
            join_distant_y_rect=join_distant_y_rect,
        )
    )

    # At this stage:
    # _new_or_extd_col is:
    # - either the union of the current _horiz_bbox and one of the existing
    #   columns
    # - or a new column of its own.
    # _col_idx is the index of the corresponding column in column_bboxes.

    # Variable `column_bboxes` might have been modified in
    # _extend_existing_col_or_make_new_col(): one new column might have been
    # appended to it if the current _horiz_bbox could not be used to extend
    # any existing column).

    # However, if the _new_or_extd_col did not collide with any other column,
    # no modification has yet been made in the list of column (the extended
    # column has not yet been saved).

    # Accordingly, if _chk_extend_col is True (and only in this case):
    # we want to check whether the extended column collides with
    # an horizontal text block. If so, this means that there is
    # an horizontal text rectangle inside the column that has not
    # been added to the column.
    # => in this case, _horiz_bbox is the beginning of a new column.
    # => else: the column can be extended.
    if _chk_extend_col:
        _make_new_extendable_col_or_confirm_new_or_extd_col(
            extended_col=_new_or_extd_col,
            horiz_bbox=_horiz_bbox,
            col_idx=_col_idx,
            column_bboxes=column_bboxes,
            horiz_bboxes=horiz_bboxes,
            vert_bboxes=vert_bboxes,
        )

    # set the current _horiz_bbox to None so that it not be
    # checked again
    horiz_bboxes[block_idx] = None


def make_column_bboxes(
    column_bboxes: list[Rect | IRect],
    horiz_bboxes: list[Rect],
    path_bboxes: list[Rect],
    vert_bboxes: list[Rect],
    path_rects: list[Rect],
    join_distant_y_rect: bool,
) -> list[Rect | IRect]:
    '''
    Iterates the horizontal text block bbox Rectangles stored in horiz_bboxes
    and, for each of them, checks whether it can extend one of the column bbox
    Rectangles stored in column_bboxes.

    Else, appends a new column to column_bboxes.

    :returns: a list of text column bbox Rectangles.

    :param column_bboxes: list[Rect | IRect]: the list of columns bboxes that
        is being built. Initialized with the first horizontal text block
        bbox Rectangle.

    :param horiz_bboxes: list[Rect]: the list of horizontal text block
        bbox Rectangles.

    :param path_bboxes: list[Rect]: the list of path block bbox Rectangles.

    :param vert_bboxes: list[Rect]: the list of vertical text block
        bbox Rectangles.

    :param path_rects: list[IRect]: the identified vg clusters rectangles.

    :param join_distant_y_rect: bool: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remain
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    # iterate the list of horizontal text block bbox Rectangles
    # (which starts at text block + 1) and either append new columns
    # to column_bboxes or extend one of the existing columns.

    # Set the end index of the range to iterate on the horizontal
    # bboxes
    _end_horizontal_text_blocks_bboxes: int = len(horiz_bboxes)

    # Prepare a _make_column_bbox_partial partial for easier iteration
    _make_column_bbox_partial: Callable = functools.partial(
        _make_column_bbox,
        column_bboxes=column_bboxes,
        horiz_bboxes=horiz_bboxes,
        path_bboxes=path_bboxes,
        vert_bboxes=vert_bboxes,
        join_distant_y_rect=join_distant_y_rect,
    )

    # Iterate on the horizontal text blocks bboxes and turn them into
    # columns
    for _block_idx in range(0, _end_horizontal_text_blocks_bboxes):
        _make_column_bbox_partial(block_idx=_block_idx)

    # return the identified column bboxes after some post-processing
    # (deleting duplicates, joining rectangles) and sorting
    return post_process_column_blocks(
        column_blocks=column_bboxes,
        path_rects=path_rects,
        join_distant_y_rect=join_distant_y_rect,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
