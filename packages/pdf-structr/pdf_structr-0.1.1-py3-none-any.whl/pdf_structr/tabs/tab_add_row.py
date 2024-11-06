# tab__add_row.py
'''
Module encapsulating the functions adding rows to an existing table.
'''

import logging
from typing import Callable

from pdf_structr.tabs.tab_fns import (
    update_col_bbox_upon_append_or_pop_bottom_row,
    update_col_bbox_upon_prepend_or_pop_top_row,
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
# Add rows into table
#################################


def _make_table_row_dict(
    tentative_row: list[dict],
) -> dict[str, tuple[float, float, float, float] | list[dict]]:
    '''
    Once the tentative row (a list of cells) has been validated as
    acceptable to extend the table, convert it into a table row dict
    (a bbox + a list of cells).
    '''
    return {
        'bbox': (
            min(_cell['bbox'][0] for _cell in tentative_row),
            min(_cell['bbox'][1] for _cell in tentative_row),
            max(_cell['bbox'][2] for _cell in tentative_row),
            max(_cell['bbox'][3] for _cell in tentative_row),
        ),
        'cells': tentative_row,
    }


def _get_col_and_cell_bboxes(
    table,
    idx: int,
    cell: dict,
) -> tuple[
    tuple[float, float, float, float], tuple[float, float, float, float]
]:
    '''
    Get the bboxes for the current column and the current cell and returns
    them as a tuple (of tuples, since the cell's and column's bboxes
    are 4-float tuples).
    '''
    _col_bbox: tuple[float, float, float, float] = table['cols'][idx]
    _cell_bbox: tuple[float, float, float, float] = cell[
        'bbox'
    ]  # type: ignore

    return _col_bbox, _cell_bbox


def _update_table_bbox_xs_upon_adding_new_row(
    row: dict[str, tuple[float, float, float, float] | list[dict]],
    table: dict,
):
    '''
    Update the table's bbox x coordinates when adding a new row
    to the table.
    '''
    # Update the table's bbox
    table['bbox'].x0 = min(table['bbox'].x0, row['bbox'][0])
    table['bbox'].x1 = max(table['bbox'].y1, row['bbox'][2])


def _append_row_and_update_table_bbox(
    row: dict[str, tuple[float, float, float, float] | list[dict]],
    table: dict,
):
    '''
    Appends a row to the table and then update the table's bbox
    coordinates.
    '''
    # Append the row to the rows list
    table['rows'] += [row]

    # Update the table's bbox
    table['bbox'].y1 = row['bbox'][3]


def _prepend_row_and_update_table_bbox(
    row: dict[str, tuple[float, float, float, float] | list[dict]],
    table: dict,
):
    '''
    Prepend a row to the table and then update the table's bbox
    coordinates.
    '''
    # Prepend the row to the rows list
    table['rows'] = [row] + table['rows']

    # Update the table's bbox
    table['bbox'].y0 = row['bbox'][1]


def _update_cols_bboxes_upon_add_row(
    row: dict[str, tuple[float, float, float, float] | list[dict]],
    table: dict,
    column_update_fn: Callable,
) -> None:
    '''
    High-order function that updates the columns bboxes upon
    adding a new row to the table.

    row: dict[str, tuple[float, float, float, float] | list[dict]]:
        the row dictionary.

    table: dict: the current table dict.

    column_update_fn: Callable: a function to update each column, varying
        depending on whether the row has been appended or prepended.
    '''
    # Update the bboxes of the column
    # Walk the cells of the new row with enumerate and use the _idx
    # to grab the corresponding columns
    for _idx, (_cell) in enumerate(row['cells']):

        # Get the corresponding column's bbox in the table and the
        # current cell's bbox
        _col_bbox, _cell_bbox = _get_col_and_cell_bboxes(
            table, _idx, _cell  # type: ignore
        )

        # Update the column
        table['cols'][_idx] = column_update_fn(_col_bbox, _cell_bbox)


def _add_row(
    row: dict[str, tuple[float, float, float, float] | list[dict]],
    table: dict,
    add_row_and_update_table_bbox_fn: Callable,
    update_col_bbox_upon_add_row_fn: Callable,
) -> None:
    '''
    High-order function that appends or prepends a given row into a table,
    depending on the passed-in functions.

    :param row: dict[str, tuple[float, float, float, float] | list[dict]]:
        the tentative row, converted to a table row (i.e. has been added
        a 'bbox' and a 'cells' key).

    :param table: dict: the table dict to which the row shall be append
        or prepend.

    :param add_row_and_update_table_bbox_fn: Callable: a function that
        prepends or appends the row and updates the table's bbox
        accordingly.

    :param update_col_bbox_upon_add_row_fn: Callable: a function that
        updates the columns bboxes upon adding a row.

    '''
    # Add the row to the table
    add_row_and_update_table_bbox_fn(row, table)

    # Update the table's xs coordinates
    _update_table_bbox_xs_upon_adding_new_row(row, table)

    # Update the table's columns coordinates
    _update_cols_bboxes_upon_add_row(
        row, table, update_col_bbox_upon_add_row_fn  # <- beware the func
    )


def add_tentative_row(
    tentative_row: list[dict],
    table,
) -> None:
    '''
    Convert a tentative row (a list of cells) into a row dict,
    determine whether the row should be append or prepended
    and then do it.

    Returns True if a row was added and False otherwise.

    :param tentative_row: list[dict]: a list of cells passed
        as a potential new row.

    :param table: a table dict.

    '''
    # Convert the list of cells into a real row dict
    _row_dict = _make_table_row_dict(tentative_row)

    # Determine whether it should be prepended or appended
    # and configure functions to pass as arguments to
    # _add_row
    #
    # If the top of the table is higher (lower on the page)
    # than the bottom of the row, the row should be prepend.
    # Else, appended.
    if table['bbox'].y0 > _row_dict['bbox'][1]:

        add_row_and_update_table_bbox_fn = _prepend_row_and_update_table_bbox
        update_col_bbox_upon_add_row_fn = (
            update_col_bbox_upon_prepend_or_pop_top_row
        )

    else:

        add_row_and_update_table_bbox_fn = _append_row_and_update_table_bbox
        update_col_bbox_upon_add_row_fn = (
            update_col_bbox_upon_append_or_pop_bottom_row
        )

    # Do it
    _add_row(
        row=_row_dict,
        table=table,
        add_row_and_update_table_bbox_fn=add_row_and_update_table_bbox_fn,
        update_col_bbox_upon_add_row_fn=update_col_bbox_upon_add_row_fn,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
