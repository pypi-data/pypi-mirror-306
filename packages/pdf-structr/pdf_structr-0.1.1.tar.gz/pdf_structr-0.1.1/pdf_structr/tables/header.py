# header.py
'''
'''

import copy
from functools import partial
from typing import Any, Callable, Generator

from pymupdf import (  # type: ignore
    EMPTY_RECT,
    Page,
    Rect,
    TextPage,
)

# from pdf_struct.tables.table_classes import TableRow


class TableHeader:
    """PyMuPDF extension containing the identified table header."""

    def __init__(self, bbox, cells, names, above):
        self.bbox = bbox
        self.cells = cells
        self.names = names
        self.external = above


def _is_table_one_liner(
    table_rows: list, first_row_cells: list[tuple[float, float, float, float]]
) -> bool:
    return len(table_rows) < 2 or len(first_row_cells) < 2


def _is_inside_bbox(
    container: tuple[float, float, float, float],
    bbox: Rect,
) -> bool:
    return (
        (container[0] >= bbox.x0)
        and (container[2] <= bbox.x1)
        and (container[1] >= bbox.y0)
        and (container[3] <= bbox.y1)
    )


def _is_table_top_row_bold(
    blocks: list[dict],
    bbox: Rect,
) -> bool:
    """Check if row 0 has bold text anywhere.

    If this is true, then any non-bold text in lines above disqualify
    these lines as header.

    bbox is the (potentially repaired) row 0 bbox.

    Returns True or False
    """
    return any(
        (_span["flags"] & 16) and _is_inside_bbox(_span['bbox'], bbox)
        for _block in blocks
        for _line in _block["lines"]
        for _span in _line["spans"]
    )


def _compute_clip_above_table(
    table_bbox: tuple[float, float, float, float]
) -> Rect:
    # NOTE: comment coming from pymupdf: take row 0 bbox
    # _clip: Rect = +_table_bbox
    # take the table bbox
    _clip: Rect = Rect(table_bbox)
    _clip.y0 = 0  # start at top of page
    # end at top of table
    _clip.y1 = table_bbox[1]

    return _clip


def _get_spans_above_table(
    blocks: list[dict],
    clip_above_table: Rect,
) -> list[dict]:
    '''
    Get the spans that are located above the current table and returns them
    as a list.
    '''

    # for b in page.get_text(
    #   "dict", clip=clip, flags=TEXTFLAGS_TEXT)["blocks"]:
    #     for line in b["lines"]:
    #         for s in line["spans"]:
    #             if (
    #                 not s["flags"] & 1 and s["text"].strip()
    #             ):  # ignore superscripts and empty text
    #                 spans.append(s)

    _spans_above: list[dict] = [  # the text spans inside clip
        _span
        # NOTE: the clip parameter does not work.
        # NOTE: passing the text page avoids an error made when NOT passing
        # the textpage
        # for b in page.get_text(
        #     "dict", clip=clip, flags=TEXTFLAGS_TEXT
        # )["blocks"]:
        for _block in blocks
        for _line in _block["lines"]
        for _span in _line["spans"]
        if (
            _is_inside_bbox(_span['bbox'], clip_above_table)
            # ignore superscripts and empty text
            and (not _span["flags"] & 1 and _span["text"].strip())
        )
    ]

    return copy.deepcopy(_spans_above)


def _compute_clip_get_spans_above_table(
    table_bbox: tuple[float, float, float, float],
    blocks: list[dict],
) -> tuple[Rect, list[dict]]:
    '''
    Get the clip and the spans above the current table.
    '''
    # Compute the clip above the current table
    _clip_above_table: Rect = _compute_clip_above_table(table_bbox)

    # Get the spans above the current table
    _spans_above_table: list[dict] = _get_spans_above_table(
        blocks=blocks,
        clip_above_table=_clip_above_table,
    )

    return _clip_above_table, _spans_above_table


