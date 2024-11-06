# nclusts.py
'''
Module encapsulating the functions that handle individual rows that may contain
by themselves a table and might be better treated with the rlb stack.

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


#####################
# Select isolated rows that may contain a table
#####################


def remove_clusterized_rows_from_rows_list(
    tentative_tables_multiple_rows_coords: list[
        tuple[
            list[int],  # the index numbrs of the rows in the table
            pymupdf.Rect,  # the table's bbox
            list[tuple[float, float]],  # the rows' y coordinates
            list[tuple[float, float]],  # the cols x coordinates
        ]
    ],
    table_like_rows: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ],
    ],
) -> list[
    tuple[
        int,  # index number of the row
        tuple[float, float, float, float],  # its bbox
        list[tuple[float, float]],  # list of columns' x0 and x1
        list[list[dict]],  # list of spans grouped by cells
    ],
]:
    '''
    Remove the rows that have been grouped into clusters of rows from the list
    of rows.

    :returns: the list of initial rows without the rows that have been grouped
    into a cluster.

    :param tentative_tables_multiple_rows: list[
        list[
            tuple[
                int,
                tuple[float, float, float, float],
                list[tuple[float, float]],
                list[list[dict]],  # list of spans grouped by cells
            ]
        ]
    ]: the groups of rows likely to represent tables.

    :param table_like_rows: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ],
    ]: the list of table-like rows.
    '''

    # Get the list of the indices of the rows that have already been
    # added to clusters of rows
    _clusterized_rows_idxs: list[int] = [
        _row_number
        for _tentative_table in tentative_tables_multiple_rows_coords
        for _row_number in _tentative_table[0]
    ]

    # Get rid of all the rows that have already been added to one of
    # the clusters
    return [
        _row
        for _row in table_like_rows
        if _row[0] not in _clusterized_rows_idxs
    ]


#####################
# External API: conversion of table-like isolated rows into simple Rect bboxes
#####################


def make_simple_idx_rect_bbox_for_remaining_tlike_rows(
    remaining_tlike_rows: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ],
    ],
) -> list[tuple[int, pymupdf.Rect]]:
    '''
    Selects the rows of blocks that appear to have several columns.

    Convert each of these rows to a basic table composed of one row
    and a list of cells/columns and cleans out bulleted (and TODO numbered)
    lists detected as tables.

    :returns: a list of tuple row idx - bbox, where each row is highly
        likely to contain an individual table.

    :param rows_with_col_coords: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[dict],  # list of spans
        ],
    ]: all the initially extracted rows.

    '''
    return [
        (_table[0], pymupdf.Rect(_table[1])) for _table in remaining_tlike_rows
    ]
