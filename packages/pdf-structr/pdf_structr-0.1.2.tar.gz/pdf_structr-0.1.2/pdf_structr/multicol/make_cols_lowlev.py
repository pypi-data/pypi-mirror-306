# make_col_lowlev.py
'''
Encapsulating the lower level functions of the code converting the text
blocks into columns.
'''

import logging

from pymupdf import IRect  # type: ignore

from pdf_structr.utils.utils import in_bbox

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


def _intersects_bboxes(bb: IRect, bboxes: list[IRect]) -> bool:
    '''
    Return True if a bbox touches bb, else return False.
    '''
    for bbox in bboxes:
        if not (bb & bbox).is_valid:
            return True
    return False


def _can_extend(
    extended_rect: IRect,
    extending_rect: IRect,
    excluding_bboxlist: list[IRect],
    vert_bboxes: list[IRect],
) -> bool:
    """
    Determines whether rectangle 'extended_rect' can be extended by
    'extending_rect' without intersecting any of the rectangles contained
    in 'bboxlist'.

    If so, that means that the column can be extended.

    :returns: True if 'extended_rect' has no intersections with any items of
        'bboxlist'.

    The function is called twice:

    1. when trying to figure out whether one of the horizontal txt block bbox
       shall be used to extend an existing column or as the first item in a new
       column, to check whether we collide with another existing column;

    2. when trying to figure out whether a new column or a column being
       extended shall be saved as a new column or as a column being
       extended, to check whether we collide with a remaining horizontal text
       block bbox.

    On the first call:

    - extended_rect is a column extended by the horizontal text block.

    - extending_rect is the same column before being extended.

    - excluding_bboxlist is the list of columns.

    On the second call:

    - extended_rect is a column extended by the horizontal text block.

    - extending_rect is the same horizontal text block.

    - excluding_bboxlist is the list of horizontal text blocks.

    Accordingly:

    - on the first call, it returns True if the column extended by the
      horizontal text block does not collide with any other existing column
      => this column can be extended by this horizontal text block.

    - on the second call, it returns True if the column extended by the
      horizontal text block does not collide with any other horizontal text
      block.

    :param extended_rect: IRect: either (i) the current column's bbox
        extended by the current horizontal block's bbox and or (ii) the current
        column's bbox.

    :param extending_rect: IRect: either (i) the current column's bbox or
        (ii) the current horizontal block's bbox.

    :param excluding_bboxlist: list[IRect]: either the list column bboxes
        or the list of horizontal text block bboxes. Items of bboxlist may
        be None if they have been removed. As we go down the page, more
        and more items in horiz_bboxes have been marked as None.

    :param vert_bboxes: list[IRect]:

    """
    _xtd_rect_does_intersect_vertical_bbox: bool = _intersects_bboxes(
        extended_rect, vert_bboxes
    )

    # Return false if the extended_rectangle intersect with a vertical
    # text block bbox
    if _xtd_rect_does_intersect_vertical_bbox:
        return False

    # bboxlist is either the column's list or the horizontal bbox list
    for _excluding_bb in excluding_bboxlist:

        # get some bboxes out of the way:
        # 1. already treated horizontal blocks bboxes
        # 2. the extending rect out of the way
        if _excluding_bb is None or _excluding_bb == extending_rect:
            continue

        # if all the intersections of any the rectangles in bboxlist
        # with the extended rectangle is empty, the extension is valid.
        #
        # - an intersection means the largest rectangle contained in both
        # _excluding_bb and extended_rect
        # - empty means that x0 >= x1 or y0 >= y1
        #
        # In the first call to _can_extend:
        # - bboxlist is the list of horizontal text blocks
        # - extended_rect is a column's bbox extended by extending_rect
        # - extending_rect is one of the horizontal text blocks
        # => _excluding_bb is another horizontal text block
        #
        # => (extended_rect & _excluding_bb).is_empty if:
        # _excluding_bb is on the left of extended_rect
        # _excluding_bb is above extended_rect
        if (extended_rect & _excluding_bb).is_empty:
            continue

        return False

    # To return True:
    # 1. extended_rect must not intersect with a vertical text bbox
    # 2. all the items in bboxlist must be either None or extending_rect or
    #    extended_rect must not intersect with any item in bboxlist.
    return True


def _different_backgrounds(
    this_col_bb: IRect,
    horiz_bbox: IRect,
    path_bboxes: list[IRect],
):
    '''
    Checks if this_col_bb and horiz_bbox have different background.

    If so, returns True. Else (same background), return False.
    '''
    return in_bbox(
        bb=this_col_bb,
        bboxes=path_bboxes,
    ) != in_bbox(
        bb=horiz_bbox,
        bboxes=path_bboxes,
    )


