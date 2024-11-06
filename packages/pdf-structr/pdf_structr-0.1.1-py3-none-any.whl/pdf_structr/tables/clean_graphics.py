# clean_graphics.py
'''
Encapsulation of subfunctions for table_make_edges module.
'''

# from functools import partial
# from typing import Any, Generator


from pymupdf import (  # type: ignore
    Page,
    Rect,
    TextPage,
)

from pdf_structr.tables.table_funcs import (
    white_spaces,
)

# -------------------------------------------------------------------
# clean_graphics stack
# -------------------------------------------------------------------


def are_neighbors(r1, r2, snap_x, snap_y):
    """Detect whether r1, r2 are neighbors.

    Defined as:
    The minimum distance between points of r1 and points of r2 is not
    larger than some delta.

    This check supports empty rect-likes and thus also lines.

    Note:
    This type of check is MUCH faster than native Rect containment checks.
    """
    if (  # check if x-coordinates of r1 are within those of r2
        # r2[0] - snap_x <= r1[0] <= r2[2] + snap_x
        # or r2[0] - snap_x <= r1[2] <= r2[2] + snap_x
        r2.x0 - snap_x <= r1.x0 <= r2.x1 + snap_x
        or r2.x0 - snap_x <= r1.x1 <= r2.x1 + snap_x
    ) and (  # ... same for y-coordinates
        # r2[1] - snap_y <= r1[1] <= r2[3] + snap_y
        # or r2[1] - snap_y <= r1[3] <= r2[3] + snap_y
        r2.y0 - snap_y <= r1.y0 <= r2.y1 + snap_y
        or r2.y0 - snap_y <= r1.y1 <= r2.y1 + snap_y
    ):
        return True

    # same check with r1 / r2 exchanging their roles (this is necessary!)
    if (
        # r1[0] - snap_x <= r2[0] <= r1[2] + snap_x
        # or r1[0] - snap_x <= r2[2] <= r1[2] + snap_x
        r1.x0 - snap_x <= r2.x0 <= r1.x1 + snap_x
        or r1.x0 - snap_x <= r2.x1 <= r1.x1 + snap_x
    ) and (
        # r1[0] - snap_y <= r2[0] <= r1[2] + snap_y
        # or r1[0] - snap_y <= r2[2] <= r1[2] + snap_y
        r1.y0 - snap_y <= r2.y0 <= r1.y1 + snap_y
        or r1.y0 - snap_y <= r2.y1 <= r1.y1 + snap_y
    ):
        return True
    return False


def _make_paths_list_in_strict_mode(
    drawings: list[dict],
    snap_x: float,
    snap_y: float,
) -> list[dict]:
    '''
    In lines_strict mode, ignore fill-only graphics if they
    do not simulate lines, which means one of width or height
    is small.
    '''

    return [
        p
        for p in drawings
        # in lines_strict mode, ignore fill-only graphics if they
        # do not simulate lines, which means one of width or height
        # are small.
        if not (
            p["type"] == "f"
            # and (p["rect"][2] - p["rect"][0]) > snap_x
            # and (p["rect"][3] - p["rect"][1]) > snap_y
            and p["rect"].width > snap_x
            and p["rect"].height > snap_y
        )
    ]  # paths relevant for table detection


def _extend_rect_delete_rect(
    prect0,
    prect1,
    prects_dq,
    i,
):
    '''
    Extends the current rectangle by another rectangle and deletes
    the rectangle by which the extension has been made from the deque
    of Rectangles.
    '''
    prect0 |= prect1.tl  # extend rect 0
    prect0 |= prect1.br  # extend rect 0

    del prects_dq[i]  # delete this rect

    return prect0


def _compare_join_delete(
    prects_dq,
    prect0,
    snap_x,
    snap_y,
    repeat,
) -> tuple[Rect, bool]:
    '''
    Walk the initial rectangle deque, back to front, and tries
    to extend the current rectangle if it touches one of the
    rectangles in the deque.

    In such case, also deletes the merged rectangle from the list
    and turns the repeat witness to True.
    '''
    for i in range(len(prects_dq) - 1, 0, -1):  # run backwards

        prect1 = prects_dq[i]

        if are_neighbors(
            prect0, prect1, snap_x, snap_y
        ):  # close enough to rect 0?
            prect0 = _extend_rect_delete_rect(prect0, prect1, prects_dq, i)
            repeat = True  # keep checking the rest

    return prect0, repeat


