# tabs_validates.py
'''
Module to validate that the tables which have been
made are valid.

- cleaning up wrong first line.
- passing wrong last line from top table to bottom
table when two tables follow each other.
'''


import logging

import pymupdf  # type: ignore

from pdf_structr.tabs.tab_fns import (
    is_virtual_cell,
    pop_first_row,
    pop_last_row,
    recompute_columns,
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
# Playground
#####################


def _update_table_upon_popping_top_or_bottom_row(
    table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
):
    '''
    Recompute the columns bboxes upon popping top or bottom
    row.

    Recompute x0 and x1 of the table upon popping top or bottom
    row.
    '''
    # Recompute the columns bboxes
    recompute_columns(table)

    # Recompute the table's bbox x0 and x1
    table['bbox'].x0 = table['cols'][0][0]  # type: ignore
    table['bbox'].x1 = table['cols'][-1][2]  # type: ignore


def _check_table_and_remove_first_row_acmb(
    table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
) -> dict[
    str,
    int  # page number
    | float  # reference y1_gap
    | pymupdf.Rect  # table's bbox
    | list[dict]  # a list of rows[cells[spans]]
    | list[tuple[float, float, float, float]],  # list of cols bbox
]:
    '''
    If all the cells except the first one are virtual cells,
    this row cannot be the first row of the table
    (assuming tables do not start with a first row where only the first
    cell is filled).

    :param table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: a table dictionary.
    '''
    if all(
        is_virtual_cell(_cell)
        for _cell in table['rows'][0]['cells'][1:]  # type: ignore
    ):
        # Pop the first row
        pop_first_row(table)

        # Recompute table and columns bboxes
        _update_table_upon_popping_top_or_bottom_row(table)

    return table


def _check_tables_and_remove_first_row_acmb(
    tables: list[  # type: ignore
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
        int
        | float
        | pymupdf.Rect
        | list[dict]
        | list[tuple[float, float, float, float]],
    ]
]:
    '''
    Check whether the cells other than the first cell in the first row of
    each of the tables are virtual cells and removes the row (and recomputes)
    the table and columns bboxes accordingly.

    :param tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of table dictionaries.

    '''
    # Delete first row if first row is composed of something in the left cell
    # and only virtual cells to the right
    return [
        _check_table_and_remove_first_row_acmb(_table) for _table in tables
    ]


def _check_table_and_remove_last_row_acmb(
    table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
) -> dict[
    str,
    int  # page number
    | float  # reference y1_gap
    | pymupdf.Rect  # table's bbox
    | list[dict]  # a list of rows[cells[spans]]
    | list[tuple[float, float, float, float]],  # list of cols bbox
]:
    '''
    Opinionated way of selecting last row: we assume that the last
    row of a table cannot be composed of a virtual cell at the
    bottom right.

    :param table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: a table dictionary.
    '''
    _last_cell: dict = table['rows'][-1]['cells'][-1]  # type: ignore

    # If the last cell is a virtual cell
    if is_virtual_cell(_last_cell):

        # Pop the last row
        pop_last_row(table)

        # Recompute table and columns bboxes
        _update_table_upon_popping_top_or_bottom_row(table)

    return table


def _check_tables_and_remove_last_row_acmb(
    tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
) -> list[dict]:
    '''
    Check whether the cells other than the first cell and the last cell
    in the last row of each of the tables are virtual cells and removes
    the row (and recomputes) the table and columns bboxes accordingly.

    :param tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of table dictionaries.

    '''
    # Delete last row if last row is composed of something in the left cell
    # and only virtual cells to the right
    return [_check_table_and_remove_last_row_acmb(_table) for _table in tables]


def validate_tables(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    textpage_bbox: pymupdf.Rect,
    tables: list[  # type: ignore
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
        int
        | float
        | pymupdf.Rect
        | list[dict]
        | list[tuple[float, float, float, float]],
    ]
]:
    '''
    Validates each of the tables for erroneous first and last row.

    - erroneous first rows are first rows that have only virtual cells
    after the initial one.

    - erroneous last rows are rows that do not have a real cell as last
    cell.

    :param tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of table dictionaries.

    '''
    tables = _check_tables_and_remove_first_row_acmb(tables)
    # tables = _check_tables_and_remove_last_row_acmb(tables)
    return tables


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
