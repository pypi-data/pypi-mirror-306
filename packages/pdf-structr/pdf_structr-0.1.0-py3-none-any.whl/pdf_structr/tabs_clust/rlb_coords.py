# clust_rlb_coords.py
'''
Encapsulating function the compute the coordinates for the horizontal
and vertical lines and the clusters' rectangles for clusters of
row-like blocks (rlb).

NOTE: the columns' coordinates computing stack is not re-usable outside
the row-like blocks approach, because it assumes that each block contains
the same number of spans and each span forms a column.

The vertical lines (i.e. tables rows) coordinates computing stack is also
quite restricted in its re-usability because it is based on the implicit
assumption that the rows are not vertically overlapping and that each
passed-in list of dicts represents a full-row in the table in making.
'''


import logging
import math
from typing import Callable

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
# Compute cluster's Rectangles
#####################


def _make_cluster_rect(
    hlines: list[float],
    vlines: list[float],
) -> pymupdf.Rect:
    '''
    At this stage, each cluster of blocks corresponds to a probable table
    and the coordinates for the columns and lines have been computed.

    For each cluster of blocks in the block_clusters list, compute a Rectangle
    (probable table rectangle).

    :param hlines: list[float]: the lists of horizontal lines y coordinates
        for a cluster.

    :param vlines: list[float]: the lists of vertical lines y coordinates
        for a cluster.
    '''

    return pymupdf.Rect(
        x0=vlines[0],
        y0=hlines[0],
        x1=vlines[-1],
        y1=hlines[-1],
    )


#####################
# Compute rows edges
#####################


def _compute_cluster_rows_one_side_edges(
    pot_rows: list[dict[str, int | float | tuple | list]],
    side: int,
    adj_factor: float = 0,
) -> list[float]:
    '''
    Commputes the rows coordinates for a cluster of blocks by making
    a list of each block's y0 or y1 as defined in the side argument (with 1
    for the y0s and 3 for the y1s).

    :returns: a list of float, where each float is either the lines y0s or y1s.

    :param pot_rows: list[dict[str, int | float | tuple | list]]: a list
        of potential rows, which need to have a 4-float tuple under the
        key 'bbox'. It may in particular be the list of blocks in a cluster,
        previously built by `make_rlb_clusters`. Implicitly, each potential
        row is supposed not to overlap with its neighbors and occupy the
        whole table space.

    :param side: int: an integer indicating the side for which the line's edges
        shall be computed. 1 for y0s and 3 for y1s.

    :param adj_factor: float: an adjustment factor to be added to the first or
        the last y in the list (to the first y if we're computing the top edges
        of the lines or the last y if we're computing the bottom edges).
        NOTE: The adjustment factor is usefully set to some value
        proportionnal to the line's height when further passing the
        returned lines to find_tables as argument to the
        add_line parameter.

        However, when using pure stabs, some lines go undetected with
        table enlargement feature.

    '''
    # Make a list of the top or bottom ys
    _lines_edges: list[float] = [
        _block['bbox'][side] for _block in pot_rows  # type: ignore
    ]

    # Add the adjustment factor to the first or last item in the list
    # side == 1: this is the list of the y0s
    if side == 1:
        # enlarge somewhat the first line downwards
        _lines_edges[0] = math.floor(_lines_edges[0])
        # _lines_edges[0] = math.floor(_lines_edges[0] - adj_factor)
    # else side == 3: this is the list of y1s
    else:
        # enlarge somewhat the last line downwards
        _lines_edges[-1] = math.ceil(_lines_edges[-1])
        # _lines_edges[-1] = math.ceil(_lines_edges[-1] + adj_factor)

    # Return the lines' edges
    return _lines_edges


def _compute_table_lines_two_side_edges(
    pot_rows: list[dict[str, int | float | tuple | list]],
) -> list[list[float]]:
    '''
    Computes top ys and bottom ys lines' edges.

    :returns a list of two lists of floats (one for the y0s and one the y1s),
        where each float is a coordinate for one of the table lines.

    :param pot_rows: list[dict[str, int | float | tuple | list]]: a list
        of potential rows, which need to have a 4-float tuple under the
        key 'bbox'. It may in particular be the list of blocks in a cluster,
        previously built by `make_rlb_clusters`. Implicitly, each potential
        row is supposed not to overlap with its neighbors and occupy the
        whole table space.

    '''
    # Make two lists (of y0s and of y1s) into a list
    return [
        _compute_cluster_rows_one_side_edges(
            pot_rows=pot_rows,
            side=_side,
        )
        # 1 and 3 represents y0 and y1 in the
        # bboxes
        for _side in [1, 3]
    ]


