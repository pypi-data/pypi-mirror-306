# main.py
'''
Main entry point to the spans per blocks based table detector.

To the difference of the pymupdf table detector, this table detector
works by using the blocks-lines-spans dictionaries and assumes a
table if it finds two or more blocks, that each have several lines dict
on the same geometrical line separated by an unusually wide white space.
'''

import logging
from typing import Union

# from statistics import geometric_mean, harmonic_mean
import pymupdf  # type: ignore

from pdf_structr.tables.table_lib import (
    fill_in_table_dicts,
)
from pdf_structr.tabs.tab_enl import (
    try_to_extend_and_merge_tables,
)
from pdf_structr.tabs.tab_extract import (
    extract_stab_to_markdown,
    extract_table,
    make_header_names,
)
from pdf_structr.tabs.tab_rows import (
    compute_tables_rows_properties,
)
from pdf_structr.tabs.tabs_make import (
    convert_clusters_to_tables,
)
from pdf_structr.tabs.tabs_validate import (
    validate_tables,
)
from pdf_structr.tabs.utils import (
    in_clip,
)
from pdf_structr.tabs_clust.clustc_validate_coords import (
    validate_table_candidates,
)
from pdf_structr.tabs_clust.rlb import (
    make_rlb_clusters,
)
from pdf_structr.tabs_clust.rlb_coords import (
    compute_clusters_coordinates,
)
from pdf_structr.utils.utils import (
    sort_rect_key_by_bottom_y_left_x,
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
# Detect tables and return list of list of list of str
#####################


def _fill_in_table_dicts_from_table_dicts(
    tab_rects: dict[int, pymupdf.Rect],
    tab_md_strs: dict[int, str],
    table: dict[  # type: ignore
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple, tuple, tuple, tuple],  # list of cols bbox
    ],
    idx: int,
):
    '''
    Fills in the tables Rectangles dict and the tables markdown strings
    dict.

    :param tab_rects: dict[int, pymupdf.Rect]: the numbered dict of table
        Rectangles for the tables detected by the stabs detector.

    :param tab_md_strs: dict[int, str]:  the numbered dict of table
        strings for the tables detected by the stabs detector.

    :param table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple, tuple, tuple, tuple],  # list of cols bbox
    ]: a table dictionary.

    param idx: int: the index number of the table in the list of tables
        candidates.
    '''
    # Compute table's edges as well as line and columns coordinates
    _table_rect: pymupdf.Rect = table['bbox']

    # Compute other parameter to pass to the fill_in_table_dicts fn
    _table_col_count: int = len(table['cols'])  # type: ignore

    # Get the table rows
    _table_rows: list[list[str]] = extract_table(table)

    # Get table headers if you can
    _header_names: list[str] = make_header_names(table)

    # Make the table md string
    _table_md_str: str = extract_stab_to_markdown(
        header_names=_header_names,
        table_rows=_table_rows,
        col_count=_table_col_count,
    )

    return fill_in_table_dicts(
        tab_rects=tab_rects,
        tab_md_strs=tab_md_strs,
        table_rect=_table_rect,
        table_md_str=_table_md_str,
        row_count=len(table['rows']),  # type: ignore
        col_count=_table_col_count,
        idx=idx,
    )


#####################
# Main API
#####################


