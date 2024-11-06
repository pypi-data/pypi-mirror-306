# make_lines_rect.py

'''
Module to store the functions making the lines' rectangles.
'''


import logging

from pymupdf import Rect  # type: ignore

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


###############################
# Subfunctions for make lines rect
###############################


def _span_is_on_the_same_line(
    span_bbox: Rect,
    line_bbox: Rect,
    y_delta: float,
) -> bool:
    '''
    Checks if this span y coordinates are within the y_delta tolerance
    to consider that it pertains to the line.

    :param span_bbox: Rect: the Rectangle of the span.

    :param line_bbox: Rect: the Rectangle of the line being built.

    :param y_delta: float: the y_delta tolerance between the span y coordinates
        and the line y coordinates as y coordinates aren't always exactly
        matching.
    '''
    return (abs(span_bbox.y1 - line_bbox.y1) <= y_delta) or (
        abs(span_bbox.y0 - line_bbox.y0) <= y_delta
    )


def _amend_span(
    span: dict[
        str,
        # flags and color
        int
        # size (fontsize), ascender and descender
        | float
        # font (fontname) and text
        | str
        # origin
        | tuple[float, float]
        # bbox
        | Rect,
    ],
    line_count: int,
) -> dict[
    str,
    # flags and color
    int
    # size (fontsize), ascender and descender
    | float
    # font (fontname) and text
    | str
    # origin
    | tuple[float, float]
    # bbox
    | Rect,
]:
    '''
    Appends the span number in line and the line number
    as new keys to the current span.

    :param append_new_line_or_amend_last_line_func: Callable: a function
        that either extends the last line's rectangle in the lines rectangle
        list with the current span's rectangle or appends the current span's
        rectangle to the list of lines' rectangles.

    :param span: dict: the current span in the iteration which is necessarily
        the first span of one of line.

    :param line_count: int: the line count, incremented on each new line
        to save in the span the number of its line under key 'raw_line_no'.

    '''
    # add index numbers to the span
    span['raw_line_no'] = line_count

    # return the span
    return span


def _amend_first_span(
    first_span: dict,
) -> dict:
    '''
    Amend the first span of the clip (by y1) and return it to initialize
    the list of amended spans.

    :param first_span: dict: the first span in the clip (by y1).
    '''
    # Add the line number to the first span
    first_span['raw_line_no'] = 0

    # Add the span number in clip to the first span
    first_span['span_no_in_clip'] = 0

    # return the span
    return first_span


###############################
# Main function for make lines rect
###############################


def make_lines_rect_and_amended_spans(
    spans: list[
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ],
    y_delta: float,
) -> tuple[
    list[  # the list of spans
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ],
    list[Rect],  # the list of lines' Rect
    int,  # the lines' count
]:
    '''
    Computes lines' rectangles, count the lines and appends various index
    numbers to the spans' dict.

    :returns:
    - the list of amended spans' dict
    - the list of lines' Rectangles
    - the lines' count

    :param spans: list[
        dict[
            str,
            int
            | float
            | str
            | tuple[float, float]
            | Rect,
        ]
    ]: the list of augmented spans for the current page.

    :param y_delta: float: put spans on the same line if their top or bottom
        coordinate differ by no more than this value.
    '''

    # Declare a line count variable
    _line_count: int = 0

    def __make_line_rect_and_amend_span(
        idx: int, span: dict, line_rects: list[Rect], y_delta: float
    ) -> dict:
        '''
        Give each span a span_no_in_clip key with its index number on the page.
        Give each span a raw_line_no.
        Create the lines' bbox Rectangle.

        :param idx: int: the index number of the span on the page.

        :param span: dict: the current span.

        :param line_rects: list[Rect]: the list of raw line's Rectangles
            currently being built.

        :param y_delta: float: the y_delta tolerance to assess whether a span
            belongs to the same line as the current line.
        '''
        # Get access the parent function variables
        nonlocal _line_count

        # add a span_no_in_clip key to each span
        span['span_no_in_clip'] = idx

        # following spans on the same line
        # --------------------------------
        if _span_is_on_the_same_line(
            span_bbox=span["bbox"],
            line_bbox=line_rects[-1],
            y_delta=y_delta,
        ):
            # extend the lines' Rectangle
            line_rects[-1] |= span['bbox']
            # amend following span and extend line's rectangle
            span['raw_line_no'] = _line_count
            return span

        # else: first span on a new line
        # ------------------------------
        # make new line rect
        line_rects.append(span['bbox'])
        # increment the _line_count and the raw_line_no
        _line_count += 1
        # amend first span and make new line rect
        span['raw_line_no'] = _line_count
        return span

    # end of nested function
    # #######################################

    # Declare and initialize a list of lines' rectangles
    # with the first span's bbox rectangle
    _line_rects: list[Rect] = [spans[0]['bbox']]

    # Initialize the _amended_spans list
    _amended_spans: list[dict] = [_amend_first_span(spans[0])]

    # update or make new lines' Rectangle list by walking the
    # spans and add the "raw" line number to which they pertain
    # to the spans
    _amended_spans.extend(
        __make_line_rect_and_amend_span(idx, span, _line_rects, y_delta)
        for idx, span in enumerate(spans[1:], start=1)
    )

    return _amended_spans, _line_rects, _line_count


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
