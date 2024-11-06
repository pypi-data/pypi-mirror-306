# clustc_blocks_to_rows.py
'''
Functions grouping blocks into rows, where a row is cluster
of blocks vertically separated by some significant white-space.

Used both by the clb and the rlb stacks.
'''

import logging
from typing import Callable

from pdf_structr.tabs.prep_stats import (
    compute_ftsize_mode_for_block_or_row,
)
from pdf_structr.tabs.tab_enl_nr_utils import (
    flatten_lines_in_blocks,
    make_new_row_from_lines,
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
# Group blocks by rows of blocks
#####################


def _append_block_to_ws_sep_row(
    blocks: list[dict],
    ws_sep_rows: list[tuple[int, list[dict]]],
    idx: int,
    ws_comput_fn: Callable,
) -> None:
    '''
    Appends the current block to one of the vertical white-space separated rows
    (list of blocks).

    :param blocks: list[dict]: a list of text blocks.

    :param ws_sep_rows: list[tuple[int, list[dict]]]: the list of vertical
        white-space separated list of blocks.

    :param idx: int: the index to get the current block.

    :param ws_comput_fn: Callable: the white space thresholds
        computation function.

    '''

    # Get the current row from blocks list
    _curr_block: dict = blocks[idx]

    # Get the last block from the last row from the rows list
    _prev_block: dict = ws_sep_rows[-1][1][-1]

    # Compute the white space's height
    _ws_height: float = _curr_block['bbox'][1] - _prev_block['bbox'][3]

    # Compute the white space thresholds
    _ws_thresholds = ws_comput_fn(_curr_block)

    # If y gap between block exceeds the white space threholds, create
    # new row
    # i.e. a new row
    if _ws_height > _ws_thresholds:

        ws_sep_rows += [
            (
                # row index number: last row index number + 1
                ws_sep_rows[-1][0] + 1,
                [_curr_block],  # list of blocks in the row
            )
        ]

    # Else append this block to the current row
    else:

        ws_sep_rows[-1][1].append(_curr_block)


def _get_ftsize_mode_for_block(block: dict):
    '''
    Gets the font size mode for a block, slightly adjusted
    downwards.

    The font size will be used as the y-gap white space thresholds
    between two blocks, lines or spans when trying agglutinate them
    in rows of text vertically separated by white space.
    '''
    # Take only the first float from the returned tuple
    # i.e. the font size (the second float is font
    # size mode relevancy indicator).
    return (
        compute_ftsize_mode_for_block_or_row(
            main_dict=block, subdict_key='lines'
        )[0]
        * 0.8
    )


def _make_rows_of_blocks_separated_by_sign_horiz_ws(
    blocks: list[dict],
    ws_comput_fn: Callable,
) -> list[tuple[int, list[dict]]]:
    '''
    Group the rows by list of rows separated by significant
    horizontal white space.

    :param blocks: list[dict]: a list of text blocks.

    :param ws_comput_fn: Callable: the white space thresholds
        computation function.

    '''
    # Sort the blocks top to bottom by bottom y and left to right by left x
    blocks.sort(key=lambda _block: (_block['bbox'][3], _block['bbox'][0]))

    # Create rows
    # Initialize the white-space separated list of lists of blocks
    _ws_sep_rows: list[tuple[int, list[dict]]] = [(0, [blocks[0]])]

    for _idx in range(1, len(blocks)):

        _append_block_to_ws_sep_row(blocks, _ws_sep_rows, _idx, ws_comput_fn)

    return _ws_sep_rows


#####################
# API for the rlb stack when trying to extend existing tables
#####################


def _convert_ws_list_sep_blocks_to_tentative_row_of_spans(blocks: list[dict]):
    '''
    Convert a list of blocks into a tentative row.

    :param blocks: list[dict]: a list of blocks.
    '''

    return make_new_row_from_lines(flatten_lines_in_blocks(blocks))


def convert_blocks_to_candidate_rows(
    blocks: list[dict],
) -> list[list[dict]]:
    '''
    Converts a list of blocks into a list of candidate rows, by
    grouping the blocks into clusters of blocks vertically separated
    by significant white-space.

    :param blocks: list[dict]: a list of text blocks.

    :param table: dict: the current table dictionary.

    :param ext_direction: int: -1 or 0, with -1 being when extending
        upwards and 0 when extending downwards.

    '''
    # Define function computing the whitespace thresholds for
    # clustering
    _ws_comput_fn: Callable = _get_ftsize_mode_for_block

    # We now need to find columns
    return [
        _convert_ws_list_sep_blocks_to_tentative_row_of_spans(_blocks)
        for _, _blocks in _make_rows_of_blocks_separated_by_sign_horiz_ws(
            blocks,
            _ws_comput_fn,
        )
    ]


#####################
# API for the clb stack when initially trying to detect rows on the page
#####################


def get_rows_of_ws_sep_blocks(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[tuple[int, list[dict]]]:
    '''
    Sort the blocks from top to bottom and left to right and
    groups them by row of blocks separated by a significant
    white space.

    :return: a list of tuples, where each tuple is a white-space
        separated cluster of rows and contains:

        - the index number of the row
        - the list of blocks in the row

    :param blocks: list[dict]: a list of text blocks.
    '''
    # Define function computing the whitespace thresholds
    # between two blocks for clustering
    _ws_comput_fn: Callable = _get_ftsize_mode_for_block

    return _make_rows_of_blocks_separated_by_sign_horiz_ws(
        blocks, _ws_comput_fn
    )
