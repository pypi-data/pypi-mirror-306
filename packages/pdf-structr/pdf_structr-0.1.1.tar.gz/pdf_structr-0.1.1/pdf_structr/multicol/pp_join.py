# pp_join.py
"""
Module to encapsulate the post-processing rectangles joining
functions for multi_column.
"""

import logging

from pymupdf import IRect, Rect  # type: ignore

from pdf_structr.utils.utils import in_bbox

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
# Join rectangles stack
#####################


def join_rects_phase1(bboxes: list[IRect]) -> list[IRect]:
    """
    Postprocess identified text blocks, phase 1.

    Joins any rectangles that "touch" each other. This means that
    their intersection is valid (but may be empty).

    To prefer vertical joins, we will ignore small horizontal gaps.
    """
    # allow this gap below - this is probably
    # a parameter to be passed-in
    delta: tuple = (0, 0, 0, 2)

    # make a copy of the detected text rectangles list
    prects: list[IRect] = bboxes[:]

    # declare a new list of rectangle (return list)
    _new_rects: list[IRect] = []

    # walk the copy of the detected text rectangles list in ascending order
    while prects:

        # at each iteration, get the first rectangle in the list
        # as it has been deleted at the end of the code nested into
        # the `while`, this is always the next rectangle in the list
        prect0: IRect = prects[0]
        # declare a sentinel and set it to True
        repeat: bool = True
        # while the sentinel is True
        while repeat:
            # switch the sentinel to False
            repeat = False

            # walk the remaining rectangle in reverse order
            # (because where deleting)
            for i in range(len(prects) - 1, 0, -1):

                # if the prect0 + delta intersects with the current
                # prect:
                # -> join both rectangles and delete the current
                # rectangle
                if not ((prect0 + delta) & (prects[i])).is_empty:

                    # join the rectangles
                    prect0 |= prects[i]

                    # delete the current rectangle
                    # NOTE: we might be deleting in the middle of
                    # the list... Not so sensitive as the list
                    # shall not be that large, but nevertheless..
                    del prects[i]

                    # Switch the sentinel to True to repeat the first
                    # inner loop (the while loop)
                    repeat = True

        # Once the sentinel has been turned to false (i.e. all the
        # remaining rectangles have been either (i) joined to the first
        # rectangle and deleted from the initial list or (ii) left in the
        # list if they do not form a valid rectangle with the first one),
        # - append the first rectangle to the return list and delete the
        # the first rectangle
        # - walk the remaining rectangles' list (if any)
        _new_rects.append(prect0)

        # NOTE: Deleting at the beginning of a list...
        del prects[0]

    # return the list of 'concatenated' text rectangles
    return _new_rects


def join_rects_phase2(bboxes: list[IRect]) -> list[IRect]:
    """
    Postprocess identified text blocks, phase 2.

    Increase the width of each text block so that small left or right
    border differences are removed. Then try to join even more text
    rectangles.
    """
    # copy of argument list
    _prects: list[IRect] = bboxes[:]

    # `xs rounding up`
    # ----------------

    # walk the copy of the rectangle's list (argument list) in ascending
    # order and slightly increase the left and right borders of the
    # rectangles compared to the others
    for _i in range(len(_prects)):
        # get the current rectangle
        _current_rect: IRect = _prects[_i]

        # go left and right somewhat
        # go left somewhat if any one of the other rectangles has a left border
        # slightly left to this one
        _x0: int = min(
            [_bb.x0 for _bb in _prects if abs(_bb.x0 - _current_rect.x0) <= 3]
        )
        # go right somewhat if one of the other rectangles has a right border
        # slightly right to this one
        _x1: int = max(
            [_bb.x1 for _bb in _prects if abs(_bb.x1 - _current_rect.x1) <= 3]
        )
        # update new left / right border
        _current_rect.x0 = _x0
        _current_rect.x1 = _x1
        # store new left / right border
        _prects[_i] = _current_rect

    # `xs rounding up` completed
    # ----------------

    # joining if we have similar borders and are not too far down
    # ----------------

    # sort by left, top
    _prects.sort(key=lambda b: (b.x0, b.y0))

    # declare a return list and
    # initialize with first item (first text rectangle)
    _new_rects: list[IRect] = [_prects[0]]

    # walk through the rest, top to bottom, then left to right
    for _r in _prects[1:]:
        # previous bbox
        _r0: IRect = _new_rects[-1]

        # join if we have similar borders and are not to far down
        if (
            abs(_r.x0 - _r0.x0) <= 3
            and abs(_r.x1 - _r0.x1) <= 3
            # NOTE: the following param (12) might need to be adjusted
            # depending on the font size
            and abs(_r0.y1 - _r.y0) <= 12
        ):
            # extend the previous bbox
            _r0 |= _r
            # store the extended previous bbox in the return list
            _new_rects[-1] = _r0
            continue

        # else (the distance is above the allowed gap)
        # append this as new text block
        _new_rects.append(_r)

    return _new_rects