def _recompute_clip_above_table(
    spans_above_table: list[dict],
    top_row_y1_coord: float,
    clip_above_table: Rect,
    first_row_bbox_y0: float,
) -> Rect:
    '''
    Recomputes the clip above a given table.

    Compared to the first computation:

    - y-wise, it will go max 5 lines up instead of to the top
      of the page.
    - x-wise, it will span left and right to the maximum
      left and right of the spans in such a clip. The first
      clip was as wide as the table. Accordingly, at this stage,
      it may be wider or smaller than the initial clip.

    :param top_row_y1_coord: float: select the last row's y1 coordinate
        .i.e this is the topmost row, since the rows (candidate header
        rows) are ordered from bottom to top.
    '''
    _nclip = EMPTY_RECT()

    # Walk the spans above the current table and
    # select the spans above the table within
    # max 5 lines above the table
    _spans_above_table: Generator[dict, Any, Any] = (
        _span
        for _span in spans_above_table
        # Keep it only if the current span's y1 is
        # above or equal (i.e. lower geometrically) than the
        # last (the topmost) row's y1 coordinate
        if _span["bbox"][3] >= top_row_y1_coord
    )

    # Walk the remaining spans and build the new clip
    # above the table from them
    #
    # update the Rect with each span's bbox
    for _span in _spans_above_table:
        _nclip |= _span["bbox"]

    # If the clip is valid, assign the new clip
    # to the passed-in clip_above_table
    if not _nclip.is_empty:
        clip_above_table = _nclip

        # make sure we still include every word above
        # -> we extend the y1 of the clip_above_table to the top of the table
        clip_above_table.y1 = first_row_bbox_y0

    # Return the passed-in clean, eventually modified
    return clip_above_table


def _get_span_properties(span) -> tuple[float, float, int]:
    '''
    Return a tuple with the span's y1, its height and whether is is bold.
    '''
    _span_y1: float = span["bbox"][3]
    # span bbox height
    _span_height: float = _span_y1 - span["bbox"][1]
    _span_is_bold: int = span["flags"] & 16

    return _span_y1, _span_height, _span_is_bold


def _update_row_property_lists(
    row_y1_coords,
    row_heights,
    row_bolds,
    span_y1,
    span_height,
    span_is_bold,
) -> None:
    '''
    Update the row property lists.
    '''
    row_y1_coords.append(span_y1)
    row_heights.append(span_height)
    row_bolds.append(span_is_bold)


def _is_current_span_more_or_less_fitting_inside_prev_row(
    y1_gap: float,
    y_delta: float,
    prev_row_y1: float,
    prev_row_height: float,
    curr_span_y0: float,
) -> bool:
    '''
    Test whether the current span is fitting within the previous
    row's row (in terms of height).
    '''
    return (
        # if the _y1_gap between this spans and the previous one
        # is below _y_delta tolerance (default to 3 pts)
        (y1_gap <= y_delta)
        # or if the difference between the previous row top y
        # (_prev_row_y1 - _prev_row_height) and this spans's top y
        # is below the _y_delta tolerance
        or (abs((prev_row_y1 - prev_row_height) - curr_span_y0) <= y_delta)
    )


def _adjust_span_bbox_to_row_dimensions(
    span: dict,
    prev_row_y1: float,
    prev_row_height: float,
):
    # modify bbox
    span["bbox"] = (
        span["bbox"][0],
        prev_row_y1 - prev_row_height,
        span["bbox"][2],
        prev_row_y1,
    )
    return span


def _is_gap_between_span_and_row_too_large(
    prev_row_y1: float,
    prev_row_height: float,
    span_y1: float,
) -> bool:
    return (prev_row_y1 - span_y1) > (1.5 * prev_row_height)


def _fill_in_lines_above_properties_list(
    spans: list[dict],
    row_y1_coords: list[float],
    row_heights: list[float],
    row_bolds: list[int],
    y_delta: float,
) -> None:
    '''
    Walks the spans above the current table and fills in the
    row_y1_coords, row_heights and row_bolds properties list.
    '''
    for i in range(len(spans)):

        _span: dict = spans[i]
        _span_y1, _span_height, _span_is_bold = _get_span_properties(_span)

        # use first span to start the lists of rows properties
        if i == 0:
            _update_row_property_lists(
                row_y1_coords,
                row_heights,
                row_bolds,
                _span_y1,
                _span_height,
                _span_is_bold,
            )
            continue

        # get last items from the 3 lists
        # i.e. the row above this span
        _prev_row_y1 = row_y1_coords[-1]
        _prev_row_height = row_heights[-1]
        _prev_row_bold = row_bolds[-1]

        # stop if switching from bold to non-bolds
        if _prev_row_bold and not _span_is_bold:
            break  # stop if switching from bold to non-bold

        # compute the y1 gap between the previous row y1 and this span's y1
        # NOTE: _prev_row_y1 shall in principle always be greater that _span_y1
        # => _y1_gap is always positive
        _y1_gap: float = _prev_row_y1 - _span_y1

        # if fitting in height of previous row, modify span's bbox
        if _is_current_span_more_or_less_fitting_inside_prev_row(
            _y1_gap, y_delta, _prev_row_y1, _prev_row_height, _span["bbox"][1]
        ):
            # update the current span in the spans list
            spans[i] = _span = _adjust_span_bbox_to_row_dimensions(
                _span, _prev_row_height, _prev_row_y1
            )
            # if this span is bold, consider the whole list as bold
            if _span_is_bold:
                row_bolds[-1] = _span_is_bold
            continue

        # stop if distance to previous line too large
        elif _is_gap_between_span_and_row_too_large(
            _prev_row_y1, _prev_row_height, _span_y1
        ):
            break  # stop if distance to previous line too large

        # update the three lists
        _update_row_property_lists(
            row_y1_coords,
            row_heights,
            row_bolds,
            _span_y1,
            _span_height,
            _span_is_bold,
        )