def extract_tables_by_clusters(
    page: pymupdf.Page,
    textpage_bbox: pymupdf.Rect,
    blocks: list[dict[str, int | float | tuple | list]],
) -> tuple[
    list[dict[str, tuple[float, float, float, float] | int]],
    dict[int, str],
    dict[int, pymupdf.Rect],
    list[pymupdf.Rect],
]:
    '''
    Main API: detects table candidates and extracts them as a table list.

    :param page: pymupdf.Page: the current page.

    :param textpage_bbox: pymupdf.Rect: the area of the page that contains text
        blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.).

    '''

    # 1. Make clusters / detect tables
    # --------------------------------------------

    _rlb_clusters: list[list[dict[str, int | float | tuple | list]]] = (
        make_rlb_clusters(blocks=blocks)
    )

    if not _rlb_clusters:
        return ([], {}, {}, [])

    # 2. Compute table's edges as well as line and columns coordinates
    # --------------------------------------------

    _clusters_coordinates: list[
        tuple[
            pymupdf.Rect,
            list[tuple[float, float]],
            list[tuple[float, float]],
        ]
    ] = compute_clusters_coordinates(_rlb_clusters)

    # 3. Validate candidate tables - ex. checks for overlapping cols
    # --------------------------------------------

    _valid_block_clusters: tuple[tuple, tuple] = validate_table_candidates(
        _rlb_clusters,
        _clusters_coordinates,
    )

    if not _valid_block_clusters:
        return ([], {}, {}, [])

    # 4. Make tables_dicts:
    # for each table:
    # - the page number
    # - the reference y1 gap
    # - the table's Rectangle
    # - the list or rows containing cells containing spans
    # - the list of columns bboxes
    # --------------------------------------------

    _tables_dicts: list[
        dict[
            str,
            Union[
                int,  # page number
                float,  # reference y1 gap
                pymupdf.Rect,  # the table's rectangle
                list[dict],  # the list of rows, including cells and spans
                # the list of cols bboxes
                list[tuple[float, float, float, float]],
            ],
        ]
    ] = convert_clusters_to_tables(
        page.number,
        block_clusters=_valid_block_clusters,
    )

    # 4. Extend tables if possible
    # --------------------------------------------

    _tables_dicts = try_to_extend_and_merge_tables(
        page_textblocks=blocks,
        textpage_bbox=textpage_bbox,
        tables=_tables_dicts,
    )

    # 4. Validate the tables
    # --------------------------------------------

    _tables_dicts = validate_tables(
        page_textblocks=blocks,
        textpage_bbox=textpage_bbox,
        tables=_tables_dicts,
    )

    # 5. Compute table rows properties
    # --------------------------------------------

    _tables_dicts = compute_tables_rows_properties(
        tables=_tables_dicts,
    )

    # 6. Make table information storages
    # --------------------------------------------

    # Declare storages structures
    # - two numbered dicts: one of table rectangles and one of table md strings
    # - a tables list
    _tab_rects_dict: dict[int, pymupdf.Rect] = {}
    # NOTE: Refacto: _tab_md_strs could be a dict of preconfigured partials
    # instead of already output strings
    _tab_md_strs: dict[int, str] = {}

    # NOTE: Convert this to a numbered dict because the information stored
    # here may change if the tables are merged or deleted because duplicates
    # with tables detected by the NewTableFinder
    _tables: list[dict[str, tuple[float, float, float, float] | int]] = [
        _fill_in_table_dicts_from_table_dicts(
            tab_rects=_tab_rects_dict,
            tab_md_strs=_tab_md_strs,
            table=_table_dict,
            idx=_idx,
        )
        for _idx, _table_dict in enumerate(_tables_dicts)
    ]

    # 7. Make a Rectangles' list and sort them
    # --------------------------------------------

    _tab_rects0: list[pymupdf.Rect] = list(_tab_rects_dict.values())
    _tab_rects0.sort(key=sort_rect_key_by_bottom_y_left_x)

    return (
        _tables,
        _tab_md_strs,
        _tab_rects_dict,
        _tab_rects0,
    )


#####################
# Detect tables in clip
#####################


def extract_tables_by_clusters_in_clip(
    page: pymupdf.Page,
    textpage_bbox: pymupdf.Rect,
    blocks,
    clip: pymupdf.Rect | tuple[float, float, float, float] | None = None,
):
    '''
    Wrapper for `detect_and_extract_table_list_dict` that filters blocks within
    a clip for table detection.

    '''

    def _filter_blocks_to_clip(
        blocks: list[dict[str, int | float | tuple | list]],
        clip: pymupdf.Rect,
    ) -> list[dict[str, int | float | tuple | list]]:
        '''
        Walk the blocks and returns the ones that are in the clip
        '''
        return [
            _block
            for _block in blocks
            if in_clip(clip, _block['bbox'])  # type: ignore
        ]

    # filter the blocks to the ones inside the clip
    _clipped_blocks = _filter_blocks_to_clip(blocks, clip)

    # if there are any blocks in there, try to find tables
    if _clipped_blocks:
        return extract_tables_by_clusters(
            page=page,
            textpage_bbox=textpage_bbox,
            blocks=_clipped_blocks,
        )

    return ([], {}, {}, [])


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