def _join_rects_phase3_core(
    prects: list[Rect | IRect],
    prect0: Rect | IRect,
    new_rects: list[Rect | IRect],
    i: int,
    repeat: bool,
    path_rects: list[Rect],
) -> tuple[bool, Rect | IRect]:
    '''
    Joins rectangles that are separated by a wide y gap filled with white
    space but have the same x coordinates.

    It may help, but may also have unintended consequences.

    :param prects: list[Rect | IRect]: a copy of the list of text column
        rectangles.

    :param prect0: Rect | IRect: the first item of the list of text column
        rectangles.

    :param new_rects: list[Rect | IRect]: the list of text column
        rectangles to be returned after the post-processing.

    :param i: int: the index number of the rectangle to be processed in this
        function (from back to front in the list of prects).

    :param repeat: bool: the sentinel. Starts at False.

    :param path_rects: list[Rect]: the identified vg rectangles.
    '''
    # Get the current rectangle in the list we are iterating from back to front
    # _prect1: Rect | IRect = prects[i]
    _current_rect: Rect | IRect = prects[i]

    # do not join across columns
    # If the left x of the current rectangle is located to the left
    # of the right x of the first rectangle,
    # OR
    # if the right x of the current rectangle is located to the left
    # of the left x of the first rectangle,
    #
    # pass and go to penultimate rectangle in the list we are iterating
    # from back to front.
    # If prect1 is the last (first) rectangle in the list,
    if _current_rect.x0 > prect0.x1 or _current_rect.x1 < prect0.x0:
        return repeat, prect0

    if in_bbox(prect0, path_rects) != in_bbox(_current_rect, path_rects):
        return repeat, prect0

    # Else define a temporary rectangle making the union of the first
    # rectangle in the list with the current rectangle in the innermost loop
    _temp_union: Rect | IRect = prect0 | _current_rect

    # make a set of the rectangles that this temporary union intersects
    _test: set[Rect | IRect] = {
        tuple(b) for b in (prects + new_rects) if b.intersects(_temp_union)
    }

    # make a set of the first rectangle in the list and the current rectangle
    _current_first_rect_set: set[Rect | IRect] = {
        tuple(prect0),
        tuple(_current_rect),
    }

    # If the two sets match, there is no intermediate rectangles between them
    # => we can unite these rectangles into a single one
    if _test == _current_first_rect_set:

        # extend the first rectangle
        prect0 |= _current_rect

        # delete the current rectangle from the copy of the list of rect
        del prects[i]

        # set the sentinel to True
        repeat = True

        # return the sentinel and the extended first rectangle
        return repeat, prect0

    # return the sentinel in its passed-in state as well as the
    # firts rectangle
    return repeat, prect0


def join_rects_phase3(
    bboxes: list[Rect | IRect],
    path_rects: list[IRect],
) -> list[Rect | IRect]:
    '''
    Joins rectangles that are separated by a wide y gap filled with white
    space (or table or vector graphic rectangles) and which combination
    does not cover another text rectangle.

    It helps in the cases the text has two or more columns and inside one
    of the columns, a vg/img, a table or a large white space has been
    inserted between the text blocks.

    It has unintended consequences in the case where the columns and "kind of"
    tabular, where for instance blocks of texts are organized in 2 x 2 fashion.

    :returns: the list of joined rectangles.

    :param bboxes: list[Rect | IRect]: the list of text rectangle
        bboxes detected earlier in multicolumn.

    :param path_rects: list[IRect]: the identified vg rectangles.
    '''
    # get a copy of the list of rectangles
    _prects: list[Rect | IRect] = bboxes[:]

    # declare a return list of rect
    _new_rects: list[Rect | IRect] = []

    # Iterate over the copy of the list of rectangles
    # from front to back
    while _prects:

        # Get the first rectangle in the list
        _prect0: Rect | IRect = _prects[0]

        # Declare a repeat sentinel and set it to True
        _repeat: bool = True

        # Iterate while the sentinel is True
        while _repeat:

            # Set the sentinel to False. The sentinel will be set
            # to True only if two rectangles have been joined in the
            # for loop below so the `while _repeat` will stop immediately
            # upon the first iteration in the for loop below if the two
            # rectangles are no consecutive by x0 and y0
            _repeat = False

            # Iterate on the rectangles from back to front and try to
            # join rectangles that are consecutive
            for _i in range(len(_prects) - 1, 0, -1):

                _repeat, _prect0 = _join_rects_phase3_core(
                    prects=_prects,
                    prect0=_prect0,
                    new_rects=_new_rects,
                    i=_i,
                    repeat=_repeat,
                    path_rects=path_rects,
                )

                # _repeat is True if two rectangles have been joined, else
                # it is False
                # _prect0 is the union of the two rectangles that
                # have been joined, else it is the passed-in _prect0

        # Once the while loop has completed (i.e. no intersection),
        # append the first rectangle to the return list
        _new_rects.append(_prect0)

        # and delete the first rectangle in the list
        # NOTE: popping left in a list... List is
        # supposed to be quite short, so no real overhead
        del _prects[0]

    return _new_rects