def _does_any_word_intersect_with_any_col(
    col_x_coords: list[float],
    word_rects: list[Rect],
    current_word_row_top_y: float,
) -> bool:
    '''
    Check if any of the words in the word_rects Rectangles
    list intersects with any column x coordinate.

    At this stage, the col_x_coords are the columns coordinates
    of the topmost row of the table, which may contain None cells.
    '''

    # compute intersecting list
    #
    # Compute list of words from the current row which DO
    # INTERSECT with one of the column
    _intersecting = [
        (_col_x_coord, _rect)
        # For each x coordinate of each column
        for _col_x_coord in col_x_coords
        # Check only for non-None cells
        if _col_x_coord is not None
        # For each word
        for _rect in word_rects
        # Keep only words which:
        # - are on the current row of words
        # - intersect with one of the column
        if (
            # 1. their top edge (y0 coordinates) of the current word
            # is equal to current row of words; and
            _rect[1] == current_word_row_top_y
            # 2. their x0 coordinate (_rect[0]) is below the
            # current column x coordinate
            and _rect[0] < _col_x_coord
            # 3. their x0 coordinate (_rect[0]) is above the
            # current column x coordinate
            and _rect[2] > _col_x_coord
        )
    ]

    # Check if the list is not empty
    # Return False if the list is empty (no intersections)
    # Return True if any word intersects with one of the columns
    # (words are free to go into None cells)
    return _intersecting != []


def _select_candidate_headers(
    col_x_coords: list[float],
    word_y0s: list[float],
    word_rects: list[Rect],
) -> list[float]:
    '''
    Select the candidate headers by eliminating all the rows where a word
    that overlaps with one of the non-None columns and ordering them in
    rows of words from the closest to the table to the furthest.

    :param col_x_coords: list[float]: the columns' inner x coordinates,
        except for None cells.
    '''

    _candidate_hdrs_y0s: list[float] = []

    # Walk the words y0 coordinates
    # => by rows, from top of table to top of the page
    # => for each row of words:
    #
    for _word_row_top_y in word_y0s:

        # If any word in this row intersects with any of the non-None
        # column, break
        # -> do not go any further: we do not want any row where
        # words intersect with the last row columns. We've probably
        # reached the end of the table going upwards.
        if _does_any_word_intersect_with_any_col(
            col_x_coords=col_x_coords,
            word_rects=word_rects,
            current_word_row_top_y=_word_row_top_y,
        ):
            break

        else:

            # Else: none of the words in this row intersect with any of the
            # non-None column
            #
            # Append this row's y0 to the list of rows candidates
            _candidate_hdrs_y0s.append(_word_row_top_y)

    # We now have all the non-intersecting rows y0 coordinates
    # => top edge of the header
    return _candidate_hdrs_y0s


