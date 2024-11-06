# clust_rlb_lib.py
'''
Module encapsulating some of the functions used by
module `clust_rlb`.

'''


import logging
import math

from pdf_structr.stats.prep_stats import (
    compute_ftsize_mode_for_block_or_row,
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
# Testing whether two blocks are rows to the same table
#####################


def _get_rounded_block_height(
    block: dict,
) -> float:
    '''
    Get the block top and bottom ys and its height, slightly enlarged.
    '''
    _block_top_y: float = math.ceil(block['bbox'][1])
    _block_bottom_y: float = math.ceil(block['bbox'][3])

    return _block_bottom_y - _block_top_y


def _is_block_about_same_height_its_mode_font_size(
    block_height: float,
    fs_mode_tup: tuple[float, float],
) -> bool:
    '''
    Test whether a block's height is about the same as its font size
    mode, if such font size mode is relevant.

    :param block_height: float: block's height.

    :param fs_mode_tup: tuple[float, float]: the font size mode and font size
        mode relevancy for the current block.
    '''
    return (
        # if the font size mode is relevant
        (fs_mode_tup[1] > 0.6)
        # and the block's height is about 1.4 times the font size mode
        and (block_height <= fs_mode_tup[0] * 1.4)
    )


def _is_block_about_same_height_its_highest_line(
    block: dict,
    block_height: float,
) -> bool:
    '''
    Test whether the block's height is about the same as the
    highest line it contains.
    '''
    # Compute the lines' heights
    _lines_y0: list[float] = [
        math.ceil(_line['bbox'][1]) for _line in block['lines']
    ]

    _lines_y1: list[float] = [
        math.ceil(_line['bbox'][3]) for _line in block['lines']
    ]

    _lines_heights: list[float] = [
        _line_y1 - _line_y0 for _line_y1, _line_y0 in zip(_lines_y1, _lines_y0)
    ]

    # take the highest line's height
    _lines_heights.sort()
    _max_lines_height: float = _lines_heights[-1]

    if (block_height - _max_lines_height) <= block_height * 1 / 10:
        return True

    return False


def _are_all_lines_on_same_geom_line(
    block: dict,
    fs_mode_tup: tuple[float, float],
) -> bool:
    '''
    Test whether all the lines in the block are on the same geometrical
    line.

    :param block: dict: a block dict.

    :param fs_mode_tup: tuple[float, float]: the font size mode and font size
        mode relevancy for the current block.

    '''

    # Get the block's height, slightly enlarged
    _block_height: float = _get_rounded_block_height(block)

    # If the font size mode is relevant, we can test the ratio of
    # the block's height to the font size mode
    if _is_block_about_same_height_its_mode_font_size(
        _block_height, fs_mode_tup
    ):
        return True

    # Else test if the block's height is about the same as the one of its
    # highest line
    if _is_block_about_same_height_its_highest_line(block, _block_height):
        return True

    # Otherwise, it is very highly likely that the lines are on different
    # geometrical lines.
    return False


def _are_spans_xs_far_enough_to_be_cells(
    block: dict,
    fs_mode_tup: tuple[float, float],
) -> bool:
    '''
    Test if the spans in the block are too close or even overlapping
    horizontally to be likely cells.

    At this stage, we know that the all the lines are on the same
    geometrical line (and accordingly, the spans also) because this
    was checked in `_are_all_lines_on_same_geom_line`.

    It is assumed that tables cells are separated by an horizontal
    distance at least equal to one time the font size.

    :param block: dict: a block dict.

    :param fs_mode_tup: tuple[float, float]: the font size mode and font size
        mode relevancy for the current block.

    '''
    _flattened_spans_x0s_list: list[float] = [
        _spans['bbox'][0]
        for _line in block['lines']
        for _spans in _line['spans']
    ]

    _flattened_spans_x1s_list: list[float] = [
        _spans['bbox'][2]
        for _line in block['lines']
        for _spans in _line['spans']
    ]

    for _x1_this_span, _x0_next_span in zip(
        # exclude last span
        _flattened_spans_x1s_list[:-1],
        # exclude first span; start with second one
        _flattened_spans_x0s_list[1:],
    ):
        if (
            # if the font size mode is relevant
            (fs_mode_tup[0] > 0.6)
            # and the x gap between two consecutive spans is
            # below the font size mode
            and (_x0_next_span - _x1_this_span) < fs_mode_tup[0]
        ):
            return False

        # if the font size mode is not relevant, the x gap
        # between the spans shall be at least 3
        if (_x0_next_span - _x1_this_span) <= 3:
            return False

    return True


def _do_blocks_contain_likely_cells(
    this_block: dict,
    next_block: dict,
) -> bool:
    '''
    Test the inner structure of two consecutive blocks (i.e. spans and lines
    composition and positions) in two consecutive blocks to assess whether
    the blocks could be consecutive rows in a table.

    Criteria:
    - already met from pre-selection: same number of spans in each blocks
    - now testing:
        - if all the lines in the block are on the same geometrical line
        - if the spans are far enough from each other to form likely cells
    '''
    _fs_mode_tup_list: list[tuple[float, float]] = [
        compute_ftsize_mode_for_block_or_row(_block, 'lines')
        for _block in [this_block, next_block]
    ]

    return (
        # verticality test
        _are_all_lines_on_same_geom_line(this_block, _fs_mode_tup_list[0])
        and _are_all_lines_on_same_geom_line(next_block, _fs_mode_tup_list[1])
    ) and (
        # horizontality test
        _are_spans_xs_far_enough_to_be_cells(this_block, _fs_mode_tup_list[0])
        and _are_spans_xs_far_enough_to_be_cells(
            next_block,
            _fs_mode_tup_list[1],
        )
    )


def are_blocks_likely_rows_in_same_table(
    curr_block: dict[str, int | float | tuple | list],
    next_block: dict[str, int | float | tuple | list],
) -> bool:
    '''
    Test whether the two blocks are consecutive and whether they
    have the same spans' count and returns True or False.

    :param curr_block: dict[str, int | float | tuple | list]: the current
        block in the iteration on the blocks.

    :param next_block: dict[str, int | float | tuple | list]: the next
        block in the iteration on the blocks.

    '''

    _test = (
        (
            # are the block consecutive?
            curr_block['_bno'] + 1  # type: ignore
            == next_block['_bno']
        )
        and (
            # do the two blocks have the same spans' count?
            curr_block['spans_count']
            == next_block['spans_count']
        )
        and _do_blocks_contain_likely_cells(curr_block, next_block)
    )

    if _test is True:
        pass

    return _test


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
