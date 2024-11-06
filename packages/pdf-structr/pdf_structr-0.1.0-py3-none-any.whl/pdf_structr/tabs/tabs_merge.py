# tabs_merge.py
'''
Module encapsulating the merging of two consecutive tables on the same page.
'''

import logging

import pymupdf  # type: ignore

from pdf_structr.tabs.tab_fns import (
    compute_rows_ref_y_gap,
)
from pdf_structr.tabs.utils import (
    in_clip,
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
# Mergeability testing
#####################


def _have_significt_horizontal_overlap_and_about_same_size(
    first_tab_bbox: pymupdf.Rect,
    second_tab_bbox: pymupdf.Rect,
) -> bool:
    '''
    Tests if two tables have a significant overlap and are about
    the same size.
    '''
    _first_tab_width: float = first_tab_bbox.x1 - first_tab_bbox.x0
    _second_tab_width: float = second_tab_bbox.x1 - second_tab_bbox.x0

    _smallest_tab_width: float = min(_first_tab_width, _second_tab_width)
    _largest_tab_width: float = max(_first_tab_width, _second_tab_width)

    return (
        # test if have horizontal significant overlap
        (
            abs(second_tab_bbox.x0 - first_tab_bbox.x0)
            <= (1 / 3 * _smallest_tab_width)
        )
        # test if about the same size
        and (_smallest_tab_width / _largest_tab_width) >= 3 / 4
    )


def _are_horizontally_overlapping(
    first_tab_bbox: pymupdf.Rect,
    second_tab_bbox: pymupdf.Rect,
) -> bool:
    '''
    Basic testing over horizontal overlap between two bboxes.
    '''
    return (
        # second table overlapping from the right
        (first_tab_bbox.x0 <= second_tab_bbox.x0 <= first_tab_bbox.x1)
        or
        # second table overlapping from the left
        (
            (second_tab_bbox.x0 <= first_tab_bbox.x1)
            and (first_tab_bbox.x0 <= second_tab_bbox.x1)
        )
    )


def _has_text_blocks_in_the_clip(
    first_tab_bbox: pymupdf.Rect,
    second_tab_bbox: pymupdf.Rect,
    page_textblocks: list[dict[str, int | float | tuple | list]],
) -> bool:
    '''
    Test if there are some text blocks in between two tables.

    :param first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the first table to test for textblocks below.

    :param first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the second table to test for textblocks above.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

    '''
    _clip_between_tables: pymupdf.Rect = pymupdf.Rect(
        x0=min(first_tab_bbox.x0, second_tab_bbox.x0),
        y0=first_tab_bbox.y1,
        x1=max(first_tab_bbox.x1, second_tab_bbox.x1),
        y1=second_tab_bbox.y0,
    )

    _blocks_in_between: list[dict[str, int | float | tuple | list]] = [
        _block
        for _block in page_textblocks
        if in_clip(_clip_between_tables, _block['bbox'])  # type: ignore
    ]

    if _blocks_in_between:
        return True

    return False


def _are_tables_mergeable(
    first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
    second_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
    page_textblocks,
):
    '''
    Test a series of conditions to figure out whether two tables are
    mergeable.

    It is assumed that:
    - first_table is above second_table
    - there are no remaining text blocks positionned horizontally in
    between the tables.

    The tables are tables dict as returned by `convert_clusters_to_tables`.

    Criteria for tables to be deemed mergeable:
    - same number of columns
    - significantly overlapping
    - more or less the same size
    - not too far apart vertically

    :param first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the first table to test for mergeability.

    :param second_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the second table to test for mergeability.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

    '''
    _first_tab_bbox: pymupdf.Rect = first_table['bbox']
    compute_rows_ref_y_gap(first_table)
    _second_tab_bbox: pymupdf.Rect = second_table['bbox']

    return (
        # we need the same number of columns in both table
        (len(first_table['cols']) == len(second_table['cols']))  # type: ignore
        # keep only tables overlapping horizontally
        and _are_horizontally_overlapping(_first_tab_bbox, _second_tab_bbox)
        # keep only tables significantly overlapping horizontally
        # keep only tables that are more or less the same width
        and _have_significt_horizontal_overlap_and_about_same_size(
            first_tab_bbox=_first_tab_bbox,
            second_tab_bbox=_second_tab_bbox,
        )
        # not too far apart vertically
        and (
            (
                (_second_tab_bbox.y0 - _first_tab_bbox.y1)
                < first_table['ref_y0_gap'] * 3
            )
        )
        # no text blocks in the clip between the two
        and (
            not _has_text_blocks_in_the_clip(
                _first_tab_bbox,
                _second_tab_bbox,
                page_textblocks,
            )
        )
    )


#####################
# Merging stack
#####################


def _merge_tables(
    first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
    second_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ],
) -> None:
    '''
    Merges two consecutive tables.

    first_table MUST be above second_table.

    :param first_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the first table to merge.

    :param second_table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]: the second table to merge.
    '''
    # Enlarge the first table's Rectangle
    first_table['bbox'] |= second_table['bbox']  # type: ignore

    # Append the second tables' rows to the first table's row
    first_table['rows'] += second_table['rows']  # type: ignore

    # Recompute the columns' Rectangles
    first_table['cols'] = [
        (
            min(_first_col[0], _second_col[0]),
            _first_col[1],
            max(_first_col[2], _second_col[2]),
            _second_col[3],
        )
        for _first_col, _second_col in zip(
            first_table['cols'],  # type: ignore
            second_table['cols'],  # type: ignore
        )
    ]


def _try_to_merge_tables(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
    new_tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
):
    '''
    Function repeatedly called in the while loop in
    `try_to_merge_tables_wrapper` to try and merge tables
    or push them out of the initial list and into the new list.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the page's textblocks. Used to test if there are any textblocks
        between the tables to be merged.

    :param tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: the initial tables list.

    :param new_tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ]: the final tables list upon merging what can be merged.
    '''
    # Get the first two tables
    _first_table = tables[0]
    _second_table = tables[1]

    # If the tables are mergeable
    if _are_tables_mergeable(_first_table, _second_table, page_textblocks):

        # merge them into the first one
        _merge_tables(
            _first_table,
            _second_table,
        )
        # delete the second one from the old list
        del tables[1]

        return

    # If no merging was possible

    # append the first table to the new list
    new_tables.append(_first_table)
    # delete it from the old list
    del tables[0]


def try_to_merge_tables_wrapper(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ],
) -> list[
    dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple[float, float, float, float]],  # list of cols bbox
    ]
]:
    '''
    Tries to merge tables if there are several tables in the page. Otherwise,
    just return the current tables list.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.). This is the original list
        of blocks passed into the custrag_tabs package.

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
    # Only one table, return the tables' list as is; nothing to do
    # -----------------------------------------------------------------

    if len(tables) == 1:
        return tables

    # More than one tables, let's merge and collect the remaining tables
    # -----------------------------------------------------------------

    # Declare a new tables list
    _new_tables: list[
        dict[
            str,
            int  # page number
            | float  # reference y1_gap
            | pymupdf.Rect  # table's bbox
            | list[dict]  # a list of rows[cells[spans]]
            | list[tuple[float, float, float, float]],  # list of cols bbox
        ]
    ] = []

    # Now we're going to empty the tables' list and merge tables as the case
    # may be
    while len(tables) > 1:

        _try_to_merge_tables(
            page_textblocks=page_textblocks,
            tables=tables,
            new_tables=_new_tables,
        )

    # Add the last table to the new list
    _new_tables.append(tables[0])

    return _new_tables


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