def _get_properties_of_rows_above_table(
    spans: list,
    y_delta: float,
) -> tuple[list[float], list[float], list[int]]:
    '''
    Collect the properties of the rows above the table
    and returns them under the form of three parallel
    lists.

    Returns a list of rows y1 coordinates, a list of rows' height
    and a list of row bold property (0 or 16).
    '''

    # _select: list[float] = []  # y1 coordinates above, sorted descending
    _row_y1_coords: list[float] = []
    _row_heights: list[float] = []  # line heights above, sorted descending
    _row_bolds: list[int] = []  # bold indicator per line above, same sorting

    # spans sorted descending (from larger to smaller
    # i.e. from bottom to top), by y1 (bottom y)
    spans.sort(key=lambda _span: _span["bbox"][3], reverse=True)

    # walk through the spans and fill above 3 lists
    # walk through the spans and fill the 3 lists
    _fill_in_lines_above_properties_list(
        spans=spans,
        row_y1_coords=_row_y1_coords,
        row_heights=_row_heights,
        row_bolds=_row_bolds,
        y_delta=y_delta,
    )

    return _row_y1_coords, _row_heights, _row_bolds


def _is_first_candidate_row_too_far_away(
    first_table_row_y0: float,
    first_hdr_candidate_y0: float,
    first_row_height: float,
) -> bool:
    return first_table_row_y0 - first_hdr_candidate_y0 >= first_row_height


def _complete_cell_coordinates_with_left_alignment_of_None_cells(
    hdr_bbox: Rect,
    merged_cells_x_coords: list[float | None],
) -> None:

    # Take the right most edge
    _last_coord: float = hdr_bbox.x1

    # Walk the x coordinates, back to front, except the last one
    # (right edge) and the first one (left edge)
    for _idx in range(-2, -len(merged_cells_x_coords), -1):

        _coord: float | None = merged_cells_x_coords[_idx]

        # If the coordinate is a None, replace it with the
        # rightmost preceeding coordinate.
        # This way, None cells will have a bbox with the
        # same x0 and x1 coordinates.
        if _coord is None:
            merged_cells_x_coords[_idx] = _last_coord

        # Else: there's a value for the _coord.
        # Do not change the list.
        # Update the _last_coord for the following iterations
        # if a None cell appears
        else:
            _last_coord = _coord


def _compute_hdr_cells(
    table_first_row_cells: list[tuple[float, float, float, float]],
    hdr_bbox: Rect,
) -> list[tuple[float, float, float, float]]:
    '''
    Computes the header cells.
    '''
    # Build a maximum cells row with only the x-coordinates
    # of the columns, which may be None if some of the first row's
    # cells have been noned.
    _merged_cells_x_coords: list = (
        # Initialize with the table's left edge
        [hdr_bbox.x0]
        + [
            # Get the cell's right edge or None
            None if _cell is None else _cell[2]
            # Do not consider the last cell
            for _cell in table_first_row_cells[:-1]
        ]
        # for the last cell right edge, we take the columns' right edge
        + [hdr_bbox.x1]
    )

    # NOTE: _merged_cells_x_coords is one item longer than the cells' count

    # We now have a list of the columns' x coordinates, with
    # some of them filled with a None value
    # The following function will replace None value by the
    # closest right float value.
    _complete_cell_coordinates_with_left_alignment_of_None_cells(
        hdr_bbox=hdr_bbox,
        merged_cells_x_coords=_merged_cells_x_coords,
    )

    # Build the hdr_cells list of bboxes
    return [
        (_left_x, hdr_bbox.y0, _right_x, hdr_bbox.y1)
        for _left_x, _right_x in zip(
            _merged_cells_x_coords[:-1], _merged_cells_x_coords[1:]
        )
    ]


def _compute_hdr_bbox_and_cells(
    table_bbox: tuple[float, float, float, float],
    table_first_row_cells: list[tuple[float, float, float, float]],
    candidate_hdrs_y0s: list[float],
) -> tuple[Rect, list[tuple[float, float, float, float]]]:
    '''
    Computes the header cells and bbox from the passed in:
    - table bbox
    - clip above the table
    - first rows cells
    - candidate header (above-rows non-overlapping the columns)
    '''
    # - hdr_bbox's top is smallest top coord of words. The header
    # top y is equal to the smallest (geometrically highest)
    # y coordinate in the list of non-intersecting rows.
    # - left/right of header bbox are those of the table bbox
    _hdr_bbox: Rect = Rect(
        table_bbox[0], candidate_hdrs_y0s[-1], table_bbox[2], table_bbox[1]
    )

    # Build the hdr_cells bboxes
    _hdr_cells: list[tuple[float, float, float, float]] = _compute_hdr_cells(
        table_first_row_cells=table_first_row_cells,
        hdr_bbox=_hdr_bbox,
    )

    # build a list of hdr_cells' bboxes
    # _hdr_cells: list[tuple[float, float, float, float]] = [
    #     (
    #         (_cell[0], _hdr_bbox.y0, _cell[2], _hdr_bbox.y1)
    #         if _cell is not None
    #         else None
    #     )
    #     for _cell in table_first_row_cells
    # ]

    return _hdr_bbox, _hdr_cells


