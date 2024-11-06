"""
Module to encapsulate the post-processing cleaning functions for multi_column.
"""

import logging

from pymupdf import IRect, Rect  # type: ignore

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
# Clean column blocks stack
#####################


def _remove_duplicates(blocks_count: int, column_blocks: list[Rect | IRect]):
    """
    Remove duplicate column bbox Rectangles.

    :param blocks_count: int: the number of column blocks.
    :param column_blocks: list[IRect]: the list of column blocks.
    """
    # Define the starting point of the range
    _start: int = blocks_count - 1

    # Iterate the columns back to front
    for _i in range(_start, -1, -1):
        # Get the current and the previous block
        _current_block: IRect = column_blocks[_i]
        _previous_block: IRect = column_blocks[_i - 1]

        # If duplicates, delete the last column block
        if _current_block == _previous_block:
            del column_blocks[_i]


def _reorder_column_sequence(
    column_blocks: list[Rect | IRect],
    i1: int,
    i0: int,
) -> None:
    '''
    Sort the column sequence.

    :param column_blocks: list[Rect | IRect]: the list of columns Rectangles.
    :param i1: int: the index of last bbox with same bottom.
    :param i0: int: the index of the bbox with the _prev_y1 coordinate.
    '''
    # set the _end_idx of the sorted list to
    # the index number of the previous iteration
    _end_idx: int = i1 + 1

    # sort the column bboxes between -i0 and _end_idx
    # horizontally (by x0) in place
    # NOTE: Replacing in the middle of a list...
    column_blocks[i0:_end_idx] = sorted(
        column_blocks[i0:_end_idx], key=lambda b: b.x0
    )


def _reorder_column_sequence_when_diff_bottoms(
    column_blocks: list[Rect | IRect],
    last_same_bot_idx: int,
    start_index: int,
    curr_col: Rect | IRect,
    current_idx: int,
):
    '''
    When the current column does not have the same bottom as the reference
    bottom, we check whether the column sequence has more than one item
    and if so, we reorder it by left x (x0).

    :returns: the new bottom value and the corresponding new start index.

    :param column_blocks: list[Rect | IRect]: the list of columns Rectangles.
    :param last_same_bot_idx: int: the index of last bbox with same bottom.
    :param start_index: int: the index of the previous bbox having the
        bottom_value coordinate.
    :param curr_col: Rect | IRect: the current column in the column's
        iteration.
    :param current_idx: int: the index of the current column in the column's
        iteration.
    '''
    # if i1 > i0:  # segment length > 1? Sort it!
    #     nblocks[i0 : i1 + 1] = sorted(
    #         nblocks[i0 : i1 + 1], key=lambda b: b.x0
    #     )

    # segment length > 1? Sort it!
    # if more than one column in the sequence, sort them
    if last_same_bot_idx > start_index:

        _reorder_column_sequence(
            column_blocks=column_blocks,
            i1=last_same_bot_idx,
            i0=start_index,
        )

    # y1 = b1.y1  # store new bottom value
    # i0 = i  # store its start index

    # store the current column bottom value
    # as the new bottom value
    _new_bottom_value = curr_col.y1

    # store the current column index as the new start index
    _new_start_index = current_idx

    return _new_bottom_value, _new_start_index


def _reorder_column_sequence_acmb(
    column_blocks: list[Rect | IRect],
    current_idx: int,
    bottom_value: float,
    last_same_bot_idx: int,
    start_index: int,
) -> tuple[float, int, int]:
    '''
    Check whether the columns need to be resorted and sort them,
    as the case may be.

    :returns: the bottom y of the [previous column].

    :param column_blocks: list[Rect | IRect]: the list of columns Rectangles.
    :param current_idx: int: the idx of the current column index in the
        list of columns Rectangles.
    :param bottom_value: float: the bottom y of the previous column.
    :param last_same_bot_idx: int: the index of last bbox with same bottom.
    :param start_index: int: the index of the previous bbox having the
        bottom_value coordinate.
    '''
    # get the current column
    # b1 = nblocks[i]
    _curr_col: Rect | IRect = column_blocks[current_idx]

    # Prepare the default return values
    _new_bottom_value: float = bottom_value
    _new_start_index: int = start_index

    # if this column and the previous one have a y gap exceeding 3 pts
    # => different bottoms
    # if abs(b1.y1 - y1) > 3:  # different bottom
    if abs(_curr_col.y1 - bottom_value) > 3:

        # Reorder the relevant columns if needs be and reset
        # the _new_bottom_value and the _new_start_index
        _new_bottom_value, _new_start_index = (
            _reorder_column_sequence_when_diff_bottoms(
                column_blocks=column_blocks,
                last_same_bot_idx=last_same_bot_idx,
                start_index=_new_start_index,
                curr_col=_curr_col,
                current_idx=current_idx,
            )
        )

    # In all cases, store the current index as the index of
    # column with the index of last bbox with same bottom
    # i1 = i  # store current index
    _new_last_same_bot_idx: int = current_idx

    return _new_bottom_value, _new_last_same_bot_idx, _new_start_index


