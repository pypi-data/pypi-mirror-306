# tab_fns.py
'''
Module storing functions providing simili-methods to table dicts.
'''


import logging
import statistics

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
# Assess whether a cell is a virtual cell
#####################


def is_virtual_cell(cell: dict) -> bool:
    _spans_in_cell: int = len(cell['spans'])

    if _spans_in_cell > 1:
        return False

    _span: dict = cell['spans'][0]

    if (_span['bbox'][0] == _span['bbox'][2]) and (
        _span['bbox'][1] == _span['bbox'][3]
    ):
        return True

    return False


#####################
# Remove row
#####################


def pop_first_row(
    table: dict,
) -> None:
    '''
    Pops the first row and then update the table's bbox y0 coordinate.
    '''
    # Prepend the row to the rows list
    table['rows'] = table['rows'][1:]

    # Update the table's bbox y0 with the new first row's y0
    table['bbox'].y0 = table['rows'][0]['bbox'][1]


def pop_last_row(
    table: dict,
) -> None:
    '''
    Pops the first row and then update the table's bbox y0 coordinate.
    '''
    # Prepend the row to the rows list
    table['rows'] = table['rows'][1:]

    # Update the table's bbox y1 with the last first row's y1
    table['bbox'].y1 = table['rows'][0]['bbox'][3]


#####################
# Recompute columns upon change in rows
#####################


def update_col_bbox_upon_append_or_pop_bottom_row(
    col_bbox: tuple[float, float, float, float],
    cell_bbox: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    '''
    Recomputes a given column's bbox upon appending a new row.
    '''
    return (
        min(col_bbox[0], cell_bbox[0]),
        col_bbox[1],  # the y0 remains the same
        max(col_bbox[2], cell_bbox[2]),
        cell_bbox[3],
    )


def update_col_bbox_upon_prepend_or_pop_top_row(
    col_bbox: tuple[float, float, float, float],
    cell_bbox: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    '''
    Recomputes a given column's bbox upon prepending a new row.
    '''
    return (
        min(col_bbox[0], cell_bbox[0]),
        cell_bbox[1],
        max(col_bbox[2], cell_bbox[2]),
        col_bbox[3],  # the y1 remains the same
    )


#####################
# Recompute columns
#####################


def recompute_columns(
    table: dict,
) -> None:
    '''
    Recomputes the columns from the cells in the rows.

    Used mainly when removing a row.

    When adding a row, the computation is made by comparing
    each of the cells in the row with the existing columns'
    bboxes.

    :param table: dict: the current table's dict.
    '''
    # Walk the columsn by index
    for _idx in range(0, len(table['cols'])):

        # Get min x0 for all the cells in this column
        _left_x: float = min(
            _row['cells'][_idx]['bbox'][0] for _row in table['rows']
        )
        # Get max x1 for all the cells in this column
        _right_x: float = max(
            _row['cells'][_idx]['bbox'][2] for _row in table['rows']
        )

        # Update the column's bbox
        table['cols'][_idx] = (
            _left_x,
            table['bbox'].y0,
            _right_x,
            table['bbox'].y1,
        )


#####################
# Compute table rows reference y gap
#####################


def compute_rows_ref_y_gap(
    table: dict,
):
    '''
    For a given table, computes the reference y0 gap between rows.
    '''
    # Get the list of row coordinate tuples
    _row_coords: list[tuple[float, float]] = [
        (
            _row['bbox'][1],
            _row['bbox'][3],
        )
        for _row in table['rows']
    ]

    # Compute the rows y0 reference gap
    #
    # Make a list of rows y0 gaps
    _rows_y0_gaps: list[float] = [
        (round(_next_row_ys[0]) - round(_curr_row_ys[0]))
        for _curr_row_ys, _next_row_ys, in zip(
            _row_coords[:-1],
            _row_coords[1:],
        )
    ]
    # Get the mode of rows y0 gaps
    _mode_rows_y0_gaps: float = statistics.mode(_rows_y0_gaps)
    # Compute the mode relevancy
    _mode_rel_rows_y0_gaps: float = sum(1 for _row_coord in _row_coords) / len(
        _row_coords
    )

    # take the mode if the mode is more than 40% of the gaps
    if _mode_rel_rows_y0_gaps > 0.4:
        table['ref_y0_gap'] = _mode_rows_y0_gaps

    else:
        # take the average
        table['ref_y0_gap'] = statistics.mean(_rows_y0_gaps)


#####################
# Compute columns maximum left and right extension limits
#####################


def _compute_col_max_extension_limit(
    curr_col_bbox: tuple[float, float, float, float],
    next_col_bbox: tuple[float, float, float, float],
    left_ext_coord: float,
    max_ext: list[tuple[float, float]],
    idx: int,
) -> float:
    '''
    For a given column in the table (column passed-in as curr_col_bbox),
    compute the maximum acceptable extension coordinates (on the horizontal
    axis).

    :param curr_col_bbox: tuple[float, float, float, float]: the current
        bbox as a 4-float tuple.

    :param next_col_bbox: tuple[float, float, float, float]: the next
        bbox as a 4-float tuple.

    :param left_ext_coord: float: the maximum extension to the left.

    :param max_ext: list[tuple[float, float]]: the list of 2-float tuples
        where each element in the list is a column and the two floats
        are the right and left coordinates of the maximum possible
        extension on each side.

    :param idx: int: the index of the current iteration on the columns.

    '''

    # Get the right maximum extension
    _right_ext_coord: float = next_col_bbox[0]

    # If we are on the first column, set the left maximum extension to the
    # same size as right one
    if idx == 0:
        left_ext_coord = curr_col_bbox[0] - (
            _right_ext_coord - curr_col_bbox[2]
        )

    # Append the tuple of max extensions to the list
    max_ext.append(
        (
            left_ext_coord,
            _right_ext_coord,
        )
    )

    # Reset the maximumn left extension for next iteration to
    # the current column right x
    return curr_col_bbox[2]


def compute_cols_max_extension_limits(
    cols: list[tuple[float, float, float, float]],
) -> list[tuple[float, float]]:
    '''
    For a list of columns, compute the maximum right and left extensions
    limits coordinates for each one and returns them as a list of 2-float
    tuples, where the left float is the left coordinate's maximum
    extension limit and the right one is the right coordinate's
    maximum extension limit (on the horizontal axis).

    :param cols: list[tuple[float, float, float, float]]: a list of
        columns' bboxes.
    '''
    _max_ext: list[tuple[float, float]] = []

    _left_ext_coord: float = 0

    # Walk the columns two by two and fill in the _max_ext list with
    # 2-float tuples (left and right extension for the current column)
    for _idx, (_curr_col_bbox, _next_col_bbox) in enumerate(
        zip(cols[:-1], cols[1:])
    ):

        _left_ext_coord = _compute_col_max_extension_limit(
            curr_col_bbox=_curr_col_bbox,
            next_col_bbox=_next_col_bbox,
            left_ext_coord=_left_ext_coord,
            max_ext=_max_ext,
            idx=_idx,
        )

    # Compute and append the 2-float extension tuple for the last column
    _max_ext.append(
        (
            _left_ext_coord,
            cols[-1][2]  # type: ignore
            + (cols[-1][0] - _left_ext_coord),  # type: ignore
        )
    )

    return _max_ext


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
