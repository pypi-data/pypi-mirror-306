# main.py
'''
Grouping of blocks vertically separated by a significant white space
by rows. The rows grouping intervenes when several successive rows
of blocks appear to have the same number of columns.

'''

import logging

import pymupdf  # type: ignore

from pdf_structr.tabs_clb.coords import (
    flatten_blocks_to_spans_and_compute_prows_coords,
    get_tentative_tables_multiple_rows_coords,
)
from pdf_structr.tabs_clb.lib import (
    are_rows_likely_rows_in_same_table,
)
from pdf_structr.tabs_clb.nclusts import (
    make_simple_idx_rect_bbox_for_remaining_tlike_rows,
    remove_clusterized_rows_from_rows_list,
)
from pdf_structr.tabs_clb.prototrs import (
    select_table_like_individual_rows,
)
from pdf_structr.tabs_clust.clustc_blocks_to_rows import (
    get_rows_of_ws_sep_blocks,
)
from pdf_structr.tabs_clust.clustc_ho_trows import (
    group_items_by_clusters_of_consecutive_items_with_same_coll_count,
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
# Group rows by clusters
#####################


def _get_rows_of_blocks(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[
    tuple[  # a row of blocks
        int,  # index number of the row
        tuple[float, float, float, float],  # its bbox
        list[tuple[float, float]],  # list of columns' x0 and x1
        list[dict],  # list of spans
    ],
]:
    '''
    Get rows (groups) of blocks vertically separated by significant white
    spaces.

    :returns: a list of rows, with internal coordinates (row's bboxes and
        column's x0 and x1), still to be grouped into clusters or be treated
        as a table of its own.

    :param blocks: list[dict[str, int | float | tuple | list]]: a list of
        text blocks.
    '''
    # 1. Make rows of blocks close enough vertically to belong to the same row
    # (so-called page rows)
    _prows: list[tuple[int, list[dict]]] = get_rows_of_ws_sep_blocks(blocks)

    # 2. Compute page rows' coordinates (bbox and columns coordinates) and
    # flatten their spans
    _rows_with_coords: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[dict],  # list of spans
        ],
    ] = flatten_blocks_to_spans_and_compute_prows_coords(_prows)

    return _rows_with_coords


def get_table_like_blocks_groups(
    page,
    blocks: list[dict[str, int | float | tuple | list]],
) -> tuple[
    list[
        tuple[
            list[int],  # idx nbrs of page rows inside the table
            pymupdf.Rect,  # the table's bbox
            list[tuple[float, float]],  # the rows' y coordinates
            list[tuple[float, float]],  # the cols x coordinates
        ]
    ],
    list[
        tuple[
            int,  # index number of the row from which the table has been made
            pymupdf.Rect,
        ]
    ],
]:
    '''
    From the passed-in blocks:

    - identifies blocks vertically separated by significant white space
    and groups them in rows
    - numbers the rows and flattens the blocks inside each row into a
    list of their spans
    - uses the spans to identifiy rows that contain at least two columns

    -> multirows tables
    - groups the rows by clusters of consecutive rows with the same
    columns' count
    - computes the multirows tables' bboxes, rows x coordinates and columns y
    coordinates

    # -> monorow tables
    - detect monorows tables
    - computes the monorows tables' bboxes, rows x coordinates and columns y
    coordinates

    :return: two list, a list coordinates for the multirow tables and a list
    of coordinates for monorow tables.

    Coordinates for multirow tables are presented as a 3-tuple containing
    the following information:

    - a table Rectangle
    - a corresponding list of ys coordinates of each of the rows (y0 and y1)
    - a corresponding list of xs coordinates of each of the cols (x0 and x1)

    Coordinates for monorow tables are presented as 2-tuple containing the
    following informaion:

    - a table Rectangle
    - a corresponding list of xs coordinates of each of the cols (x0 and x1)

    :param page: pymupdf.Page: the pymupdf Page. For later use.

    :param blocks: list[dict]: a list of text blocks.

    '''

    # 1. Make groups of blocks close enough vertically to belong to the same
    #    row and compute the rows' coordinates (bbox and columns coordinates)
    #    and flatten their spans
    _rows_with_coords: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[dict],  # list of spans
        ],
    ] = _get_rows_of_blocks(blocks)

    # 2. Filter out rows which are not table-like (multi-cols) or are
    #    bulleted paragraphs mistakenly identified as table-like.
    _table_like_rows: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ]
    ] = select_table_like_individual_rows(
        rows_with_col_coords=_rows_with_coords,
    )

    # 2. Group rows by groups of consecutive rows containing the same
    #    number of columns
    _tentative_tables_multiple_rows: list[
        # Each list is a multi-row table
        list[
            # Each tuple is one of the rows in the multi-row table
            tuple[
                int,  # idx num
                tuple[float, float, float, float],  # row bbox
                list[tuple[float, float]],  # cols x0 and x1
                list[list[dict]],  # list of spans grouped by cells
            ]
        ]
    ] = group_items_by_clusters_of_consecutive_items_with_same_coll_count(
        items=_table_like_rows,
        are_items_likely_rows_in_same_table_fn=(
            are_rows_likely_rows_in_same_table
        ),
    )

    # 3. Build coordinates for each multi-row column
    #
    # For each _tentative_tables_multiple_rows, we want to have:
    # - a bbox
    # - a list of x0 - x1 coordinates for its rows
    # - a list of y0 - y1 coordinates for its columns
    # - a list of its rows
    #
    # Eventually, a list of its spans or even better, its blocks
    _tentative_tables_multiple_rows_coords: list[
        tuple[
            list[int],  # the index numbrs of the rows in the table
            pymupdf.Rect,  # the table's bbox
            list[tuple[float, float]],  # the rows' y coordinates
            list[tuple[float, float]],  # the cols x coordinates
        ]
    ] = get_tentative_tables_multiple_rows_coords(
        _tentative_tables_multiple_rows
    )

    # 4. Remove the rows gathered into `_tentative_tables_multiple_rows`
    #    from the list of rows
    _remaining_tlike_rows: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ],
    ] = remove_clusterized_rows_from_rows_list(
        tentative_tables_multiple_rows_coords=(
            _tentative_tables_multiple_rows_coords
        ),
        table_like_rows=_table_like_rows,
    )

    # 6. Now we have removed non-table like rows, collected tentative tables
    #    made out of consecutive rows of blocks and removed the rows
    #    that have been embedded in such multirow tables.
    #
    # The remaining rows are necessarily table-like rows. We just want to
    # simplify their form to their idx number and their bbox as a Rect
    # to be able to pass them as clips to the rlb table detection stack.
    _remaining_tlike_rows_coords: list[
        tuple[
            int,  # index number of the initial row
            pymupdf.Rect,  # row/table bbox as a Rect
        ]
    ] = make_simple_idx_rect_bbox_for_remaining_tlike_rows(
        remaining_tlike_rows=_remaining_tlike_rows,
    )

    # Return the tentative tables for multiple rows and the tables
    # from isolated rows
    return _tentative_tables_multiple_rows_coords, _remaining_tlike_rows_coords
