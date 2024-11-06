# lib.py
'''
This module contains the functions testing whether consecutive rows
of cell-like blocks could pertain to the same table.

'''

import logging

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
# Test whether two rows are consecutive and have same col count above 1
# to decide whether they shall be grouped in the same table
#####################


def _are_rows_consecutive(
    curr_row_idx_nb: int,
    next_row_idx_nb: int,
) -> bool:
    '''
    Test if two rows index numbers following each other
    and returns False or True.
    '''
    return curr_row_idx_nb == next_row_idx_nb - 1


def _do_rows_have_same_col_count_and_more_than_2cols(
    curr_row_cols: list[tuple[float, float]],
    next_row_cols: list[tuple[float, float]],
) -> bool:
    '''
    Test whether two consecutive page rows have the same rows count and
    this count is more than one and returns True or False.

    :param curr_row_cols: list[tuple[float, float]]: the current row
        list of x0-x1 float per column.

    :param next_row_cols: list[tuple[float, float]]: the next row list
        of x0-x1 float per column.

    '''
    _curr_row_cols_count: int = len(curr_row_cols)
    _next_row_cols_count: int = len(next_row_cols)

    if _curr_row_cols_count < 2 or _next_row_cols_count < 2:
        return False

    return _curr_row_cols_count == _next_row_cols_count


def are_rows_likely_rows_in_same_table(
    curr_row: tuple[
        int,
        tuple[float, float, float, float],
        list[tuple[float, float]],
        list[dict],
    ],
    next_row: tuple[
        int,
        tuple[float, float, float, float],
        list[tuple[float, float]],
        list[dict],
    ],
) -> bool:
    '''
    Test whether two consecutive page rows have the same cols count and
    this count is more than one and returns True or False.
    '''
    return _are_rows_consecutive(
        curr_row[0], next_row[0]
    ) and _do_rows_have_same_col_count_and_more_than_2cols(
        curr_row[2], next_row[2]
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
