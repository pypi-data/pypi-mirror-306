# tab_enl_nr_reg.py
'''

Library encapsulating the detection and creation of new
new rows (nr) when trying to enlarge (enl) a table previously
detected by stabs (sub module of stabs_tbs_enl).

'''

import functools
import logging
from typing import Callable

from pdf_structr.tabs.tab_add_row import add_tentative_row
from pdf_structr.tabs.tab_enl_nr_utils import (
    flatten_lines_in_blocks,
    is_tentative_row_acceptable,
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


#################################
# Make new row API
#################################


def make_new_row_decorator(make_new_row_fn: Callable) -> Callable:
    '''
    Function decorating the make_new_row_fn which may be either
    `make_new_row_from_closest_block` (also in this module),
    `make_new_row_from_blocks` (also in this module) or
    `make_new_row_when_discrepancy` (in module tab_enl_nr_dis).
    '''

    @functools.wraps(make_new_row_fn)
    def _make_new_row_wrapper(
        *args,
        **kwargs,
        # above_blocks: list[dict],
    ) -> bool:
        '''
        This wrapper gets a tentative row from the make_new_row_fn,
        assesses whether it is acceptable as a new row for the
        table and appends it to the tables row and updates the
        table as the case may be.

        :returns: True if it has extended the table or False otherwise.
        '''
        # If some neighboring blocks have been found, try to make a
        # new row from the lines living in the closest block
        # or from the lines living in the returned blocks.
        _tentative_row: list[dict] = make_new_row_fn(
            *args,
            **kwargs,
            # lines=above_blocks[-1]['lines']  # type: ignore
        )

        # If the _tentative_row is acceptable as a new row,
        # convert it into a row (with a bbox of its own)
        # and add it to the list of rows of the table
        if _extending := is_tentative_row_acceptable(
            _tentative_row,
            kwargs['table'],
        ):
            add_tentative_row(
                _tentative_row,
                kwargs['table'],
            )

        return _extending

    return _make_new_row_wrapper


def make_new_row_from_closest_block(
    neighbor_blocks: list[dict],
    idx_for_closest_block: int,
    *args,
    **kwargs,
) -> list[dict]:
    '''
    Try to make a tentative row out of the closest block by making
    a list of cells where cells are dict containing a list of spans
    and a bbox. Some cells may contains several close neighbors or
    overlapping lines/spans.

    The start and limit parameters are compared to each to determine
    whether the closest block shall be the first one in the list or
    the last one.

    returns: a tentative row as a list of cells.

    :param neighbor_blocks: list[dict]: a list of blocks living above the
        table.

    :param idx_for_closest_block: int: -1 or 0, with -1 being when extending
        upwards and 0 when extending downwards.

    :param start: float: the point (as a y coordinate) from which neighbor
        blocks have been collected.

    '''

    # Get the lines from the closest block
    _lines: list[dict] = neighbor_blocks[idx_for_closest_block][
        'lines'
    ]  # type: ignore

    # Pass the lines to _make_new_row_from_lines
    return make_new_row_from_lines(lines=_lines)


def make_new_row_from_blocks(
    neighbor_blocks: list[dict],
    *args,
    **kwargs,
) -> list[dict]:
    '''
    Try to make a tentative row out of a list of blocks by flattening
    the lines from the blocks into a single list and trying to make
    convert them into a list of cells where cells are dict containing
    a list of spans and a bbox. Some cells may contains several close
    neighbors or overlapping lines/spans.

    Returns a tentative row.

    :param neighbor_blocks: list[dict]: a list of blocks living above
        or below the table.

    '''

    # Flatten the lines in the blocks
    _lines: list[dict] = flatten_lines_in_blocks(neighbor_blocks)

    # Pass the lines to _make_new_row_from_lines
    return make_new_row_from_lines(lines=_lines)


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
