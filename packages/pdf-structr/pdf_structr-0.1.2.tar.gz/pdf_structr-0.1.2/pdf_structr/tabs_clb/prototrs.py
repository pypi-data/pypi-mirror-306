# prototrs.py
'''
Module encapsulating the functions that convert rows into proto-table
rows. A proto-table row is a row where the spans have been ordered
into the cells to which they pertain.

'''

import logging

import pymupdf  # type: ignore

from pdf_structr.write.handle_bullets import (
    bullet,
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
# Make cells
#####################


def _push_spans_to_cell(
    spans: list[dict],
    cell_coords: tuple[float, float],
) -> list[dict]:
    '''
    Returns a list of spans which located within a given
    column of the row (i.e. a cell).

    :param spans: list[dict]: the list of spans in the row.

    :param cell_coords: tuple[float, float]: the current cell
        x0 and x1 coordinates.

    '''
    return [
        _span
        for _span in spans
        if (
            (_span['bbox'][0] >= cell_coords[0])
            and (_span['bbox'][2] <= cell_coords[1])  # type: ignore
        )
    ]


def _make_cells_from_spans(
    row: tuple[
        int,
        pymupdf.Rect,
        list[tuple[float, float]],
        list[dict],
    ]
) -> list[list[dict]]:
    '''
    Groups the spans stored in the row by cols/cells.
    '''
    # Get the list of spans in the row
    _row_spans: list[dict] = row[3]
    # Get the list of cols/cells x coordinates
    _row_cells_coords: list[tuple[float, float]] = row[2]

    return [
        _push_spans_to_cell(_row_spans, _cell_coords)
        for _cell_coords in _row_cells_coords
    ]


#####################
# Make tables
#####################


def _group_rows_spans_by_cells(
    table_like_rows: list[
        tuple[
            int,
            pymupdf.Rect,
            list[tuple[float, float]],
            list[dict],
        ]
    ],
) -> list[
    tuple[
        int,
        pymupdf.Rect,
        list[tuple[float, float]],
        list[list[dict]],
    ]
]:
    '''
    For each table like row, groups its spans by cols/cells.

    :returns: the passed-in rows where the spans have been grouped by
        the cells to which they pertain.

    :param table_like_rows: list[
        tuple[
            int,
            pymupdf.Rect,
            list[tuple[float, float, float, float]],
            list[dict],
        ]
    ]: a list of table-like rows (i.e. rows containing more than one single
        column).
    '''
    return [
        (
            _row[0],
            _row[1],
            _row[2],
            _make_cells_from_spans(_row),
        )
        for _row in table_like_rows
    ]


#####################
# Filter out noise
#####################


def _first_col_bullet_only(
    first_col_spans: list[dict],
) -> bool:
    '''
    Basic filtering out bulleted list recognized as tables.

    :param first_col_spans: list[dict]: the list of spans pertaining
        to the first column.
    '''

    # Test if all the first column spans are bullets
    if all(
        _first_col_span['text'].strip() in bullet
        for _first_col_span in first_col_spans
    ):
        return True

    # Test if all the first column spans are bullets
    if all(
        _first_col_span['text'].strip() == 'o'
        for _first_col_span in first_col_spans
    ):
        return True

    return False


#####################
# Filtering out bulleted rows
#####################


def _filter_out_bulleted_rows(
    table_like_rows: list[
        tuple[
            int,  # row index number
            tuple[float, float, float, float],  # row's bbox
            list[tuple[float, float]],  # cols/cells x0-x1
            list[dict],  # the spans in the row
        ]
    ]
) -> list[
    tuple[
        int,  # index number of the row
        tuple[float, float, float, float],  # its bbox
        list[tuple[float, float]],  # list of columns' x0 and x1
        list[list[dict]],  # list of spans
    ]
]:
    '''
    Filters out bulleted paragraphs that have been detected as
    tables and return a list of table-like rows' bboxes as Rect.

    :returns: for each row, a 4-tuple with:

        - the row's index number
        - its bbox as a 4-float tuple
        - the list of x0-x1 coords of its columns
        - the list of its spans

    :param table_like_rows: list[
        tuple[
            int,  # row index number
            tuple[float, float, float, float],  # row's bbox
            list[tuple[float, float]],  # cols/cells x0-x1
            list[dict],  # the spans in the row
        ]
    ]: a list of the rows that appears to have more than one column.

    '''
    # b. Put the spans into raw cells
    _tables: list[
        tuple[
            int,
            tuple[float, float, float, float],
            list[tuple[float, float]],
            list[list[dict]],  # <- spans grouped by cells/cols
        ]
    ] = _group_rows_spans_by_cells(table_like_rows=table_like_rows)

    # c. Filter out bulleted lists: first column composed of bullets only
    #    and return the tables' bboxes as a list of tuples row idx - tab bbox
    return [
        _table
        for _table in _tables
        if not _first_col_bullet_only(_table[3][0])
    ]

    # d. make inner rows
    #
    # NOTE: formerly, tried to compute inner rows within the identified
    # potential table, but the result was disappointing.
    # `compute_table_with_inner_rows_coords()` is located in module
    # `clusts_nclusts_irs`.
    #
    # _tables_with_inner_rows_coords: list[
    #     tuple[
    #         # index number of the row from which the table has been made
    #         int,
    #         pymupdf.Rect,  # table's bbox
    #         # table's columns bboxes
    #         list[tuple[float, float, float, float]],
    #         list[tuple[float, float]],  # rows y0-y1 coords
    #         list[list[dict]],  # the list of spans in each of their cols
    #     ]
    # ] = [compute_table_with_inner_rows_coords(_table) for _table in _tables]

    # return _tables_with_inner_rows_coords


def select_table_like_individual_rows(
    rows_with_col_coords: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[dict],  # list of spans
        ],
    ],
) -> list[
    tuple[
        int,  # index number of the row
        tuple[float, float, float, float],  # its bbox
        list[tuple[float, float]],  # list of columns' x0 and x1
        list[list[dict]],  # list of spans grouped by cells
    ]
]:
    '''
    Selects the rows of blocks that appear to have several columns, filtering
    out rows corresponding to bulleted paragraphs that would otherwise
    be identified as table rows.

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
    # 1. Select the table-like individual rows (rows that appear to have more
    # than one column) out of the list of rows
    _table_like_individual_rows: list[
        tuple[
            int,
            tuple[float, float, float, float],
            list[tuple[float, float]],
            list[dict],
        ]
    ] = [_row for _row in rows_with_col_coords if len(_row[2]) > 1]

    # 2. Filter out noise (bulletted list recognized as tables) and for
    #    each table like, return one (row index - bbox) tuple
    _tables_like_rows_bbox: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ]
    ] = _filter_out_bulleted_rows(table_like_rows=_table_like_individual_rows)

    return _tables_like_rows_bbox
