# coords.py
'''
Module encapsulating the functions computing the coordinates
of rows of cell-like blocks and the coordinates of multirows
tables (bboxes, rows xs coords and cols xs coords)

'''

import logging

import pymupdf  # type: ignore

from pdf_structr.tabs_clust.clustc_validate_coords import (
    validate_clb_multirow_table_candidates,
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
# Flatten spans in row
#####################


def _flatten_spans_in_blocks(
    blocks: list[dict],
) -> list[dict]:
    '''
    Flattens the spans in a list of blocks.

    :param blocks: list[dict]: a list of text blocks.
    '''
    return [
        _span
        for _block in blocks
        for _line in _block['lines']
        for _span in _line['spans']
    ]


def _flatten_spans_in_rows(_rows: list[tuple[int, list[dict]]]) -> list[tuple]:
    '''
    Flattens the spans in the blocks of a row into a single list
    of spans.

    :returns: the passed-in list of rows, where the last elements of each
        of the passed-in tuples is still a flat list of the spans it contains,
        but made of spans instead of blocks.

    :param _rows: list[tuple[int, list[dict]]]: the basic rows before
        any treatment.
    '''
    return [
        (
            _idx,
            _flatten_spans_in_blocks(_blocks),
        )
        for _idx, _blocks in _rows
    ]


#####################
# Compute rows bboxes
#####################


def _compute_row_bbox(blocks: list[dict]) -> tuple[float, float, float, float]:
    '''
    Computes and return the bbox for a list of blocks as a 4-float tuple.
    '''
    return (
        min(_block['bbox'][0] for _block in blocks),
        min(_block['bbox'][1] for _block in blocks),
        max(_block['bbox'][2] for _block in blocks),
        max(_block['bbox'][3] for _block in blocks),
    )


def _compute_rows_bboxes(
    rows: list[tuple[int, list[dict]]]
) -> list[tuple[int, tuple[float, float, float, float], list[dict]]]:
    '''
    Compute the rows bboxes.

    :param rows: list[tuple[int, list[dict]]]: the list of rows tuple, where
        each tuple has an index number and a list of blocks.
    '''
    return [
        (
            _idx,
            _compute_row_bbox(_blocks),
            _blocks,
        )
        for _idx, _blocks in rows
    ]


#####################
# Determine columns coordinates
#####################


def _overlapping_any_span(
    x_coord: float,
    spans: list[dict[str, tuple[float, float, float, float]]],
) -> bool:
    '''
    Test if the x_coord (the potential right x or left x coord of the
    edge of a column) overlaps with any of the passed-in spans.

    Will return True if this x_coord overlaps any spans. Else returns False
    (False means that the coordinate does not overlap with any span).

    Because we use the strictly superior, testing the x_coord against
    the span it comes from will always return False => does not overlap
    with itself.

    IMPORTANT: Do not use any rounding, or the test will be biaised.

    '''
    return any(
        # always use strictly superior with any(), never `<=`
        (_span['bbox'][0] < x_coord < _span['bbox'][2])
        for _span in spans
    )


def _are_cols_too_close_to_each_other(
    cols_left_edge_x_coords: list[float],
    cols_right_edge_x_coords: list[float],
    idx: int,
    ref_x_gap: float = 1.0,
) -> bool:
    '''
    Test whether two columns are closer to each other than the
    reference x-gap and return True or False.
    '''
    if (
        cols_left_edge_x_coords[idx + 1] - cols_right_edge_x_coords[idx]
    ) < ref_x_gap:  # x gap between the columns; to be dynamically computed
        return True
    else:
        return False


def _is_single_column(
    cols_left_edge_x_coords_count: int,
    cols_right_edge_x_coords_count: int,
) -> bool:
    '''
    Test whether the side edge x coordinates for potential column
    candidates form one single column.

    :param cols_left_edge_x_coords_count: int: the left x coordinates
        count for potential columns.

    :param cols_right_edge_x_coords_count: int: the right x coordinates
        count for potential columns.

    '''
    # Not the same count of edges -> one single column here
    if cols_left_edge_x_coords_count != cols_right_edge_x_coords_count:
        return True

    # Only one item in each list -> one single column here
    if cols_left_edge_x_coords_count == 1:
        return True

    return False


def _merge_columns_acmb(
    cols_left_edge_x_coords: list[float],
    cols_right_edge_x_coords: list[float],
) -> list[tuple[float, float]]:
    '''
    Parses both lists of coordinates simultaneously,
    compare the current right x with the following left x,
    if above the reference x_gap, keeps both coordinates,
    converts the resulting filtered list of coordinates into
    2-float tuples corresponding to x0 x1 coordinates
    of each columns.

    :param cols_left_edge_x_coords: list[float]: the list of
        columns' left edge x coordinates, sorted in ascending order.

    :param cols_right_edge_x_coords: list[float]: the list of
        columns' right edge x coordinates, sorted in ascending order.

    '''
    # Declare two new list of floats that will store the valid
    # coordinates
    _nleft_coords: list[float] = [cols_left_edge_x_coords[0]]
    _nright_coords: list[float] = []

    # Walk the two list simultaneously to compare this current right x
    # with the next left x
    for _next_left, _curr_right in zip(
        cols_left_edge_x_coords[1:],
        cols_right_edge_x_coords[:-1],
    ):
        # If the space between the columns is above the thresholds,
        # keep the current right x and the next left x
        if (_next_left - _curr_right) > 1:
            _nleft_coords += [_next_left]
            _nright_coords += [_curr_right]

    # Append the last x right coordinate
    _nright_coords += [cols_right_edge_x_coords[-1]]

    return list(zip(_nleft_coords, _nright_coords))


def _make_columns(
    cols_left_edge_x_coords: list[float],
    cols_right_edge_x_coords: list[float],
) -> list[tuple[float, float]]:
    '''
    Make columns by joining the left x and right x into a tuples.

    Merges columns that are very close to one another.

    :param cols_left_edge_x_coords: list[float]: the list of
        columns' left edge x coordinates, sorted in ascending order.

    :param cols_right_edge_x_coords: list[float]: the list of
        columns' right edge x coordinates, sorted in ascending order.

    '''
    # If we have only one column -> return a list with one single
    # 2-float tuple, with the leftmost and rightmost xs
    if _is_single_column(
        len(cols_left_edge_x_coords),
        len(cols_right_edge_x_coords),
    ):
        return [
            (
                cols_left_edge_x_coords[0],
                cols_right_edge_x_coords[-1],
            )
        ]

    # Merge columns that are very close to one another
    return _merge_columns_acmb(
        cols_left_edge_x_coords=cols_left_edge_x_coords,
        cols_right_edge_x_coords=cols_right_edge_x_coords,
    )


def _make_list_side_edges_coords(
    spans: list[dict[str, tuple[float, float, float, float]]],
    side: int,
) -> list[float]:
    '''
    Makes a list of column edges on one side (left or right)
    by taking all the spans' left or right edges and checking
    if they overlap with any span and keeping only those that do
    not overlap.

    :param spans: list[dict[str, tuple[float, float, float, float]]]:
        the list of spans in which we're trying to find column's edges.

    :param side: int: the side for which we're trying to compute
        the columns' edges. Used to select the correct float in the
        4-float bbox tuples. 0 for left and 2 for right.

    '''
    # Get a list of all the left x or right x coordinates for all the spans
    _cols_side_edge_x_coords: list[float] = [
        _span['bbox'][side] for _span in spans
    ]

    # Keep only the x coordinates that do not overlap with any other span
    _cols_side_edge_x_coords = [
        _side_x
        for _side_x in _cols_side_edge_x_coords
        if not _overlapping_any_span(
            _side_x,
            spans,
        )
    ]

    # Delete duplicates
    _cols_side_edge_x_coords = list(set(_cols_side_edge_x_coords))

    # Sort the list
    _cols_side_edge_x_coords.sort()

    return _cols_side_edge_x_coords


def _append_col_coords_to_row(
    row: tuple[int, tuple[float, float, float, float], list[dict]],
) -> tuple[
    int,
    tuple[float, float, float, float],
    list[tuple[float, float]],
    list[dict],
]:
    '''
    Computes the columns' coordinates for a given row.

    :returns: a list of 3-tuples corresponding to rows of blocks, where
        each tuple contains:

    - an index number
    - the row's bbox
    - a list of the block's columns x coordinates (x0 and x1)
    - a list of the spans (extracted from the blocks) in the row

    :param row: tuple[int, tuple[float, float, float, float], list[dict]]: a
        3-tuple row index - row bbox - list of spans contained in
        the row.
    '''
    # Get the list of spans in the row
    _spans: list[dict] = row[2]

    # -----------------------------
    # Right edges
    # -----------------------------

    _cols_right_edge_x_coords: list[float] = _make_list_side_edges_coords(
        _spans, 2
    )

    # -----------------------------
    # Left edges
    # -----------------------------

    _cols_left_edge_x_coords: list[float] = _make_list_side_edges_coords(
        _spans, 0
    )

    # -----------------------------
    # Columns
    # -----------------------------

    _cols_coords: list[tuple[float, float]] = _make_columns(
        _cols_left_edge_x_coords,
        _cols_right_edge_x_coords,
    )

    # Append the list of columns' edge to the row tuple
    return (
        row[0],  # index number
        row[1],  # row's bbox
        # list of columns left and right edges
        # # Zip left and right edges into a single list of tuples
        # list(zip(_cols_left_edge_x_coords, _cols_right_edge_x_coords)),
        _cols_coords,
        row[2],  # list of spans for the current row
    )


def _append_col_coords_to_rows(
    rows: list[tuple[int, tuple[float, float, float, float], list[dict]]],
) -> list[
    tuple[
        int,
        tuple[float, float, float, float],
        list[tuple[float, float]],
        list[dict],
    ],
]:
    '''
    Computes the columns' coordinates for all the rows.

    :returns: a list of 4-tuples corresponding to rows of blocks, where
        each tuple contains:

    - an index number
    - the row's bbox
    - a list of column's x coordinates (x0 and x1)
    - a list of the spans (extracted from the blocks) in the row

    :param rows: list[
        tuple[int, tuple[float, float, float, float], list[dict]]
    ]: a list of 3-tuple row index - row bbox - list of spans contained in
        the row.
    '''
    return [_append_col_coords_to_row(row=_row) for _row in rows]


#####################
# Main API to compute rows coordinates (bbox and columns)
#####################


def flatten_blocks_to_spans_and_compute_prows_coords(
    rows: list[tuple[int, list[dict]]],
) -> list[
    tuple[
        int,  # index number of the row
        tuple[float, float, float, float],  # its bbox
        list[tuple[float, float]],  # list of columns' x0 and x1
        list[dict],  # list of spans
    ],
]:
    '''
    Computes the coordinates of page level rows:

    - rows' bboxes
    - inside each row, its columns' x0 and x1

    Flattens the blocks contained in a row into a list of spans.

    :param rows: list[tuple[int, list[dict]]]: a list of rows, where each
        row is a 2-tuple:

        - index number
        - list of blocks
    '''
    # 0. Flatten the spans in the rows
    _rows_with_flattened_spans: list[tuple[int, list[dict]]] = (
        _flatten_spans_in_rows(rows)
    )

    # 1. Compute rows' bbox
    _rows_with_bboxes: list[
        tuple[int, tuple[float, float, float, float], list[dict]]
    ] = _compute_rows_bboxes(_rows_with_flattened_spans)

    # 2. Compute the columns' coordinates for each row
    _rows_with_col_coords: list[
        tuple[
            int,  # index number of the row
            tuple[float, float, float, float],  # its bbox
            list[tuple[float, float]],  # list of columns' x0 and x1
            list[dict],  # list of spans
        ],
    ] = _append_col_coords_to_rows(_rows_with_bboxes)

    # Return the rows with columns' coordinates and bboxes
    return _rows_with_col_coords


#####################
# Multirow table coordinates
#####################


def _get_columns_coordinates_for_table(
    tent_table: list[
        # Each tuple is one of the rows in the multi-row table
        tuple[
            int,  # idx num
            tuple[float, float, float, float],  # row bbox
            list[tuple[float, float]],  # cols x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ]
    ]
) -> list[tuple[float, float]]:
    '''
    Computes the table's columns coordinates from the
    passed-in table's coordinates.
    '''
    # Make a list of list of all the x0-x1 tuples per row
    _tent_cols_coords: list[list[tuple[float, float]]] = [
        list(_row[2]) for _row in tent_table
    ]

    # Transpose to a list of all the x0-x1 tuples per column
    _tent_cols_coords = list(zip(*_tent_cols_coords))  # type: ignore

    # Now we have the x0-x1 tuples ordered by columns
    # We just need to take the min and the max for each col

    _tent_cols_coord: list[tuple[float, float]] = [
        (
            min(_tup[0] for _tup in _cols),
            max(_tup[1] for _tup in _cols),
        )
        for _cols in _tent_cols_coords
    ]

    return _tent_cols_coord


def _get_tentative_table_coordinates(
    tent_table: list[
        # Each tuple is one of the rows in the multi-row table
        tuple[
            int,  # idx num
            tuple[float, float, float, float],  # row bbox
            list[tuple[float, float]],  # cols x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ]
    ]
) -> tuple[
    list[int],
    pymupdf.Rect,  # the table's bbox
    list[tuple[float, float]],  # the rows' y coordinates
    list[tuple[float, float]],  # the cols x coordinates
]:
    '''
    Computes a tentative multirow table's coordinates (bbox, rows ys coords and
    cols xs coords).

    :param tent_table: list[
        tuple[
            int,  # idx num
            tuple[float, float, float, float],  # row bbox
            list[tuple[float, float]],  # cols x0 and x1
            list[list[dict]],  # list of spans grouped by cells
        ]
    ]: a table candidate, containing a list of row tuples.

    '''
    # With the ys for the rows, we can be pretty sure that we are
    # in the correct order since the rows in the table
    # are made of significant whitespace separated rows which have
    # been created from top to bottom.

    # Declare list of ys coord
    # walk the rows and get the y coord in the rows bboxes
    _rows_ys_coord: list[tuple[float, float]] = [
        (
            _row[1][1],
            _row[1][3],
        )
        for _row in tent_table
    ]

    # With the xs for the colums, we need to go into each row,
    # get each of the columns/cells bboxes coordinates, then
    # compute the max and the min for each of the member
    # of the tuples

    # Declare list of xs coord
    _cols_xs_coord: list[tuple] = _get_columns_coordinates_for_table(
        tent_table=tent_table,
    )

    # Compute the table bbox
    _table_bbox: pymupdf.Rect = pymupdf.Rect(
        _rows_ys_coord[0][0],
        _cols_xs_coord[0][0],
        _rows_ys_coord[-1][-1],
        _cols_xs_coord[-1][-1],
    )

    return (
        [_row[0] for _row in tent_table],
        _table_bbox,
        _rows_ys_coord,
        _cols_xs_coord,
    )


def get_tentative_tables_multiple_rows_coords(
    tentative_tables_multiple_rows: list[
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
    ]
) -> list[
    tuple[
        list[int],  # the index numbrs of the rows in the table
        pymupdf.Rect,  # the table's bbox
        list[tuple[float, float]],  # the rows' y coordinates
        list[tuple[float, float]],  # the cols x coordinates
    ]
]:
    '''
    Computes and returns the coordinates for tables made out
    multi-rows of cells-like blocks (bbox, rows' ys coord and
    cols's xs coords).

    :returns: list[
        tuple[
            list[int],
            pymupdf.Rect,  # the table's bbox
            list[tuple[float, float]],  # the rows' y coordinates
            list[tuple[float, float]],  # the cols x coordinates
        ]
    ]: a list of tuple, where each tuple groups, for a table candidate,
        its bbox, rows' ys coord and cols's xs coords.

    :param tentative_tables_multiple_rows: list[
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
    ]: a very basic list of tentative_tables_multiple_rows under the form of
        a list of list of rows, where each row is a tuple with (i) its index
        number, (ii) a row's bbox, (iii) a list of 2-tuples float corresp.
        to x0 and x1 and (iv) a list of the spans in the row.

    '''
    _tentative_tables: list[
        tuple[
            list[int],
            pymupdf.Rect,  # the table's bbox
            list[tuple[float, float]],  # the rows' y coordinates
            list[tuple[float, float]],  # the cols x coordinates
        ]
    ] = [
        _get_tentative_table_coordinates(_tent_table)
        for _tent_table in tentative_tables_multiple_rows
    ]

    return validate_clb_multirow_table_candidates(
        tentative_tables_multiple_rows_coords=_tentative_tables
    )
    # # 1. Compute y0 y1 tuples for rows
    # for _tent_table in tentative_tables_multiple_rows:

    #     _table_rect: pymupdf.Rect
    #     for _row in _tent_table:
    #         _tent_table[1]
    # # 1. Compute tables' Rectangles
    # for _tent_table in tentative_tables_multiple_rows:
    #     _table_rect: pymupdf.Rect
    #     for _row in _tent_table:
    #         _tent_table[1]
    # # 3. Compute x0 x1 tuples for cols
    # pass


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
