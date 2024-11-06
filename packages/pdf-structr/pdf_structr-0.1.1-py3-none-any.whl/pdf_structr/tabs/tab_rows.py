# tab_rows.py
'''
Module encapsulating everything related to the initial
making of table rows and the functions that permit to
compute additional properties for the rows.
'''

import logging
from typing import Any

import pymupdf  # type: ignore

from pdf_structr.tabs.prep_stats import (
    compute_fprop_block_or_row,
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
# Make stack
#####################


def _make_cell(
    line: dict[str, tuple[float, float, float, float] | list[dict]],
) -> dict:
    '''
    Converts a line into a table cell.
    '''
    return {
        'bbox': line['bbox'],  # type: ignore
        'spans': line['spans'],  # type: ignore
    }


def _make_row(block: dict[str, int | float | tuple | list]) -> dict:
    '''
    Converts a block into a table row.
    '''
    return {
        'bbox': block['bbox'],  # type: ignore
        'cells': [
            _make_cell(_line)
            # NOTE: Implicitly, here, we're assuming that a line
            # is equal to a cell.
            # This might however not always be the case.
            # Sometimes (and in particular when extending),
            # we notice that cells may encompass several lines.
            for _line in block['lines']  # type: ignore
        ],
    }


def make_rows(
    block_cluster: list[dict[str, int | float | tuple | list]],
) -> list[dict]:
    '''
    Convert a list of blocks pertaining to the same table into
    a list row dict. A row dict has a key 'bbox' and a key
    'cells', which contains a list of dict, where each dict
    has a key 'bbox' and a key 'spans' to store the spans
    that pertain to the cell.

    'cells' are to 'rows' what 'lines' are to 'blocks'.

    '''

    return [_make_row(_row_block) for _row_block in block_cluster]


#####################
# Row properties stack
#####################


def _compute_row_properties(row: dict[str, Any]) -> None:
    '''
    Compute rows properties on the fonts contained in the spans.

    :param row: dict[str, Any]: a row in a table.
    '''

    # Compute the bold and italic proportions
    _properties_tuple: tuple[
        int, tuple[float, float], float, float, float, tuple[float, float]
    ] = compute_fprop_block_or_row(
        row,
        'cells',
    )

    # Store the text length
    row['txt_len'] = _properties_tuple[0]

    # Store the font size mode and relevancy score
    row['fs_mode'] = _properties_tuple[1]

    # Store the bold proportion
    row['bold_prop'] = _properties_tuple[2]

    # Store the italic proportion
    row['italic_prop'] = _properties_tuple[3]

    # Store the mono proportion
    row['mono_prop'] = _properties_tuple[4]

    # Store the color mode and relevancy score
    row['color'] = _properties_tuple[5]


def _compute_table_rows_properties(
    table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]
) -> dict[
    str,
    int  # page number
    | float  # reference y1_gap
    | pymupdf.Rect  # table's bbox
    | list[dict]  # a list of rows[cells[spans]]
    | list[tuple[float, float, float, float]],  # list of cols bbox
]:
    '''
    Compute rows properties for all the passed-in table.

    :param table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: a basic table dictionary.
    '''
    for _row in table['rows']:  # type: ignore
        _compute_row_properties(row=_row)  # type: ignore

    return table


def compute_tables_rows_properties(
    tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
) -> list[
    dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]
]:
    '''
    Compute rows properties for all the passed-in tables.

    :param tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of basic table dictionaries.

    '''
    return [_compute_table_rows_properties(table=_table) for _table in tables]
