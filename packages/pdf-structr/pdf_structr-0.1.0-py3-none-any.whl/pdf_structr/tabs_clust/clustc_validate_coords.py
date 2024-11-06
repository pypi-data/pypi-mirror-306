# clustc_validate_coords.py
'''
Module containing functions validating:
- clusters of row-like blocks: -> rlb stack
- cell-like blocks-based table candidates: clb stack

Validation carries on the overlaps:
- between successive rows;
- between successive columns.

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
# Table instance level functions
#####################


def _has_overlapping_consectv_cols_or_rows(
    cols_xs_coord: list[tuple[float, float]],
) -> bool:
    '''
    Test overlaps between consecutive columns or rows
    in a table.
    '''
    # Walk the coord tuples two by two
    for _curr_xs, _prev_xs in zip(
        cols_xs_coord[1:],
        cols_xs_coord[:-1],
    ):
        # If the current left x is lower than
        # the previous right x
        # -> overlap!
        # NOTE: consider "<=" instead of "<"
        if _curr_xs[0] < _prev_xs[1]:
            return True

    return False


def _has_overlapping_inner_rows_or_columns(
    rows_ys_coord: list[tuple[float, float]],
    cols_xs_coord: list[tuple[float, float]],
) -> bool:
    '''
    Checks whether any y1 of a given table candidate row is lower
    (higher geometrically) the y0 of the preceeding line.
    Returns True if this is the case.

    Then if there no overlapping rows, test whether there are any
    overlapping columns.

    :param rows_ys_coord: list[tuple[float, float]]: a tuple of float
        where each tuple contains the min y and max y for a row.

    :param cols_xs_coord: list[tuple[float, float]]: a tuple of float
        where each tuple contains the min x and max x for a col.

    '''
    # Test if there are any overlapping rows or columns
    return _has_overlapping_consectv_cols_or_rows(
        rows_ys_coord
    ) or _has_overlapping_consectv_cols_or_rows(cols_xs_coord)


#####################
# Table collection level functions
#####################


def validate_clb_multirow_table_candidates(
    tentative_tables_multiple_rows_coords: list[
        tuple[
            list[int],
            pymupdf.Rect,
            list[tuple[float, float]],
            list[tuple[float, float]],
        ]
    ],
) -> list[
    tuple[
        list[int],  # list of idx nbrs of included page rows
        pymupdf.Rect,  # table's bbox
        list[tuple[float, float]],  # ys coords of rows
        list[tuple[float, float]],  # xs coords of cols
    ],
]:
    '''
    Validates table candidates cell-based table candidates by
    checking that the computed rows and cols do not overlap.

    :returns: a list of 4-tuples, where each 4-tuple is a validated
        tables' candidate.
    '''
    return [
        _cluster_coords  # type: ignore
        for _cluster_coords in tentative_tables_multiple_rows_coords
        if not _has_overlapping_inner_rows_or_columns(
            rows_ys_coord=_cluster_coords[2],
            cols_xs_coord=_cluster_coords[3],
        )
    ]


def validate_table_candidates(
    block_clusters: list[list[dict[str, int | float | tuple | list]]],
    clusters_coordinates: list[
        tuple[
            pymupdf.Rect,
            list[tuple[float, float]],
            list[tuple[float, float]],
        ]
    ],
) -> tuple[
    tuple,
    tuple,
]:
    '''
    Validates the table candidates by making sure that the lines
    and columns identified for a given cluster/table do not overlap.

    :returns: a 2-tuple of tuples, where:

    - the first subtuple contains n lists of blocks (the clusters)
    - the second subtuple containes n tuples of cluster_coordinates,
    each tuple of cluster_coordinates containing the table Rectangle,
    the 2-tuples with its lines coordinates and 2-tuple with its
    cols coordinates.

    :param blocks_clusters: list[
        list[dict[str, int | float | tuple | list]]
    ]: a list of of list of blocks, where each sublist is a candidate table.

    :param clusters_coordinates:  tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ]: a list of 3-tuples, where each 3-tuple corresponds to a table
        candidate's coordinates (Rect, x0-x1 of rows, x0-x1 of columns).

    Each tuple contains:

    - a table's Rectangle
    - a list of y0-y1 coordinates of each row.
    - a list of x0-x1 coordinates of each column.

    '''
    # Get list of 2-tuples containing:
    # - a list of row-like blocks pertaining to the table
    # - a tuple of coordinates (table's Rect, rows and cols)
    _valid_table_candidates: list[
        tuple[
            list[dict[str, int | float | tuple | list]],
            tuple[
                pymupdf.Rect,
                tuple[list[float], list[tuple[float, float]]],
                tuple[list[float], list[tuple[float, float]]],
            ],
        ],
    ] = [
        (
            block_clusters[_idx],
            clusters_coordinates[_idx],  # type: ignore
        )
        for _idx, _cluster_coords in enumerate(clusters_coordinates)
        if not _has_overlapping_inner_rows_or_columns(
            rows_ys_coord=_cluster_coords[1],
            cols_xs_coord=_cluster_coords[2],
        )
    ]

    # Transform the list of 2-tuples into a tuple of tuples where:
    # - the first subtuple contains n lists of blocks (the clusters)
    # - the second subtuple containes n tuples of cluster_coordinates,
    # each tuple of cluster_coordinates containing the table Rectangle,
    # the 2-tuples with its lines coordinates and 2-tuple with its
    # cols coordinates.
    #
    # This amounts to returning the passed-in values after cleaning
    # and encapsulating into immutables. After, all, they have been
    # deemed valid.
    return tuple(zip(*_valid_table_candidates))


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
