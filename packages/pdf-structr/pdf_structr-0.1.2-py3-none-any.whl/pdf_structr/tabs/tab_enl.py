# tab_enl.py
'''
Module that tries to enlarge the already detected tables
to the neighboring upper or lower blocks and merge
tables that are positionned above each other.

NOTE: the whole module implicitly assumes that the current table
occupies more or less the whole (text)page width.

'''


import logging
from typing import Callable

import pymupdf  # type: ignore  # type: ignore

from pdf_structr.tabs.tab_enl_nr_dis import (
    make_new_row_when_discrepancy,
)
from pdf_structr.tabs.tab_enl_nr_reg import (
    make_new_row_decorator,
    make_new_row_from_blocks,
    make_new_row_from_closest_block,
)
from pdf_structr.tabs.tab_enl_sel_blocks import (
    get_lower_blocks,
    get_upper_blocks,
)
from pdf_structr.tabs.tab_fns import (
    compute_rows_ref_y_gap,
)
from pdf_structr.tabs.tabs_merge import (
    try_to_merge_tables_wrapper,
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
# Table instance level
#####################


def _try_to_extend_one_dir_one_row(
    page_textblocks: list[dict],
    table: dict,
    start: float,
    limit: float,
    block_extraction_fn: Callable,
    ext_direction: int,
) -> bool:
    '''
    Function wrapping calls to three extension methods.
    Tries to extend the passed-in table by one row in one direction.

    :returns: True if it has extended and False otherwise.

    :param page_textblocks: list[dict]: the textblocks in the page.

    :param table: dict: the current table we're trying to extend.

    :param start: float: the starting y coordinate (the table's top y if
        trying to extend upwards and the bottom y if downwards).

    :param limit: float: the limit beyond which not to collect blocks.
        Either the page_textblock's limits (its y0 if extending up or its
        y1 if extending down) if there is one table only (or for the first
        and last tables) or the neighboring tables (for tables between other
        tables).

    :param block_extraction_fn: Callable,

    :param ext_direction: int: -1 if looking upwards; 0 if looking
        downwards. Will be used to select the relevant closest blocks
        and eventually sort the blocks.

    '''

    # 1. Configuration
    # ------------------------------------------------------------

    # Compute the reference row height for the table; this does not
    # return anything but update 'ref_y0_gap' key in the table dict
    compute_rows_ref_y_gap(table)

    # 2. Get neighboring blocks
    # ------------------------------------------------------------

    # Look for blocks above the table: go 2 ref_y0_gap up but no higher
    # than the limit of the textpage_bbox or the bottom of the previous
    # table
    _neighbor_blocks: list[dict[str, int | float | tuple | list]] = (
        block_extraction_fn(
            limit_y_coord=limit,
            start_y_coord=start,
            table_ref_y0_gap=table['ref_y0_gap'],  # type: ignore
            page_textblocks=page_textblocks,
        )
    )

    # If no blocks within the searched zones, return False
    if not _neighbor_blocks:
        return False

    # 3. Try to identify rows and extend the table
    # ------------------------------------------------------------

    # Initialize an _has_extended boolean to keep track of whether
    # we managed to extend the table
    # This value will be returned
    _has_extended: bool = False

    # 3.A - Try to extend by taking the lines inside the closest block

    _has_extended = make_new_row_decorator(
        make_new_row_from_closest_block,
    )(
        neighbor_blocks=_neighbor_blocks,  # type: ignore
        table=table,
        idx_for_closest_block=ext_direction,
    )

    if _has_extended:

        return _has_extended

    # 3.B - Try to extend by taking the lines inside all the blocks

    _has_extended = make_new_row_decorator(
        make_new_row_from_blocks,
    )(
        neighbor_blocks=_neighbor_blocks,  # type: ignore
        table=table,
    )

    if _has_extended:

        return _has_extended

    # 3.C - Try to extend by making virtual cells or grouping
    # lines close together

    _has_extended = make_new_row_decorator(
        make_new_row_when_discrepancy,
    )(
        neighbor_blocks=_neighbor_blocks,  # type: ignore
        table=table,
        ext_direction=ext_direction,
    )

    return _has_extended


def compute_limit(textpage_bbox, table_neighbors_bbxs, direction) -> float:
    '''
    Recomputes the limit beyond which not too search at each iteration.
    '''
    _limit: float

    # If we're looking upwards
    if direction == -1:
        # default: top of text blocks
        _limit = textpage_bbox.y0
        # If there is a preededing table neighbor
        if table_neighbors_bbxs[0]:
            # set to the bottom of the neighbor
            _limit = table_neighbors_bbxs[0].y1

        return _limit

    # If we're looking upwards
    # default: bottom of text blocks
    _limit = textpage_bbox.y1
    # If there is a next table neighbor
    if table_neighbors_bbxs[1]:
        # set to the top of the neighbor
        _limit = table_neighbors_bbxs[1].y0

    return _limit


def _try_to_extend_table(
    textpage_bbox: pymupdf.Rect,
    table_neighbors_bbxs: tuple[pymupdf.Rect, pymupdf.Rect],
    page_textblocks: list[dict[str, int | float | tuple | list]],
    table: dict[  # type: ignore
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple, tuple, tuple, tuple],  # list of cols bbox
    ],
) -> None:
    '''
    Try to extend the passed-in table by looking around the table for
    additional rows.

    :param textpage_bbox: pymupdf.Rect: the area of the page that contains text
        blocks.

    :param table_neighbors_bbxs: tuple[pymupdf.Rect, pymupdf.Rect]: a
        2-Rect tuple, where the first Rect is the previous table's Rect
        (or None if none) and this second one is the next table's Rect
        (or None if none). It helps to define a zone beyond which no tables
        shall be searched.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

    '''

    _has_extended: bool

    _block_extraction_fncs: tuple[Callable, Callable] = (
        get_upper_blocks,
        get_lower_blocks,
    )

    # Loop trying to extend upwards, then downwards
    for _dir, _extract_fnc in enumerate(_block_extraction_fncs, start=-1):

        _has_extended = True

        # Loop again while has extended in one direction to try and extend
        # further.
        # The while loop stops when no new extension could be made.
        while _has_extended:

            _limit: float = compute_limit(
                textpage_bbox,
                table_neighbors_bbxs,
                _dir,
            )

            _start: float = (
                table['bbox'].y0  # type: ignore
                if _dir == -1  # we start to extract upwards
                else table['bbox'].y1  # type: ignore
            )

            _has_extended = _try_to_extend_one_dir_one_row(
                page_textblocks=page_textblocks,
                table=table,
                limit=_limit,
                start=_start,
                block_extraction_fn=_extract_fnc,
                ext_direction=_dir,
            )