def _compute_cluster_line_edges(
    pot_rows: list[dict[str, int | float | tuple | list]]
) -> tuple[
    list[float],
    list[tuple[float, float]],
]:
    '''
    Computes a list of coordinates along the vertical axis for the
    horizontal row for a passed-in cluster of blocks.

    :returns: a tuple of two-lists:

    - a list of the y0s for each row + the last row's y1
    - a list of 2-float tuples, where each tuple contains the top y
        and bottom y for each table row.

    :param pot_rows: list[dict[str, int | float | tuple | list]]: a list
        of potential rows, which need to have a 4-float tuple under the
        key 'bbox'. It may in particular be the list of blocks in a cluster,
        previously built by `make_rlb_clusters`. Implicitly, each potential
        row is supposed not to overlap with its neighbors and occupy the
        whole table space.

    '''
    # Get two lists, one of the y0s and one of the y1s of each rows
    _lines_y0s_y1s_list: list[list[float]] = (
        _compute_table_lines_two_side_edges(pot_rows)
    )

    # Make a list of tuples y0-y1 for each table column
    _lines_edges_tups: list[tuple[float, float]] = list(
        zip(*(_lines_y0s_y1s_list))
    )  # type: ignore

    return (
        # The simplified list of coordinates (y0s + last line y1)
        _lines_y0s_y1s_list[0] + [_lines_y0s_y1s_list[-1][-1]],
        # The list of tuples y0-y1 for each table line
        _lines_edges_tups,
    )


#####################
# Collect x0s and x1s for to compute columns edges
#####################


def _make_list_spans_one_side_x_in_block(
    lines: list[dict],
    coord_idx_in_bbox: int,
) -> list[float]:
    '''
    Makes a list of x0s or x1s of the spans in a block.

    :param lines: list[dict]: a list of lines in a block.

    :param coord_idx_in_bbox: int: 0 for x0s or 2 for x1s.

    '''

    return [
        _span['bbox'][coord_idx_in_bbox]  # type: ignore
        for _line in lines  # type: ignore
        for _span in _line['spans']  # type: ignore
    ]


def _make_list_spans_one_side_x_per_side(
    blocks: list[dict[str, int | float | tuple | list]],
    side: int,
) -> list[list[float]]:
    '''
    From a given list of blocks, makes one list of the spans' left or right
    coord (floats) for each block in the cluster.

    returns: a list of list (per block) of the left or right coordinates of
    the spans in the blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]: a cluster
        of blocks forming together a potential table candidate.

    '''
    return [
        _make_list_spans_one_side_x_in_block(
            lines=_block['lines'],  # type: ignore
            coord_idx_in_bbox=side,
        )
        for _block in blocks
    ]


