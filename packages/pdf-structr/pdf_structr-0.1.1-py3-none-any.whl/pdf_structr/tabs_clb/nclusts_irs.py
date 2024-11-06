# nclusts_irs.py
'''
NOTE: DEAD CODE; consider deleting the module

Module encapsulating the functions that try to compute inner rows (irs)
within an isolated table-like outer row.

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
# Inner row computation
#####################


def _is_vertically_overlapping_to_the_bottom(
    bbox: tuple[float, float, float, float],
    row_y1: float,
    adj_fact: float,
) -> bool:
    '''
    Test whether a bbox is overlapping vertically to the bottom with
    a row's bottom y.

    :returns: True if the overlapping.

    :param bbox: tuple[float, float, float, float]: a bbox as a 4-float tuple.

    :param row_y1: float: the current row bottom y.

    :param adj_fact: float: an adjustment factor to collate vertically close
        bboxes.

    '''
    return (bbox[3] - adj_fact <= row_y1) or ((bbox[1] - adj_fact) <= row_y1)


def _is_vertically_overlapping_to_the_top(
    bbox: tuple[float, float, float, float],
    row_y0: float,
    adj_fact: float,
) -> bool:
    '''
    Test whether a bbox is overlapping vertically to the top with a row's
    top y.

    :returns: True if the overlapping.

    :param bbox: tuple[float, float, float, float]: a bbox as a 4-float tuple.

    :param row_y0: float: the current row top y.

    :param adj_fact: float: an adjustment factor to collate vertically close
        bboxes.

    '''
    return (bbox[1] - adj_fact >= row_y0) or ((bbox[3] - adj_fact) >= row_y0)


def _compute_cell_rows(
    spans: list[dict], adj_fact: float = 0
) -> list[tuple[float, float]]:
    '''
    Compute the rows inside a cell/column by walking its spans.

    :returns: a list of 2-float tuples, where each tuple is the
        y0-y1 coordinates of a given row in the cell.

    :param spans: list[dict]
    '''
    # Sort the spans inside the cell by y1
    spans.sort(key=lambda _span: (_span['bbox'][3]))
    # Make a list of y1s; initialize it with the topmost y1
    _list_y1: list[float] = [spans[0]['bbox'][3]]
    # Walk the spans top to bottom
    for _span in spans:
        # If not overlapping vertically
        if not _is_vertically_overlapping_to_the_bottom(
            bbox=_span['bbox'],
            row_y1=_list_y1[-1],
            adj_fact=adj_fact,
        ):
            # we' got a new column
            _list_y1.append(_span['bbox'][3])

    # Make a list of y0
    # Sort the spans inside the cell by y0
    spans.sort(key=lambda _span: (_span['bbox'][1]), reverse=True)
    # Make a list of y0s; initialize it with the bottommost y0
    _list_y0: list[float] = [spans[0]['bbox'][1]]
    # Walk the spans bottom to top
    for _span in spans:
        # If not overlapping vertically
        if not _is_vertically_overlapping_to_the_top(
            bbox=_span['bbox'],
            row_y0=_list_y0[-1],
            adj_fact=adj_fact,
        ):
            _list_y0.append(_span['bbox'][1])
    # Reverse the list of y0
    _list_y0 = _list_y0[::-1]

    # Append a list of y0_y1 tuples (i.e. rows for the current cell)
    # _cells_inner_rows_coords.append(
    #     list(zip(_list_y0, _list_y1))
    # )

    return list(zip(_list_y0, _list_y1))


def _have_all_cols_same_inner_rows_count(
    cells_inner_rows_coords: list[list[tuple[float, float]]],
    row_count_in_first_cell: int,
) -> bool:
    '''
    Test whether all the columsn have the same inner rows' count.

    :param cells_inner_rows_coords: list[list[tuple[float, float]]]:
        the inner rows' y0-y1 coord for each of the inner rows of each
        of the cells/columns.

    :param row_count_in_first_cell: int: the number of rows in the first
        cell.

    '''
    return all(
        len(_inner_row_coords) == row_count_in_first_cell
        for _inner_row_coords in cells_inner_rows_coords[1:]
    )


def _make_rows_when_unique_common_inner_rows_count(
    common_inner_rows_count: int,
    cells_inner_rows_coords: list[list[tuple[float, float]]],
    table_rows_coords: list[tuple[float, float]],
) -> None:
    '''
    Computes rows at table level when all the cells have same
    inner row count.

    :param common_inner_rows_count: int: the common inner rows count
        for all the cells/columns.

    :param cells_inner_rows_coords: list[list[tuple[float, float]]]:
        the inner rows' y0-y1 coord for each of the inner rows of each
        of the cells/columns.

    :param table_rows_coords: list[tuple[float, float]]: the return list of
        table level inner rows y0-y1 coordinates.

    '''
    # Walk the y0-y1 tuples by index
    for _idx in range(0, common_inner_rows_count):
        # Make a list of y0-y1 tuples for a given position
        _y0s_y1s_at_idx: list[tuple[float, float]] = [
            _inner_row_coords[_idx]
            for _inner_row_coords in cells_inner_rows_coords
        ]
        _y0: float = min(_y0_y1_at_idx[0] for _y0_y1_at_idx in _y0s_y1s_at_idx)
        _y1: float = max(_y0_y1_at_idx[1] for _y0_y1_at_idx in _y0s_y1s_at_idx)
        table_rows_coords.append((_y0, _y1))


def _try_to_find_inner_rows_coords(
    raw_cells: list[list[dict]],
    adj_fact: float,
) -> tuple[bool, list[tuple[float, float]]]:
    '''
    Tries to identify rows in a list of lists of spans, where the
    spans are grouped by cells/columns.

    :returns: True when the algorithm has identified a unique rows' count
        for all the cells/columns and False otherwise. Also returns the
        of the identified innner row coordinates.

    :param raw_cells: list[list[dict]]: a list of lists of spans, where the
        spans are grouped by cells/columns.

    :param adj_fact: float: an adjustment factor to try and group the spans
        together when not too far apart vertically.
    '''
    # Declare a list of list of inner rows coordinates i.e. one list
    # per cell/column
    # Walk the cells and try to identify inner rows in each column
    _cells_inner_rows_coords: list[list[tuple[float, float]]] = [
        _compute_cell_rows(spans=_spans, adj_fact=adj_fact)
        for _spans in raw_cells
    ]

    # Now try to make table level rows
    _row_count_in_first_cell: int = len(_cells_inner_rows_coords[0])
    _table_rows_coords: list[tuple[float, float]] = []

    # If all the columns have the same numbers of rows
    if _have_all_cols_same_inner_rows_count(
        cells_inner_rows_coords=_cells_inner_rows_coords,
        row_count_in_first_cell=_row_count_in_first_cell,
    ):
        _make_rows_when_unique_common_inner_rows_count(
            common_inner_rows_count=_row_count_in_first_cell,
            cells_inner_rows_coords=_cells_inner_rows_coords,
            table_rows_coords=_table_rows_coords,
        )

        return True, _table_rows_coords

    return False, _table_rows_coords


def compute_table_with_inner_rows_coords(
    table: tuple[
        int,
        tuple[float, float, float, float],
        list[tuple[float, float, float, float]],
        list[list[dict]],
    ]
) -> tuple[
    int,  # index number of the row from which the table has been made
    tuple[float, float, float, float],  # table's bbox
    list[tuple[float, float, float, float]],  # table's columns bboxes
    list[tuple[float, float]],  # rows y0-y1 coords
    list[list[dict]],  # the list of spans in each of their cols
]:
    '''
    Computes the table's inner rows out of the spans in each
    cell/column.

    :returns: a table tuple to which the list of y0-y1 coords
        has been added.
    '''
    # Get the list of raw cells for the current table
    # Cells are list of spans => we have a list of lists of dict
    _raw_cells: list[list[dict]] = table[3]

    # Try to find rows by applying progressively an adjustment
    # factor to try and group spans horizontally until we
    # find a combination that results in the same number of rows
    # in each cells
    _found_rows: bool = False
    for _adj_fact in [0, 2, 4, 6]:
        if _found_rows:
            break
        _found_rows, _table_rows_coords = _try_to_find_inner_rows_coords(
            raw_cells=_raw_cells,
            adj_fact=_adj_fact,
        )

    # We do not have the same number of rows in each column
    if not _found_rows:

        # Treat the table as a single row table
        # NOTE: more advanced treatment could be tried, such
        # as the ones in extend table
        _single_row_coords: list[tuple[float, float]] = [
            (table[1][1], table[1][3])
        ]
        return *table[:3], _single_row_coords, table[-1]

    return *table[:3], _table_rows_coords, table[-1]
