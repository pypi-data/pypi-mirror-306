# stabs_tft_tfextract.py
'''
Module to encapsulate the interface between stabs and
pymupdf's TableFinder and make the extraction of a list
of strings, by making one or several configured calls
to the `find_tables` function of pymupdf.

With the returned TableFinder, builds a list of 3-tuples,
each containing:
- a table as a list of list of strings
- the table's bbox
- the header's bbox

In this context, table extraction is the step that comes
after building tables and consists in converting the tables
to a text string and a bbox.

DEAD CODE: The function `extract_tables_with_pymupdf` is no longer
in use as we are no longer using stabs to configure a call to pymupdf's
TableFinder but uses its own text extraction features.

It is still kept as a legacy interface that could find some use in
the future.

IMPORTANT: modules with `ftf` in their names are parts of the interface
from to stabs to NewTableFinder.
'''

import logging
from functools import partial
from typing import Callable

# from statistics import geometric_mean, harmonic_mean
import pymupdf  # type: ignore

from pdf_structr.tables.classes import NewTable
from pdf_structr.tables.table import (
    find_tables,
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
# Extract tables with pymupdf TableFinder
#####################


def _extract_table_from_table_finder(table: NewTable) -> tuple[
    list[list[str]],
    tuple[float, float, float, float],
    tuple[float, float, float, float] | pymupdf.Rect,
]:
    '''
    From the passed-in table, extracts the text content as a list of list of
    strings, the table's bbox and the header's bbox.

    :returns: a 3-tuple, with:
    - the table as a list of list of strings
    - the table's bbox
    - the header's bbox

    :param table: NewTable: a table from the TableFinder.
    '''
    return (
        table.extract(),
        table.bbox,
        table.header.bbox,
    )


def extract_tables_with_pymupdf(
    page: pymupdf.Page,
    textpage: pymupdf.TextPage,
    cluster_rects_list: list[pymupdf.Rect],
    lines_per_clusters: list[list[tuple[pymupdf.Point, pymupdf.Point]]],
    horizlines_ys_per_clusters: list[list[float]],
    vertlines_xs_per_clusters: list[list[float]],
) -> list[
    tuple[
        list[list[str]],  # list of string
        tuple[float, float, float, float],
        tuple[float, float, float, float] | pymupdf.Rect,
    ]
]:
    '''
    Given the passed-in `cluster_rects_list`, `horizlines_ys_per_clusters`
    and `vertlines_xs_per_clusters`,
    Calls the find_tables function of pymupdf TableFinder and extracts tables'
    to a list of strings.

    :returns: a list of 3-tuples, where each 3-tuple contains:
    - the table as a list of list of strings
    - the table's bbox
    - the header's bbox

    :param page: pymupdf.Page: the current page.

    :param textpage: pymupdf.TextPage: the current text page.

    :param cluster_rects_list: list[pymupdf.Rect]: the list of Rectangles
        for the clusters (table candidates) identified in the page.

    :param lines_per_clusters: list[list[tuple[pymupdf.Point, pymupdf.Point]]]:
        a list of lines as pairs of point_like objects for each cluster. These
        lines are both horizontal and vertical and are meant to help
        `find_tables` detect tables.

    :param horizlines_ys_per_clusters: list[list[float]]: the list of
        y coordinates for the lines' edges of each table candidate identified
        in the page.

    :param vertlines_xs_per_clusters: list[list[float]]: the list of
        x coordinates for the columns' edges of each table candidate identified
        in the page.

    '''
    _find_tables_partial: Callable = partial(
        find_tables,
        page=page,
        # NOTE: use "explicit" or "lines_strict"
        horizontal_strategy='explicit',
        vertical_strategy='explicit',
    )

    return [
        _extract_table_from_table_finder(_table)
        for _idx, _cluster_rect in enumerate(cluster_rects_list)
        for _table in _find_tables_partial(
            clip=_cluster_rect,
            horizontal_lines=horizlines_ys_per_clusters[_idx],
            vertical_lines=vertlines_xs_per_clusters[_idx],
            snap_x_tolerance=3,  # NOTE: to be set dynamically
            snap_y_tolerance=12,  # NOTE: to be set dynamically
            add_lines=lines_per_clusters[_idx],
        )
    ]


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
