# extract_tables.py
'''
Storing the tables mapping and extraction from a pdf page.
'''
# from typing import Iterable

import pymupdf  # type: ignore

from pdf_structr.tables.classes import (
    NewTable,
    NewTableFinder,
)
from pdf_structr.tables.table import (
    find_tables,
)
from pdf_structr.tabls_lib.table_lib import (
    fill_in_table_dicts,
)
from pdf_structr.tabls_lib.tables_tup_combine import (
    combine_tables_tuples,
)
from pdf_structr.tabs.main import (
    extract_tables_by_clusters,
    extract_tables_by_clusters_in_clip,
)
from pdf_structr.tabs_clb.main import (
    get_table_like_blocks_groups,
)
from pdf_structr.utils.utils import (
    sort_rect_key_by_bottom_y_left_x,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


def _make_fulltable_rect_for_NewTable(
    table: NewTable,
) -> pymupdf.Rect:
    '''
    Makes and returns the smallest common Rectangle (union) of the table and
    its header.

    :param table: NewTable: the current table extracted
        from the table finder.

    '''
    return pymupdf.Rect(table.bbox) | pymupdf.Rect(table.header.bbox)


# @count_and_avg_timer(name='prep - _extract_tables_with_NewTableFinder')
def _extract_tables_with_NewTableFinder(
    page: pymupdf.Page,
    textpage: pymupdf.TextPage,
    drawings: list[dict],
    clip: pymupdf.Rect,
    table_strategy: str,
    blocks: list[dict],
) -> tuple[
    list[dict[str, tuple[float, float, float, float] | int]],
    dict[int, str],
    dict[int, pymupdf.Rect],
    list[pymupdf.Rect],
]:
    '''
    For a given page, makes:
    - a list of table bboxes, rows and columns ("tables")
    - an ordered dict of table md strings, sorted by y1 and x0 and
    where the keys are the index numbers in the table finder ("tab_rects")
    - an ordered dict of table rectangles, sorted by y1 and x0 and
    where the keys are the index numbers in the table finder ("tab_rects")
    - a list of table rectangles ("tab_rects0")
    Extract all the table related objects and returns them.

    :param page: pymupdf.Page: the current page.
    :param textpage: pymupdf.TextPage: the corresponding previously extracted
        textpage.
    :param drawings: the page drawings as returned by page.drawings().
    :param clip: pymupdf.Rect: the area of the page that should be parsed for
        tables.
    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries
    :param blocks: list[dict]: the previously extracted blocks.

    '''
    # 1. Create a table finder to locate all the tables on the page
    _tabs: NewTableFinder = find_tables(
        page=page,
        textpage=textpage,
        drawings=drawings,
        clip=clip,
        strategy=table_strategy,
        blocks=blocks,
    )

    # 2. Make table information storages
    # - two numbered dicts: one of table rectangles and one of table md strings
    # - a tables list
    _tab_rects_dict: dict[int, pymupdf.Rect] = {}
    _tab_md_strs: dict[int, str] = {}

    _tables: list[dict[str, tuple[float, float, float, float] | int]] = [
        fill_in_table_dicts(
            tab_rects=_tab_rects_dict,
            tab_md_strs=_tab_md_strs,
            table_rect=_make_fulltable_rect_for_NewTable(_table),
            table_md_str=_table.to_markdown(clean=False),
            row_count=_table.row_count,
            col_count=_table.col_count,
            idx=_idx,
        )
        for _idx, _table in enumerate(_tabs.tables)
    ]

    # 3. Make a Rectangle's list and sort it
    _tab_rects0: list[pymupdf.Rect] = list(_tab_rects_dict.values())
    _tab_rects0.sort(key=sort_rect_key_by_bottom_y_left_x)

    return (
        _tables,
        _tab_md_strs,
        _tab_rects_dict,
        _tab_rects0,
    )


def _compute_remaining_text_rects_to_parse(
    textpage_bbox: pymupdf.Rect,
    already_parsed_rects: list[pymupdf.Rect],
) -> list[pymupdf.Rect]:
    '''
    Compute Rectangles for zones which contains text and have not
    already been parsed.

    :returns: a list of Rectangles which may contain remaining text blocks.

    :param textpage_bbox: pymupdf.Rect: the largest Rectangle containing
        text blocks.

    :param already_parsed_rects: list[pymupdf.Rect]: the list of already
        parsed text blocks.

    '''

    # If no Rectangle yet parsed, return the textpage bbox
    # as a list[Rect]
    if not already_parsed_rects:
        return [textpage_bbox]

    # Else: there are already parsed rectangles

    # if the _parsed_rect contain only one rectangle and
    # this rectangle contains the textpage, there is nothing
    # left to parse -> return an empty list
    if len(already_parsed_rects) == 1 and already_parsed_rects[0].contains(
        textpage_bbox
    ):
        return []

    # Else: there is one or several rectangles smaller than the
    # textpage

    # Define a return list
    _remaining_rects: list[pymupdf.Rect] = []

    # Get the textpage coordinates
    _x0: float = textpage_bbox.x0
    _x1: float = textpage_bbox.x1
    _y0: float = textpage_bbox.y0

    for _parsed_rect in already_parsed_rects:

        # make a rect from the textpage y0
        # down to the top of the current rect
        _remaining_rects += [
            pymupdf.Rect(
                _x0,
                _y0,
                _x1,
                _parsed_rect.y0,
            )
        ]

        # reset the _y0 for the next _remaining_rect to be build
        # to the bottom of the current rect
        _y0 = _parsed_rect.y1

    return _remaining_rects


# @count_and_avg_timer(name='prep - extract_tables')
def extract_tables(
    page: pymupdf.Page,
    textpage: pymupdf.TextPage,
    drawings: list[dict],
    blocks: list[dict[str, int | float | tuple | list]],
    clip: pymupdf.Rect,
    textpage_bbox: pymupdf.Rect,
    table_strategy: str,
) -> tuple[
    list[dict[str, tuple[float, float, float, float] | int]],
    dict[int, str],
    dict[int, pymupdf.Rect],
    list[pymupdf.Rect],
]:
    '''
    For a given page, makes:
    - a list of table bboxes, rows and columns ("tables")
    - an ordered dict of table md strings, sorted by y1 and x0 and
    where the keys are the index numbers in the table finder ("tab_rects")
    - an ordered dict of table rectangles, sorted by y1 and x0 and
    where the keys are the index numbers in the table finder ("tab_rects")
    - a list of table rectangles ("tab_rects0")
    Extract all the table related objects and returns them.

    We use various methods to detect tables:
    - NewTableFinder in strict_lines mode, to detect "drawn" tables
    - three text-position based methods:
        - a "cell-like blocks"-based analysis, where text blocks are gathered
        into rows and may be end up part of a cell in a (large) table
        - a column-based approach to detecting columns within the rows to
        infere (smaller) tables embedded between paragraphs
        - a "row-like blocks"-based analysis, where the blocks form lines
        in a table

    :param page: pymupdf.Page: the current page.

    :param textpage: pymupdf.TextPage: the corresponding previously extracted
        textpage.

    :param drawings: the page drawings as returned by page.drawings().

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white blocks and images blocks filtered out and
        spans' dicts augmented with digit_count, punct_count, etc.)

    :param clip: pymupdf.Rect: the area of the page that should be parsed for
        tables.

    :param textpage_bbox: pymupdf.Rect: the area of the page that contains text
        blocks.

    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries
    '''
    # Pre-detects potential tables by making rows of blocks and detecting
    # columns within the rows between the spans of the blocks of a row
    _grps_of_tabular_rows, _tables_from_isolated_rows = (
        get_table_like_blocks_groups(page=page, blocks=blocks)
    )

    # Using the pre-table detector to prevent starting detection on
    # pages not containing any tables
    if not (_grps_of_tabular_rows) and not (_tables_from_isolated_rows):
        return ([], {}, {}, [])

    pass

    # Detect tables with pymupdf refactored table detector
    _tables_from_NewTableFinder: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
        list[pymupdf.Rect],
    ] = _extract_tables_with_NewTableFinder(
        page=page,
        textpage=textpage,
        drawings=drawings,
        clip=clip,
        table_strategy=table_strategy,
        blocks=blocks,
    )

    _list_clips: list[pymupdf.Rect] = _compute_remaining_text_rects_to_parse(
        textpage_bbox=textpage_bbox,
        already_parsed_rects=_tables_from_NewTableFinder[3],
    )

    # Detect tables made of blocks that act as lines in the table

    # If not clip or only one clip (i.e. the textpage)

    if not _list_clips:

        # call directly extract_tables_by_clusters
        _tables_from_clusters_tuple: list[
            tuple[
                list[dict[str, tuple[float, float, float, float] | int]],
                dict[int, str],
                dict[int, pymupdf.Rect],
                list[pymupdf.Rect],
            ]
        ] = [
            extract_tables_by_clusters(
                page=page,
                textpage_bbox=textpage_bbox,
                blocks=blocks,
            )
        ]

    else:
        # otherwise, walk the clips
        _tables_from_clusters_tuple = [
            extract_tables_by_clusters_in_clip(
                page=page,
                textpage_bbox=textpage_bbox,
                blocks=blocks,
                clip=_clip,
            )
            for _clip in _list_clips
        ]

    return combine_tables_tuples(
        _tables_from_NewTableFinder,
        _tables_from_clusters_tuple,
    )