def _compare_join_delete_wrapper(
    prects_dq,
    prect0,
    snap_x,
    snap_y,
) -> None:
    '''
    While the current rectangle has touched another rectangle
    and has been extended, this will iterate on the remaining
    rectangles to try to extend the current rectangle again
    until it does not touch any other rectangle.
    '''

    repeat = True

    while repeat:  # this loop extends first rect in list

        repeat = False  # set to true again if some other rect touches

        prect0, repeat = _compare_join_delete(
            prects_dq,
            prect0,
            snap_x,
            snap_y,
            repeat,
        )


# @count_and_avg_timer(name='prep - _make_joined_rects_list')
def _make_joined_rects_list(
    page: Page,
    textpage: TextPage,
    prects: list[Rect],
    snap_x: float,
    snap_y: float,
) -> list[Rect]:
    '''
    Strategy: Join rectangles that "almost touch" each other.
    Extend first rectangle with any other that is a "neighbor".
    Then move it to the final list and continue with the rest.
    '''

    new_rects: list[Rect] = []  # the final list of joined rectangles

    from collections import deque

    _prects_dq: deque = deque(prects)

    while _prects_dq:  # the algorithm will empty this list
        # copy of first rectangle (performance reasons!)
        prect0 = _prects_dq[0]
        # compare the current rect with the rects of the list
        # and try to extend the rect while deleting elements
        # from the list
        _compare_join_delete_wrapper(
            _prects_dq,
            prect0,
            snap_x,
            snap_y,
        )

        # add the current rectangle to the new rectangles' list
        new_rects += [prect0]

        # remove the current rectangle from the initial rect deque
        _prects_dq.popleft()

    # filter out rect covering white space
    new_rects = [
        _rect
        for _rect in new_rects
        if not white_spaces.issuperset(
            page.get_text('text', clip=_rect, textpage=textpage)
        )
    ]

    return new_rects


# @count_and_avg_timer(name='prep - clean_graphics')
def clean_graphics(
    page: Page,
    textpage: TextPage,
    drawings: list[dict],
    lines_strict: bool,
    snap_x: float,
    snap_y: float,
) -> tuple[list[Rect], list[dict]]:
    """
    Detect and join rectangles of "connected" vector graphics.

    NOTE: compared to the pymupdf version, we're passing-in the textpage
    and the drawings which have been previously extracted.

    :param page: Page: the current Page.

    :param textpage: TextPage: the current TextPage.

    :param drawings: the page drawings as returned by page.drawings().

    :param lines_strict: bool: whether we're in 'lines_strict' table
        detection strategy.

    :param snap_x: float: a float to be used as max horizontal thresholds
        for proximity between Rectangles for joining them.

    :param snap_y: float:  a float to be used as max vertical thresholds
        for proximity between Rectangles for joining them.
    """

    # ---------------------------
    # Filter the drawing dicts if we're in 'lines_strict' strategy
    # ---------------------------

    paths: list[dict] = []

    if lines_strict:
        paths = _make_paths_list_in_strict_mode(
            drawings,
            snap_x,
            snap_y,
        )

    else:
        paths = drawings

    # for p in drawings:
    #     # ignore fill-only graphics if they do not simulate lines,
    #     # which means one of width or height are small.
    #     if (
    #         p["type"] == "f"
    #         and lines_strict
    #         and p["rect"].width > snap_x
    #         and p["rect"].height > snap_y
    #     ):
    #         continue
    #     paths.append(p)

    # start with all vector graphics rectangles
    # sort them by bottom y and left x
    prects: list[Rect] = sorted(
        {p["rect"] for p in paths}, key=lambda r: (r.y1, r.x0)
    )
    # prects: list[tuple[float, float, float, float]] = (
    #     sorted({p["rect"] for p in paths}, key=lambda r: (r[3], r[0]))
    # )

    # the final list of joined rectangles
    new_rects: list[Rect] = _make_joined_rects_list(
        page,
        textpage,
        prects,
        snap_x,
        snap_y,
    )

    return new_rects, paths
