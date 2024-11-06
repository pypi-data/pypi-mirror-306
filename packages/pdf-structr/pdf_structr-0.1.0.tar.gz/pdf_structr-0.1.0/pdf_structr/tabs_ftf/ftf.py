# ftf.py
'''
Module to encapsulate a spans per blocks based table detector
for TableFinder.

All the processes and return values are made on list of clusters.

Kepts for references because returns lines as 2-tuples that can be used
for the add_lines parameter of the find_table function of the
pymupdf table module.

IMPORTANT: modules with `ftf` in their names are parts of the interface
from to stabs to NewTableFinder.
'''

import logging

# from statistics import geometric_mean, harmonic_mean
import pymupdf  # type: ignore

from pdf_structr.tabs.tab_extract import (
    simple_extract_tables,
)
from pdf_structr.tabs_clust.rlb import (
    make_rlb_clusters,
)
from pdf_structr.tabs_ftf.ftf_coords import (
    compute_lines_and_rects_per_clusters,
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
# Detect tables and compute coordinates
#####################


def _detect_tables_and_compute_coords(
    blocks: list[dict[str, int | float | tuple | list]],
) -> tuple[
    list[list[float]],
    list[list[float]],
    list[list[tuple[pymupdf.Point, pymupdf.Point]]],
    list[pymupdf.Rect],
    list[list[dict[str, int | float | tuple | list]]],
]:
    '''
    Function to detect table candidates once the spans' and the blocks' dicts
    have been augmented and the blocks-lines-spans filtered out
    of their white elements.

    The main detection stage is made by grouping the blocks into clusters
    that could correspond to a table.

    The criteria used to detect the tables are described `make_block_clusters`.

    :returns: a 5-tuple of lists:
    - one list of list of floats, corresponding to the y coordinates of the
      lines for each table candidate
    - one list of list of floats, corresponding to the x coordinates of the
      lines for each table candidate
    - one list of list of lines (represented as a 2-tuple of Points), both
      horizontal and vertical, for each table candidate
    - one list of Rect, corresponding to the bboxes of the table candidates
    - a list of clusters of blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.)
    '''

    # 1. make clusters / detect tables
    _block_clusters: list[list[dict[str, int | float | tuple | list]]] = (
        make_rlb_clusters(blocks=blocks)
    )

    # 2. compute geometry
    (
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
        _cluster_rects,
        _lines_per_clusters,
    ) = compute_lines_and_rects_per_clusters(_block_clusters)

    return (
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
        _lines_per_clusters,
        _cluster_rects,
        _block_clusters,
    )


def detect_and_extract_tables_and_coords(
    blocks: list[dict[str, int | float | tuple | list]],
):
    '''
    Detects table candidates and extracts them as a table list.

    Also returns the tables lines and columns coordinates, the tables
    bboxes and the lines as 2-tuples of Points, to be eventually
    passed to pymupdf.find_tables.

    :returns: the table candidates as well as the coordinates for
        tables, their line and column edge, their bboxes and the
        corresponding blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.)

    '''

    # Detect table
    (
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
        _lines_per_clusters,
        _cluster_rects,
        _block_clusters,
    ) = _detect_tables_and_compute_coords(blocks=blocks)

    _simple_table_list: list[list[list[str]]] = simple_extract_tables(
        block_clusters=_block_clusters
    )

    # if _simple_table_list:
    #     pass

    return (
        _horizlines_ys_per_clusters,
        _vertlines_xs_per_clusters,
        _lines_per_clusters,
        _cluster_rects,
        _block_clusters,
        _simple_table_list,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