def _validate_header_candidate(
    hdr_bbox: Rect,
    hdr_cells: list[tuple[float, float, float, float]],
    spans_above_table: list[dict],
) -> bool:
    '''

    :param hdr_bbox: Rect: the header's bbox.

    :param hdr_cells: list[tuple[float, float, float, float]]: the list
        of potential header cells.

    :param spans_above_table: list[dict]: the spans above the table.

    '''
    # 1. Select the spans that are within the hdr_bbox
    _spans_in_hdr: Generator[dict, Any, Any] = (
        _span
        for _span in spans_above_table
        if _is_inside_bbox(_span['bbox'], hdr_bbox)
    )

    # 2. Real header bbox
    _nrect: Rect = EMPTY_RECT()

    for _span in _spans_in_hdr:
        _nrect |= _span["bbox"]

    # 3. Do not validate header which occupy only the first cell
    if _is_inside_bbox(tuple(_nrect), Rect(hdr_cells[0])):

        return False

    return True


def _get_candidate_hdr_rows_y0_coords(
    page: Page,
    textpage: TextPage,
    table_first_row_bbox: Rect,
    table_first_row_cells: list[tuple[float, float, float, float]],
    clip_above_table: Rect,
    spans_above_table: list[dict],
    candidate_hdr_y1_coords: list[float],
) -> list[float]:
    '''
    Compute the header rows candidate y0 coordinates, from bottom
    to top.
    '''
    # re-compute clip above table:
    # y-wise, it will go max 5 lines up (instead of to the top)
    # x-wise, as wide as the spans it contains (instead of table-wide)
    _clip_above_table: Rect = _recompute_clip_above_table(
        spans_above_table=spans_above_table,
        # only accept up to 5 lines in any header
        top_row_y1_coord=candidate_hdr_y1_coords[:5][-1],
        clip_above_table=clip_above_table,
        first_row_bbox_y0=table_first_row_bbox.y0,
    )

    # -----------------------------------------------------------
    # Confirm that no word in clip is intersecting a column separator
    #
    # Make a list of the Rectangles of the words living above
    # the table
    # -----------------------------------------------------------

    # Get a list of the bboxes of the words above the table
    # word_rects = list of bboxes
    _word_rects: list[Rect] = [
        Rect(_word[:4])
        # NOTE: this is the old code:
        # for w in page.get_text("words", clip=clip)
        # The new code gives a better result, correcting an
        # error where a row was considered a header row when it was not
        for _word in page.get_text(
            "words", textpage=textpage, clip=_clip_above_table
        )
    ]

    # From _word_rects (the list of words rectangles),
    # get a list of the words unique y0 (top y)
    # coordinates, sorted by y0 in descending order
    # (from bottom of the page to the top)
    _word_tops: list[float] = sorted(
        # this gets a set of unique y0 for the words
        {_rect[1] for _rect in _word_rects},
        # from bottom to top
        reverse=True,
    )

    # -----------------------------------------------------------
    # Make a list of the columns x coordinates.
    # We compute it using the cells of the first row.
    # These coords will be used to compute intersections with words
    # found in row candidates later on.
    # -----------------------------------------------------------

    # Get the x-coordinates of columns between x0 and x1 of the table
    # i.e. only the x-coords between the table's x0 and x1, excluding
    # the table's outer edges
    _col_x_coords: list[float] = [
        _cell[2] if _cell is not None else None
        for _cell in table_first_row_cells[:-1]
    ]

    # Inspect whether any of the retained words intersects a
    # column border
    # Select candidate headers and return their y0
    _candidate_hdrs_y0s: list[float] = _select_candidate_headers(
        col_x_coords=_col_x_coords,  # only non-None cols coordinates
        word_y0s=_word_tops,  # dependent on _clip_above_table
        word_rects=_word_rects,  # dependent on _clip_above_table
    )

    return _candidate_hdrs_y0s


