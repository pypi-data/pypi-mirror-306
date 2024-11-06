# _ftf_coords.py
'''
Encapsulating function the compute the coordinates for the horizontal
and vertical lines and the clusters' rectangles.

IMPORTANT: modules with `ftf` in their names are parts of the interface
from to stabs to pymupdf.TableFinder.

'''


import logging
from typing import Any, Generator

import pymupdf  # type: ignore

from pdf_structr.tabs_clust.rlb_coords import (
    _compute_cluster_line_edges,
    _make_cluster_rect,
    compute_blocks_col_edges,
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
# NOTE: OLD CODE: To be refactored or deleted alltogether
#####################


def _compute_clusters_rect(
    horizlines_ys_per_clusters: Generator[list[float], Any, Any],
    vertlines_xs_per_clusters: Generator[list[float], Any, Any],
) -> list[pymupdf.Rect]:
    '''
    At this stage, each cluster of blocks corresponds to a probably table
    and the coordinates for the columns and lines have been computed.

    For each cluster of blocks in the block_clusters list, compute a Rectangle
    (probable table rectangle).

    :param horizlines_ys_per_clusters:Generator[list[float], Any, Any]: the
        lists of horizontal lines y coordinates for each block's clusters.

    :param vertlines_xs_per_clusters: Generator[list[float], Any, Any]: the
        lists of vertical lines x coordinates for each block's clusters.
    '''

    return [
        _make_cluster_rect(
            hlines=_hlines_per_cluster,
            vlines=_vlines_per_cluster,
        )
        for _hlines_per_cluster, _vlines_per_cluster in zip(
            horizlines_ys_per_clusters,
            vertlines_xs_per_clusters,
        )
    ]


def _compute_horizlines_ys_clusters_level(
    block_clusters: list[list[dict[str, int | float | tuple | list]]],
) -> Generator[list[float], Any, Any]:
    '''
    At this stage, each cluster of blocks corresponds to a probable table.

    For each cluster of blocks in the block_clusters list, compute a list
    of lines (based on the blocks y1).

    :param block_clusters: list[list[dict[str, int | float | tuple | list]]]:
        the list of blocks' clusters previously built by `make_block_clusters`.

    '''

    return (
        _compute_cluster_line_edges(_block_cluster)
        for _block_cluster in block_clusters
    )


def _compute_vertlines_xs_clusters_level(
    block_clusters: list[list[dict[str, int | float | tuple | list]]],
) -> Generator[list[float], Any, Any]:
    '''
    Compute the columns' left edges coord for every clusters in the list
    of block_clusters then computes the right most edge for each cluster
    and appends it to the column's coordinates.

    :param block_clusters: list[list[dict[str, int | float | tuple | list]]]:
        the list of blocks' clusters previously built by `make_block_clusters`.

    '''
    return (compute_blocks_col_edges(_cluster) for _cluster in block_clusters)


#####################
# Compute lines for `pdf_struct.table.find_tables()` `add_lines` parameter
#####################


def _compute_lines(
    cluster_rects: list[pymupdf.Rect],
    horizlines_ys_per_clusters: Generator[list[float]],
    vertlines_xs_per_clusters: Generator[list[float]],
) -> list[list[tuple[pymupdf.Point, pymupdf.Point]]]:
    '''
    From the lists of y coordinates for the lines' edges of each table
    candidate and the lists of x coordinates for column's edges of each
    table candidate as well as the cluster rectangles for each table
    candidate, computes lines as pairs of point_like objects to be passed as
    additional virtual vector graphics as argument to the add_lines parameters
    of function `find_tables`.

    :returns: a list of lists of 2-tuples of points, where each 2-tuples
        is a line and each list of 2-tuples is a group of lines corresponding
        to a cluster (a table candidate).

    :param cluster_rects: list[pymupdf.Rect]: the list of Rectangles
        for the clusters (table candidates) identified in the page.

    :param horizlines_ys_per_clusters: list[list[float]]: the list of
        y coordinates for the lines' edges of each table candidate identified
        in the page.

    :param vertlines_xs_per_clusters: list[list[float]]: the list of
        x coordinates for the columns' edges of each table candidate identified
        in the page.

    '''
    _lines_per_clusters: list = [
        # the list of horizontal lines
        [
            (
                pymupdf.Point(_cluster_rect.x0, _horizline_y),
                pymupdf.Point(_cluster_rect.x1, _horizline_y),
            )
            for _horizline_y in _horizlines_ys_for_cluster
        ]
        # the list of vertical lines
        + [
            (
                pymupdf.Point(_cluster_rect.y0, _vertline_x),
                pymupdf.Point(_cluster_rect.y1, _vertline_x),
            )
            for _vertline_x in _vertlines_xs_for_cluster
        ]
        for (
            _cluster_rect,
            _horizlines_ys_for_cluster,
            _vertlines_xs_for_cluster,
        ) in zip(
            cluster_rects,
            horizlines_ys_per_clusters,
            vertlines_xs_per_clusters,
        )
    ]

    return _lines_per_clusters


#####################
# Higher-level API
#####################


def _compute_tables_rect_and_lines_coord(
    block_clusters: list[list[dict[str, int | float | tuple | list]]],
) -> tuple[list[pymupdf.Rect], tuple[Generator, Generator]]:
    '''
    First computes each cluster's horizontal and vertical lines, then
    computes the bboxes as Rectangles.

    :returns: a two tuple, where the first element is a list of cluster/table
        rectangles and the second one is a tuple of lists of their horizontal
        and vertical lines.

    :param block_clusters: list[list[dict[str, int | float | tuple | list]]]:
        the list of blocks' clusters previously built by `make_block_clusters`.

    '''
    _horizlines_ys_per_clusters: Generator[list[float], Any, Any] = (
        _compute_horizlines_ys_clusters_level(block_clusters)
    )
    _vertlines_xs_per_clusters: Generator[list[float], Any, Any] = (
        _compute_vertlines_xs_clusters_level(block_clusters)
    )

    # _cluster_rects = _compute_clusters_rect(_block_clusters)
    _cluster_rects: list[pymupdf.Rect] = _compute_clusters_rect(
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
    )

    return (
        _cluster_rects,
        (_horizlines_ys_per_clusters, _vertlines_xs_per_clusters),
    )


def compute_lines_and_rects_per_clusters(
    block_clusters: list[list[dict[str, int | float | tuple | list]]]
):
    '''
    For each cluster (i.e. probable table), compute:
    - the horizontal lines
    - the vertical lines
    - the cluster's rectangles
    - the lines as a list of 2-tuples (Point, Point)

    :returns: a 4-tuple of lists:
    - one list of list of floats, corresponding to the y coordinates of the
      lines for each table candidate
    - one list of list of floats, corresponding to the x coordinates of the
      lines for each table candidate
    - one list of list of lines (represented as a 2-tuple of Points), both
      horizontal and vertical, for each table candidate
    - one list of Rect, corresponding to the bboxes of the table candidates

    These will be used by the `find_tables()` function to try and
    identify tables.

    :param block_clusters: list[list[dict[str, int | float | tuple | list]]]:
        the list of blocks' clusters previously built by `make_block_clusters`.

    '''
    # For each cluster of blocks, compute the cluster's horizontal and vertical
    # lines and the corresponding Rectangle for the cluster (candidate table).
    (
        _cluster_rects,
        (_horizlines_ys_per_clusters, _vertlines_xs_per_clusters),
    ) = _compute_tables_rect_and_lines_coord(block_clusters)

    # For each cluster, compute the lines as 2-tuple of Points.
    _lines_per_clusters: list[list[tuple[pymupdf.Point, pymupdf.Point]]] = (
        _compute_lines(
            cluster_rects=_cluster_rects,
            horizlines_ys_per_clusters=_horizlines_ys_per_clusters,
            vertlines_xs_per_clusters=_vertlines_xs_per_clusters,
        )
    )

    return (
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
        _cluster_rects,
        _lines_per_clusters,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