def sort_rects(
    joined_rects: list[Rect | IRect],
) -> list[Rect | IRect]:
    """
    Hopefully the most reasonable sorting sequence:
    At this point we have finished identifying blocks that wrap text.
    We now need to determine the SEQUENCE by which text extraction from
    these blocks should take place. This is hardly possible with 100%
    certainty. Our sorting approach is guided by the following thought:
    1. Extraction should start with the block whose top-left corner is the
        left-most and top-most.
    2. Any blocks further to the right should be extracted later - even if
        their top-left corner is higher up on the page.
    3. Sorting the identified rectangles must therefore happen using a
        tuple (y, x) as key, where y is not smaller (= higher up) than that
        of the left-most block with a non-empty vertical overlap.
    4. To continue "left block" with "next is ...", its sort key must be
                        Q +---------+    tuple (P.y, Q.x).
                        | next is |
            P +-------+   |  this   |
            | left  |   |  block  |
            | block |   +---------+
            +-------+

    :param: joined_rects: list[Rect | IRect]: the rectangles joined
        previously in the join_rects functions.
    """

    # Copy of "new_rects" with a computed sort key
    # _sort_rects is a list of 2-tuple Rect - sort-key, where
    # each sort-key is a 2-tuple of floats
    _sort_rects: list[tuple[Rect | IRect, tuple[float, float]]] = []

    for _new_box in joined_rects:

        # search for the left-most rect that overlaps like "P" above
        # candidates must have the same background
        # _background: int = in_bbox(_new_box, path_rects)

        _left_rects: list[Rect | IRect] = [
            _new_rect
            for _new_rect in joined_rects
            # filter out rectangles which right edge is on the
            # left of _new_box (i.e. not overlapping)
            if _new_rect.x1 < _new_box.x0
            # keep only rectangles that are overlapping vertically
            # with _new_box
            and (
                _new_box.y0 <= _new_rect.y0 <= _new_box.y1
                or _new_box.y0 <= _new_rect.y1 <= _new_box.y1
            )
            # keep only rectangles that share the same background
            # and in_bbox(_new_rect, path_rects) == _background
        ]
        # sort the retained rectangles by right edge
        _left_rects.sort(key=lambda r: r.x1)

        # _left_rects: list[Rect | IRect] = sorted(
        #     [
        #         _new_rect
        #         for _new_rect in joined_rects
        #         # filter out rectangles which right edge is on the
        #         # left of _new_box (i.e. not overlapping)
        #         if _new_rect.x1 < _new_box.x0
        #         # keep only rectangles that are overlapping vertically
        #         # with _new_box
        #         and (
        #             _new_box.y0 <= _new_rect.y0 <= _new_box.y1
        #             or _new_box.y0 <= _new_rect.y1 <= _new_box.y1
        #         )
        #         # keep only rectangles that share the same background
        #         # and in_bbox(_new_rect, path_rects) == _background
        #     ],
        #     # sort the retained rectangles by right edge
        #     key=lambda r: r.x1,
        # )

        # Set the sorting key
        _key: tuple[float, float]
        # if a "P" rectangle was found ...
        # If one or several overlapping left rectangles, the sort-key
        # will be the top y of the last overlapping rectangle
        # and the left x of the _new_box
        if _left_rects:
            # use this key
            _key = (_left_rects[-1].y0, _new_box.x0)
        # else use the original (Q.y, Q.x).
        # If no overlapping left rectangles where found, the sort-key
        # will be the top y and left x of the _new_box
        else:
            _key = (_new_box.y0, _new_box.x0)

        _sort_rects.append((_new_box, _key))

    # sort by computed key
    # Now we sort the retained rectangles by the retained sort-key
    _sort_rects.sort(key=lambda sr: sr[1])

    # extract sorted rectangles to _new_rects list
    _new_rects: list[Rect | IRect] = [sr[0] for sr in _sort_rects]

    # move shaded text rects into a separate list
    _shadow_rects: list = []

    # for i in range(len(_new_rects) - 1, 0, -1):
    #     r = +_new_rects[i]
    #     if in_bbox(r, _path_rects):  # text with shaded background
    #         _shadow_rects.insert(0, r)  # put in front to keep sequence
    #         del _new_rects[i]

    return _new_rects + _shadow_rects


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