def _compute_complex_header(
    page: Page,
    textpage: TextPage,
    table_bbox: tuple[float, float, float, float],
    table_first_row_bbox: Rect,
    table_first_row_cells: list[tuple[float, float, float, float]],
    table_cols_inner_coords: list[float],
    clip_above_table: Rect,
    spans_above_table: list[dict],
    row_abv_y1_coords: list[float],
    header_top_row_func: Callable,
) -> TableHeader:
    '''
    Compute a table header if the table header could not be
    determined otherwise and there are potential header row
    candidates.

    Uses the potential header rows candidates to try and
    make some tables.
    '''

    # We select the candidate inside _get_candidate_hdr_rows_y0_coords
    # function; the returning list is empty or contains the y0 coordinate
    # of one or several candidate external header rows
    #
    # As currently drafted, both _candidate_hdrs_y0s and _clip_above_table
    # are restricted in width to the table's top column width and structure.
    # Candidate header must not contain any word that intersect
    # with one of the columns of the last row.
    #
    # NOTE: at this stage, no efforts is made (nor shall be made) to try
    # and identify (resurecting) columns within the header
    # However, we might want to enlarge the _clip_above_table to the table
    # width.
    _candidate_hdrs_y0s = _get_candidate_hdr_rows_y0_coords(
        page=page,
        textpage=textpage,
        table_first_row_bbox=table_first_row_bbox,
        table_first_row_cells=table_first_row_cells,
        clip_above_table=clip_above_table,
        spans_above_table=spans_above_table,
        candidate_hdr_y1_coords=row_abv_y1_coords,
    )

    # No header candidates
    # -----------------------------------------------------------

    # None of the rows above has been retained a header candidate:
    # - there was no row above, or
    # - all rows above contained word intersection columns
    # => in this case, we return the first line of the table as header row.
    if _candidate_hdrs_y0s == []:  # nothing left over: return first row
        return header_top_row_func()

    # compute the header bbox and cells
    _hdr_bbox, _hdr_cells = _compute_hdr_bbox_and_cells(
        table_bbox=table_bbox,
        table_first_row_cells=table_first_row_cells,
        candidate_hdrs_y0s=_candidate_hdrs_y0s,
    )

    # Validate header: if header candidates only has words inside
    # the left most cell and none in the right most cells, this is
    # not a header
    if not _validate_header_candidate(
        hdr_bbox=_hdr_bbox,
        hdr_cells=_hdr_cells,
        spans_above_table=spans_above_table,
    ):
        return header_top_row_func()

    # column names: no line breaks, no excess spaces
    _hdr_names: list[str] = [
        (
            # NOTE: Passing the textpage as parameter seems to work and reduce
            # significantly the parsing time. But not yet sure this works.
            # page.get_textbox(c).replace("\n", " ").replace("  ", " ").strip()
            page.get_textbox(_hdr_cell, textpage=textpage)
            .replace("\n", " ")
            .replace("  ", " ")
            .strip()
            if _hdr_cell[0] != _hdr_cell[2]
            else ""
        )
        for _hdr_cell in _hdr_cells
    ]

    # If no text was found in the zone of the cells, return the first row
    # as header
    if all(_hdr_name == '' for _hdr_name in _hdr_names):
        return header_top_row_func()

    return TableHeader(tuple(_hdr_bbox), _hdr_cells, _hdr_names, True)


def _return_table_first_row_as_table_header_row(
    table_first_row_bbox: Rect,
    table_first_row_cells: list[tuple[float, float, float, float]],
    extract_method: Callable,
) -> TableHeader:
    '''Returns the first row of the table packaged as a TableHeader.

    extract_method: Callable: a callable able to extract the text
        content of the first row of the table.
    '''
    _header_top_row: TableHeader = TableHeader(
        bbox=table_first_row_bbox,
        cells=table_first_row_cells,
        # Get the first row of the table
        names=extract_method()[0],
        # Whether the header is above (and external to)
        # the table or the first row has been used
        # as header
        above=False,
    )

    return _header_top_row