def _repair_column_sequence(column_blocks: list[Rect | IRect]) -> None:
    """
    In some cases, the sequence of blocks has to be repaired (i.e. the sorting
    needs to be corrected).

    :param column_blocks: list[Rect | IRect]: the list of columns.
    """
    # first column bottom coordinate defined as previous y1
    _bottom_value: float = column_blocks[0].y1

    # its index (we're starting at 0, obviously)
    _start_index: int = 0

    # index of last bbox with same bottom (-1, we don't know yet)
    _last_same_bot_idx: int = -1

    # Iterate over bboxes, identifying segments with approx. same bottom
    # value.
    # Replace every segment by its sorted version.

    # iterate front to back over the remaining column bboxes,
    # start with the second block (range(1, len...))
    for _curr_idx in range(1, len(column_blocks)):

        _bottom_value, _last_same_bot_idx, _start_index = (
            _reorder_column_sequence_acmb(
                column_blocks=column_blocks,
                current_idx=_curr_idx,
                bottom_value=_bottom_value,
                last_same_bot_idx=_last_same_bot_idx,
                start_index=_start_index,
            )
        )

    # at the end of the loop, if there remains some segment
    # waiting to be sorted
    if _last_same_bot_idx > _start_index:

        # Set the end index of the sequence to sort
        _end_idx: int = _last_same_bot_idx + 1

        # sort the column bboxes horizontally (by x0)
        # in place
        column_blocks[_start_index:_end_idx] = sorted(
            column_blocks[_start_index:_end_idx], key=lambda b: b.x0
        )


def clean_column_blocks(
    column_blocks: list[Rect | IRect],
) -> list[Rect | IRect]:
    """
    Old function clean_nblocks

    Do some elementary cleaning on the column block Rectangles:
    - remove duplicates
    - reorder the colummns

    :param column_blocks: list[Rect | IRect]: a list of Rect or IRect,
        each element covering a column.
    """
    # 0. preliminary stage

    # Get a count of the text column rectangles
    _blocks_count: int = len(column_blocks)

    # If the block count is 1 or 0, return
    if _blocks_count < 2:
        return column_blocks

    # 1. remove any duplicate blocks
    _remove_duplicates(_blocks_count, column_blocks)

    # 2. repair sequence in special cases
    # consecutive bboxes with almost same bottom value are sorted ascending
    # by x-coordinate.
    _repair_column_sequence(column_blocks)

    return column_blocks


# NOTE: For reference: clean_nblocks(nblocks) in
# b86b33fe985f2b8f33eafd45a4fde3642d5a3805
# pymupdf/RAG v.0.0.15
# def clean_nblocks(nblocks):
#     """Do some elementary cleaning."""
#     # 1. remove any duplicate blocks.
#     blen = len(nblocks)
#     if blen < 2:
#         return nblocks
#     start = blen - 1
#     for i in range(start, -1, -1):
#         bb1 = nblocks[i]
#         bb0 = nblocks[i - 1]
#         if bb0 == bb1:
#             del nblocks[i]
#     # 2. repair sequence in special cases:
#     # consecutive bboxes with almost same bottom value are sorted ascending
#     # by x-coordinate.
#     y1 = nblocks[0].y1  # first bottom coordinate
#     i0 = 0  # its index
#     i1 = -1  # index of last bbox with same bottom
#     # Iterate over bboxes, identifying segments with approx. same bottom
#     # value.
#     # Replace every segment by its sorted version.
#     for i in range(1, len(nblocks)):
#         b1 = nblocks[i]
#         if abs(b1.y1 - y1) > 3:  # different bottom
#             if i1 > i0:  # segment length > 1? Sort it!
#                 nblocks[i0 : i1 + 1] = sorted(
#                     nblocks[i0 : i1 + 1], key=lambda b: b.x0
#                 )
#             y1 = b1.y1  # store new bottom value
#             i0 = i  # store its start index
#         i1 = i  # store current index
#     if i1 > i0:  # segment waiting to be sorted
#         nblocks[i0 : i1 + 1] = sorted(
#             nblocks[i0 : i1 + 1], key=lambda b: b.x0
#         )
#     return nblocks


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