def _make_list_of_spans_x0_x1_per_blocks_cluster(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[list[list[float]]]:
    '''
    For each side left and right (designated as 0 and 2, their
    corresponding position in the bbox tuples), walk the blocks
    in the cluster, then walk the spans of each block and return
    a list of all the x0, then x1, of the spans in each block.

    Makes lists of list of each spans' x0s and x1s in each block
    of a given cluster.

    :retuns: 2-list nested in a list:

    - the first list contains lists of the x0 coordinates of all the spans
    in each block in the cluster
    - the second list contains lists of the x1 coordinates of all the spans
    in each block in the cluster

    The columns left and right edges will be computed from these lists.

    :param blocks: list[dict[str, int | float | tuple | list]]: a cluster
        of blocks forming together a potential table candidate.

    :param coord_idx_in_bbox: int: 0 for x0s or 2 for x1s.

    '''

    return [  # outer list: 2-inner lsts: (i) for the x0s and (ii) for the x1s
        _make_list_spans_one_side_x_per_side(
            blocks=blocks,
            side=_side,
        )
        # 0 and 2 represents x0 and x1 in the
        # bboxes
        for _side in [0, 2]
    ]


#####################
# Compute columns' edges
#####################


def _compute_col_side_edge_for_cluster(
    spans_side_xs_per_block_in_cluster: list[list[float]],
    col_idx: int,
    side_fn: Callable,
) -> float:
    '''
    Computes a single column right or left edge, each column being referenced
    by its idx, by returning the minimum x0 or the maximum x1 of the spans
    in the column.

    :param spans_xs_per_block_in_cluster: list[list[float]]: a list of spans'
        x0 or x1 per block in the current cluster:
        - outer list = blocks
        - inner list = spans' x0 or x1 in a block

    :param col_idx: int: the column's index number for which we're
        collecting the x coordinates.

    :param side: Callable: the function min or max. min is used if we're
        computing the left side and max for right side.

    '''

    return side_fn(
        # we select the col_idx span's x0 in the list
        # of spans for a row (block)
        _spans_side_xs_in_block[col_idx]
        for _spans_side_xs_in_block in spans_side_xs_per_block_in_cluster
    )


def _compute_col_edges_for_blocks(
    blocks: list[dict[str, int | float | tuple | list]]
) -> list[list[float]]:
    '''
    Compute the columns' edges for a given cluster in the list
    of clusters.

    :returns: a list of list of floats

    :param blocks: list[dict[str, int | float | tuple | list]]: a list of
        the blocks in a cluster.

    '''
    # Collect the spans' x0s and x1s for each block in the cluster and
    # order them as columns
    spans_xs_per_columns_in_cluster: list[list[list[float]]] = (
        _make_list_of_spans_x0_x1_per_blocks_cluster(
            blocks=blocks,
        )
    )

    # At this stage, each most inner sublist in spans_xs_per_columns_in_cluster
    # contains the SAME number of floats, each float corresponding to
    # the spans' x0s or x1s for a given block in the cluster.
    #
    # NOTE: The preceeding statement is true only because in the
    # row-like blocks based approach, we consider a block to be a row
    # and to contain the same number of spans.
    #
    # => Get this number: this is the columns count: here, we get it
    # from the first block's list of spans' x0s
    _cols_count: int = len(spans_xs_per_columns_in_cluster[0][0])

    # Now, for each column (range(0, _cols_count)), get the smallest x0
    # or the largest x1 of all the spans in the column
    # -> this will be the column's left and right edges
    _list_cols_left_edges: list[list[float]] = [
        [
            _compute_col_side_edge_for_cluster(
                spans_side_xs_per_block_in_cluster=(
                    _spans_side_xs_per_column_in_cluster
                ),
                col_idx=_idx,
                side_fn=_side_fn,
            )
            # for each column
            for _idx in range(0, _cols_count)
        ]
        # for each side (x0 and x1)
        for _side_fn, _spans_side_xs_per_column_in_cluster in zip(
            (
                min,
                max,
            ),
            spans_xs_per_columns_in_cluster,
        )
    ]

    return _list_cols_left_edges


def compute_blocks_col_edges(
    blocks: list[dict[str, int | float | tuple | list]]
) -> tuple[list[float], list[tuple[float, float]]]:
    '''
    Commputes the vertical line coordinates for a cluster of blocks
    by computing the min value for all the spans' x0s in a given
    column (across successive blocks) and max value for all the spans' x0s
    in a given column,

    :returns: a tuple of two-lists:

    - a list of the x0s for each col + the last col's x1
    - a list of 2-float tuples, where each tuple contains the left x
        and right x for each table col.

    :param blocks: list[dict[str, int | float | tuple | list]]: a list of
        the blocks in a cluster.

    '''

    # Compute the min x0s and max x1s of all the spans in each columns
    _cols_x0s_x1s_list: list[list[float]] = _compute_col_edges_for_blocks(
        blocks
    )

    # Make a list of one 2-float tuple x0-x1 for each table column
    _cols_edges_tups: list[tuple[float, float]] = list(
        zip(*(_cols_x0s_x1s_list))
    )  # type: ignore

    return (
        # A simplified list of coordinates (x0s + last col x1)
        # for each column
        _cols_x0s_x1s_list[0] + [_cols_x0s_x1s_list[-1][-1]],
        # The list of 2-float tuples y0-y1 for each table column
        _cols_edges_tups,
    )


#####################
# Compute cluster Rect and lines and columns edges
#####################


def _compute_cluster_rect_and_lines_cols_edges(
    block_cluster: list[dict[str, int | float | tuple | list]],
) -> tuple[
    pymupdf.Rect,
    list[tuple[float, float]],
    list[tuple[float, float]],
]:
    '''
    For a given cluster, computes the lines and columns edges
    then computes the Rectangle for the cluster and returns
    the three values.

    :returns: a 3-tuples containing:

    - a table's Rectangle
    - a list of y0-y1 coordinates of each line.
    - a list of x0-x1 coordinates of each line.

    :param block_cluster: list[dict[str, int | float | tuple | list]]:
        a list of the blocks in a cluster.
    '''
    # The computation of the table rows' edges is made at the blocks
    # level, since blocks are supposed to be row-like blocks
    _trows_edges: tuple[list[float], list[tuple[float, float]]] = (
        _compute_cluster_line_edges(block_cluster)
    )
    # The computation of the table rows' edges is made at the spans
    # level. Since the blocks are supposed to row-like blocks, they
    # do not give a lot of indication on columns by themselves
    _cols_edges: tuple[list[float], list[tuple[float, float]]] = (
        compute_blocks_col_edges(block_cluster)
    )
    # The table Rect is infered from the computations of the _trows_edges
    # and the _cols_edges
    _rect: pymupdf.Rect = _make_cluster_rect(_trows_edges[0], _cols_edges[0])

    return _rect, _trows_edges[1], _cols_edges[1]


#####################
# Main API
#####################


def compute_clusters_coordinates(
    blocks_clusters: list[list[dict[str, int | float | tuple | list]]],
) -> list[
    tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ]
]:
    '''
    Computes Rectangles for each blocks_cluster and list lines and rows
    coordinates for each line and row in each cluster and returns
    them.

    :returns: a list of 3-tuples, where each tuple corresponds to a table
        candidate.

    Each tuple contains:

    - a table's Rectangle
    - a list of y0-y1 coordinates of each line.
    - a list of x0-x1 coordinates of each line.

    :param blocks_clusters: list[
        list[dict[str, int | float | tuple | list]]
    ]: a list of list of blocks, where each sublist gather a series of
        row-like blocks and forms a candidate table.

    '''
    # Compute table's edges as well as line and columns coordinates
    return [
        _compute_cluster_rect_and_lines_cols_edges(
            block_cluster=_block_cluster
        )
        for _block_cluster in blocks_clusters
    ]


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