def new_get_table_header(
    page: Page,
    textpage: TextPage,
    table_rows: list,  # a list of TableRows
    table_cols_inner_coords: list[float],
    extract_method: Callable,
    table_bbox: tuple[float, float, float, float],
    blocks: list[dict],
    y_tolerance: float = 3,
) -> TableHeader | None:
    """Identify the table header.

    Copy of `get_table_header` with one additional parameter textpage.

    *** PyMuPDF extension. ***

    Starting from the first line above the table upwards, check if it
    qualifies to be part of the table header.

    Returns a TableHeader | None or the first row if first row has been
    determined to be a header.

    Criteria include:
    * A one-line table never has an extra header.
    * Column borders must not intersect any word. If this happens, all
        text of this line and above of it is ignored.
    * No excess inter-line distance: If a line further up has a distance
        of more than 1.5 times of its font size, it will be ignored and
        all lines above of it.
    * Must have same text properties.
    * Starting with the top table line, a bold text property cannot change
        back to non-bold.

    If not all criteria are met (or there is no text above the table),
    the first table row is assumed to be the header.
    """
    _y_delta: float = y_tolerance

    # Try to get:
    # - the list of cells of the table
    # - first rows bbox
    try:
        _table_first_row = table_rows[0]
        # the cells of the first row: a list of bboxes
        _table_first_row_cells: list[tuple[float, float, float, float]] = (
            _table_first_row.cells
        )
        # the first row's rectangle
        _table_first_row_bbox: Rect = Rect(_table_first_row.bbox)
    except IndexError:  # this table has no rows
        return None

    # -----------------------------------------------------------

    # Define a partial to return the first row as table header
    _ret_1st_row_as_tbl_hdr_part: partial = partial(
        _return_table_first_row_as_table_header_row,
        _table_first_row_bbox,
        _table_first_row_cells,
        extract_method,
    )

    # one-line tables have no extra header
    # tables starting with only one cell do not have extra header
    # one-cell tables have no extra header
    if _is_table_one_liner(
        table_rows=table_rows, first_row_cells=_table_first_row_cells
    ):

        # Return the header row
        return _ret_1st_row_as_tbl_hdr_part()

    # clip = area above table
    # We will inspect this area for text qualifying as column header.

    # collect the spans above the table
    # -----------------------------------------------------------

    _clip_above_table, _spans_above_table = (
        _compute_clip_get_spans_above_table(
            table_bbox,
            blocks,
        )
    )

    # if there is nothing above the current table, interrupt now
    # and return the first row as header
    if _spans_above_table == []:

        # Return the header row
        return _ret_1st_row_as_tbl_hdr_part()

    # collect properties of the rows made from the extracted spans
    # -----------------------------------------------------------

    _row_abv_y1_coords, _row_abv_heights, _row_abv_bolds = (
        _get_properties_of_rows_above_table(
            _spans_above_table,
            _y_delta,
        )
    )

    # take top row as header
    # -----------------------------------------------------------

    # if there is nothing above the current table
    if _row_abv_y1_coords == []:  # nothing above the table?

        return _ret_1st_row_as_tbl_hdr_part()

    # if text above table is too far apart
    #

    # If first candidate row to far away, return the first
    # line of the table as header
    if _is_first_candidate_row_too_far_away(
        first_table_row_y0=_table_first_row_bbox.y0,
        first_hdr_candidate_y0=_row_abv_y1_coords[0],
        first_row_height=_row_abv_heights[0],
    ):

        return _ret_1st_row_as_tbl_hdr_part()

    # if top table row is bold, but line above is not
    # Special check: is top row bold?
    # We check if any of the spans living in the row above
    # the table is bold. If so, we consider the line as
    # bold.
    _top_row_bold: bool = _is_table_top_row_bold(
        blocks=blocks,
        bbox=_table_first_row_bbox,
    )

    if _top_row_bold and not _row_abv_bolds[0]:

        return _ret_1st_row_as_tbl_hdr_part()

    # -----------------------------------------------------------
    # Else:
    # - we've got something above the table
    # - the first line of table is not bold
    # - text above table is not too far away
    # -----------------------------------------------------------

    # We have one or more rows above the table as header candidates
    # -----------------------------------------------------------

    return _compute_complex_header(
        page=page,
        textpage=textpage,
        table_bbox=table_bbox,
        table_first_row_bbox=_table_first_row_bbox,
        table_first_row_cells=_table_first_row_cells,
        table_cols_inner_coords=table_cols_inner_coords,
        clip_above_table=_clip_above_table,
        spans_above_table=_spans_above_table,
        row_abv_y1_coords=_row_abv_y1_coords,
        # passed the top row of the table as TableHeader
        # for the case the complex header ends up being
        # the first row of the table
        header_top_row_func=_ret_1st_row_as_tbl_hdr_part,
    )