#####################
# Tables collection level
#####################


def _try_to_extend_tables(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    textpage_bbox: pymupdf.Rect,
    tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
) -> list[dict]:
    '''
    Tries to extend the table to neighbouring cells.


    :returns: a list of tables dictionaries.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

    :param textpage_bbox: pymupdf.Rect: the area of the page that contains text
        blocks.

    :param tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of table dictionaries.

    '''
    # 0-based tables count
    _tables_count: int = len(tables)
    _tables_max_idx: int = _tables_count - 1

    # Upper and lower limits where to look for additional cells
    # By default, the textpage_bbox limits
    _prev_tab_bbox: pymupdf.Rect | None = None
    _next_tab_bbox: pymupdf.Rect | None = None

    # Walk the tables and try to extend
    for _idx, _table in enumerate(tables):

        # Recompute the upper and lower limits if we
        # have more than one table.
        # The upper limit shall be the previous table
        # bottom y and the lower one shall be the following
        # table top y.
        if _tables_count > 0:
            if _idx > 0:
                _prev_tab_bbox = tables[_idx - 1]['bbox']  # type: ignore
            if _idx < _tables_max_idx:
                _next_tab_bbox = tables[_idx + 1]['bbox']  # type: ignore
            else:
                _next_tab_bbox = None

        # Try to extend the current table
        _try_to_extend_table(
            textpage_bbox,
            table_neighbors_bbxs=(_prev_tab_bbox, _next_tab_bbox),
            page_textblocks=page_textblocks,
            table=_table,
        )

    return tables


#####################
# Tables collection main API
#####################


def try_to_extend_and_merge_tables(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    textpage_bbox: pymupdf.Rect,
    tables: list[  # type: ignore
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
) -> list[dict]:
    '''
    Tries to extend the table to neighbouring cells and to merge the tables
    that are close enough, with no text blocks in between and of similar
    structure.

    :returns: a list of tables dictionaries.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

    :param textpage_bbox: pymupdf.Rect: the area of the page that contains text
        blocks.

    :param tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: a list of table dictionaries.

    '''
    tables = _try_to_extend_tables(
        page_textblocks=page_textblocks,
        textpage_bbox=textpage_bbox,
        tables=tables,
    )

    tables = try_to_merge_tables_wrapper(
        page_textblocks=page_textblocks, tables=tables
    )

    return tables


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