def _extension_possible(
    horiz_bbox: IRect,
    this_col_bb: IRect,
    path_bboxes: IRect,
    join_distant_y_rect: bool,
) -> bool:
    '''
    Test whether the vertical extension of this column with this horiz_bbox
    is possible.

    Three reasons:

    - this horizontal text box (horiz_bbox) is set to None: has already
      been used to extend an existing column or to make a new column.

    - this horizontal text box (horiz_bbox) cannot pertain to this column
      because its x coordinates are out of scope.

    - this horizontal text box (horiz_bbox) and the column do not share
      the same background color.

    :param horiz_bbox: IRect: the horizontal text block's bbox Rectangle that
        is going to be tested.

    :param this_col_bb: IRect: the current existing column in the loop over
        the existing columns.

    :param path_bboxes: IRect: this page's path's bboxes.

    :param join_distant_y_rect: bool: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    # If this horiz_bbox has already been used either as
    # a new column or to extend an existing column,
    # it cannot be used to extend this column.
    if horiz_bbox is None:
        return False

    # Never join across columns
    #
    # This is the case where this _horiz_bbox x coordinates prevent it
    # from pertaining to this column
    if (
        horiz_bbox is None
        or this_col_bb.x1 < horiz_bbox.x0
        or horiz_bbox.x1 < this_col_bb.x0
    ):
        return False

    # Never join across different background colors
    if _different_backgrounds(
        this_col_bb=this_col_bb,
        horiz_bbox=horiz_bbox,
        path_bboxes=path_bboxes,
    ):
        return False

    # Do not extend vertically when their is a wide
    # white space between the blocks
    if join_distant_y_rect:
        return True
    else:
        if abs(this_col_bb.y1 - horiz_bbox.y0) > 37:
            return False

    return True


def _try_extend_one_of_exist_col_with_horiz_bb(
    horiz_bbox: IRect,
    column_bboxes: list[IRect],
    path_bboxes: list[IRect],
    vert_bboxes: list[IRect],
    join_distant_y_rect: bool,
) -> tuple[bool, IRect | None, int]:
    '''
    Takes in an horizontal text block (horiz_bbox) and checks whether
    it can extend one of the existing columns.

    :returns: a 3-tuple, with:

    - a bool (_check_can_extend): True if horiz_bbox can extend one
      of the existing columns and False otherwise.

    - an IRect or None: if an IRect, it is the union of the horiz_bbox
      and the column's bbox which can be extended by horiz_bbox (union
      means the smallest rectangle containing both the column's bbox
      and horiz_bbox). If no column where found to be extendable, it may
      be either the union of the last column in the list and horiz_bbox
      or None.
      This is why the first returned bool is important.

    - an int representing the index number of the column which the horiz_bbox
      can extend or, if it is not possible to extend any column with the
      current horiz_bbox, the index number of the last column.

    :param horiz_bbox: IRect: the horizontal text block's bbox Rectangle that
        is going to be tested.

    :param column_bboxes: list[IRect]: the list of columns' bbox Rectangles.

    :param path_bboxes: list[IRect]: the list of bboxes for the graphic
        vectors.

    :param vert_bboxes: list[IRect]: the list of vertical text block's
        bbox Rectangles.

    :param join_distant_y_rect: bool: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.
    '''
    # Declare a sentinel that will mark whether the passed-in horiz_bbox
    # can extend one of the columns bboxes. Initialized at False.
    _check_can_extend: bool = False

    # Declare an IRect to be used to extend the eventual column that
    # would be identified as extendable by the current horiz_bbox.
    _temp_union: IRect | None = None

    # check if _horiz_bbox can extend one of the columns' bboxes
    for _col_idx in range(len(column_bboxes)):

        # get the current column block
        _this_col_bb: IRect = column_bboxes[_col_idx]

        # Extension of this column with this horiz_bbox is not
        # possible
        if not _extension_possible(
            horiz_bbox=horiz_bbox,
            this_col_bb=_this_col_bb,
            path_bboxes=path_bboxes,
            join_distant_y_rect=join_distant_y_rect,
        ):
            continue

        # temporary extension of the column
        # '|' is a binary operator for union between two rectangles.
        # _temp_union is the smallest rectangle containing both operands.
        _temp_union = horiz_bbox | _this_col_bb

        # check if _temp_union intersects with any existing column's
        # bbox Rects (or any vertical bbox).
        _check_can_extend = _can_extend(
            extended_rect=_temp_union,
            extending_rect=_this_col_bb,
            # here, bboxlist is the list of column_bboxes
            excluding_bboxlist=column_bboxes,
            vert_bboxes=vert_bboxes,
        )

        # if _temp_union does not intersect with any existing column (or
        # any vertical bbox), break out of the loop.
        if _check_can_extend is True:
            break

    return _check_can_extend, _temp_union, _col_idx


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
