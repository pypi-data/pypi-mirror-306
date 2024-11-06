# make_raw_lines.py

'''
Module to store the spans' list conversion to text lines of
package get_text_lines.

'''


import logging

from pymupdf import Rect  # type: ignore

from pdf_structr.get_text_lines.make_lines_rect import (
    make_lines_rect_and_amended_spans,
)
from pdf_structr.get_text_lines.sanitize_spans import sanitize_spans

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
# Subfunctions
###############################


def _make_raw_lines(
    amended_spans: list[dict],
    line_rects: list[Rect],
    line_count: int,
) -> list[tuple[Rect, list[dict]]]:
    '''
    Converts the list of amended spans and the list of lines' rectangles
    for the page into a list of "raw lines".

    The list of "raw lines" is a list of tuple[Rect, list[dict]],
    where each Rectangle is a line's rectangle and
    the list[dict] the list of the spans in the line.

    :param amended_spans: list[dict]: the list of spans as processed by
        `make_lines_rect_and_amended_spans()`.

    :param line_rects: list[Rect]: the list of `raw lines`' Rectangles a
        returned by `make_lines_rect_and_amended_spans()`.

    :param line_count: int: the line count for the page.
    '''

    _first_span_for_line: int = 0

    def __make_new_raw_line(
        current_line_idx: int,
        spans: list[dict],
    ) -> list[dict]:
        '''
        Make a new raw_line out of the spans (as augmented in the first list
        comprehension in the body of the main function) by iterating on the
        spans list and selecting those that have the same line number.

        nonlocal variable _first_span_for_line (int) is used so that at each
        call of the function, the spans that have already been parsed at the
        previous call and appended to a line be excluded from the current
        iteration.

        :param current_line_idx: int: the current line index number.

        :param spans: list[dict]: the spans with a 'raw_line_no' key as
            marked by nested function __mark_line_no_to_span.

        :returns: list[dict]: a spans' list corresponding to the current line.
        '''
        nonlocal _first_span_for_line

        # make the list of spans for the line by iterating on the spans
        # and selecting those that are on the current line by raw_line_no
        _line_spans_list: list[dict] = [
            _span
            # we do not iterate the full list of spans, but
            # we start where we stopped at the previous call
            # to the function
            for _span in spans[_first_span_for_line:]
            # for _span in spans
            if _span['raw_line_no'] == current_line_idx
        ]

        # Sanitize the spans in the line
        _line_spans_list = sanitize_spans(line_spans=_line_spans_list)

        # update the _first_span_for_line sentinel (nonlocal variable)
        _first_span_for_line = _line_spans_list[-1]['span_no_in_clip'] + 1

        return _line_spans_list

    ##########################################

    # make the list of raw_lines by iterating the lines' Rectangles list
    # and calling the __make_new_raw_line at each iteration, which
    # builds a list of spans for the given line.
    return [
        (
            _line_rect,
            __make_new_raw_line(
                current_line_idx=_idx,
                spans=amended_spans,
            ),
        )
        for _line_rect, _idx in zip(line_rects, range(line_count + 1))
    ]


###############################
# Main
###############################


def make_raw_lines(
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
) -> list[
    # one tuple per line
    tuple[
        # the line's rectangle
        Rect,
        # the line's spans
        list[
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
    ]
]:
    '''
    Receives a list of "augmented" spans for a given clip (a page or
    a Rectangle) sorted by bottom coord, further augment the spans
    and converts the list of augmented spans into a list of "raw"
    lines, pushing each span into a list corresponding to one of
    the "raw" line.

    The augmented spans coming in have the following structure:

    ```python
    {
        'size': 9.960000038146973,
        'flags': 16,
        'font': 'Arial-BoldMT',
        'color': 0,
        'ascender': 0.9052734375,
        'descender': -0.2119140625,
        'text': 'STIF ',
        'origin': (276.2900085449219, 187.3399658203125),
        'bbox': Rect(
            276.2900085449219,
            176.68276977539062,
            300.7789001464844,
            190.39768981933594
        ),
        'txt_len': 5,
        'digit_count': 0,
        'line': 0,
        'block': 0,
    }
    ```

    The outgoing spans have the following new keys:
    - `raw_line_no`: the number of the raw line to which the span
        pertains.
    - `span_no_in_clip`: the number of the span in the clip, when sorted
        by y1 only.
    - `span_no_in_line_x0`: the span index number when sorted by x0 after
       sanitizing.

    ```python
    {
        'size': 9.960000038146973,
        'flags': 16,
        'font': 'Arial-BoldMT',
        'color': 0,
        'ascender': 0.9052734375,
        'descender': -0.2119140625,
        'text': 'STIF ',
        'origin': (276.2900085449219, 187.3399658203125),
        'bbox': Rect(
            276.2900085449219,
            176.68276977539062,
            300.7789001464844,
            190.39768981933594
        ),
        'txt_len': 5,
        'digit_count': 0,
        'line': 0,
        'block': 0,
        'raw_line_no': 0,
        'span_no_in_clip': 0,
        'span_no_in_line_x0': 0,
    }
    ```
    :returns: a list of lines, where each line is a 2-tuple with
        a Rectangle and a list of "augmented" spans pertaining
        to this line.

    :param spans: list[
        dict[
            str,
            int
            | float
            | str
            | tuple[float, float]
            | Rect,
        ]
    ]: the textpage list of augmented spans.

    :param y_delta: float: put spans on the same line if their top or bottom
        coordinate differ by no more than this value.
    '''
    # 1. add index numbers to spans and make lines' rectangles
    _amended_spans, _line_rects, _line_count = (
        make_lines_rect_and_amended_spans(spans=spans, y_delta=y_delta)
    )

    # 2. make the raw_lines
    _raw_lines = _make_raw_lines(
        amended_spans=_amended_spans,
        line_rects=_line_rects,
        line_count=_line_count,
    )

    return _raw_lines


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
