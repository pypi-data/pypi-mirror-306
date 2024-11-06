# tabs_make.py
'''
Module storing the functions converting a candidate table
from a cluster of blocks to a table dict.
'''

import logging

import pymupdf  # type: ignore

from pdf_structr.tabs.tab_rows import make_rows

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
# Tables components: cols
#####################


def _make_cols(
    cluster_coord: tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ],
) -> list[tuple[float, float, float, float]]:
    '''
    Makes a list of bboxes for each column out of cluster_coord tuple.

    cluster_coord: tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ]: a 3-tuples containing:

    - a table's Rectangle.
    - a list of y0-y1 coordinates of each line.
    - a list of x0-x1 coordinates of each line.
    '''
    # Get the x0 - x1 2-tuples corresponding the columns coordinates
    _x0_x1_tup_list: list[tuple[float, float]] = cluster_coord[2]

    # Combine each of them in a 4-float tuple bbox and returns a list
    # columns bboxes
    return [
        (
            _cols_coord[0],
            cluster_coord[0].y0,
            _cols_coord[1],
            cluster_coord[0].y1,
        )
        for _cols_coord in _x0_x1_tup_list
    ]


#####################
# Table
#####################


def _convert_cluster_to_table(
    page_number: int,
    block_cluster: list[dict[str, int | float | tuple | list]],
    cluster_coord: tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ],
) -> dict:
    '''
    Converts a cluster and its coordinates into a table dict.

    :param page_number: int: the page number.

    :param block_cluster: list[dict[str, int | float | tuple | list]]:
        a list of the blocks in a cluster.

    cluster_coord: tuple[
        pymupdf.Rect,
        list[tuple[float, float]],
        list[tuple[float, float]],
    ]: a 3-tuples containing:

    - a table's Rectangle.
    - a list of y0-y1 coordinates of each line.
    - a list of x0-x1 coordinates of each line.

    '''

    return {
        'pno': page_number,
        'bbox': cluster_coord[0],
        'rows': make_rows(block_cluster),
        'cols': _make_cols(cluster_coord),
    }


def convert_clusters_to_tables(
    page_number: int,
    block_clusters: tuple[
        tuple[list[dict[str, int | float | tuple | list]], ...],
        tuple[
            tuple[
                pymupdf.Rect,
                list[tuple[float, float]],
                list[tuple[float, float]],
            ],
            ...,
        ],
    ],
) -> list[dict]:
    '''
    Converts a list of blocks cluster and the corresponding list
    of clusters coordinates into a list of table dicts.

    :param page_number: int: the current page number.

    :param block_clusters: tuple[
        tuple[list[dict[str, int | float | tuple | list]], ...],
        tuple[
            tuple[
                pymupdf.Rect,
                tuple[list[float], list[tuple[float, float]]],
                tuple[list[float], list[tuple[float, float]]],
            ], ...
        ]
    ]: a tuple of 2-tuples, where the first subtuple is the list of
        blocks' clusters previously built by `make_rlb_clusters` and
        the second subtuple is a list of 3-tuples, with the block's
        Rectangle, the y-coordinates of its rows and the x-coordinates
        of its cols. More precisely, each 3-tuple contains:

    - a table's Rectangle
    - a list of y0-y1 coordinates of each line.
    - a list of x0-x1 coordinates of each line.
    '''

    return [
        _convert_cluster_to_table(
            page_number,
            _block_cluster,
            _cluster_coord,
        )
        for _block_cluster, _cluster_coord in zip(
            block_clusters[0],  # the blocks' cluster
            block_clusters[1],  # the cluster's coordinates
        )
    ]


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
