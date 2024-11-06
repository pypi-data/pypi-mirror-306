# make_spans_list.py

'''
Module to store the spans' list extraction of package get_text_lines.

'''


import logging
import string
from typing import Any, Generator

from pymupdf import IRect, Rect  # type: ignore

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
# Playground
#####################


def is_white(text: str):
    WHITE = set(string.whitespace)
    return WHITE.issuperset(text)


def _adapt_superscript_span(
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
    line: dict[
        str,
        # wmode
        int
        # dir
        | tuple[float, float]
        # bbox
        | tuple[float, float, float, float]
        # list of spans
        | list[
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
                # bbox (will be converted from a
                # tuple into a Rect in the loop below)
                | tuple[float, float, float, float],
            ]
        ],
    ],
    span_no: int,
) -> None:
    '''
    If a span is superscript, modify the bbox of this span so that it matches
    that of the preceding or the following one.

    In the original pymupdf version, this function was also re-writing the
    text content between square brackets. This part (putting the text content
    between square brackets) is now handled in the `write` modules.

    :param span: dict[
        str,
        int
        | float
        | str
        | tuple[float, float]
        | Rect,
    ]: a span dictionary, as rewriten in _make_augmented_span().

    :param span_bbox_rect: Rect: a Rectangle.

    :param line: dict[
        str,
        int
        | tuple[float, float]
        | tuple[float, float, float, float]
        | list[
            dict[
                str,
                int
                | float
                | str
                | tuple[float, float]
                | tuple[float, float, float, float],
            ]
        ],
    ]: a line extracted from a textblock.

    :param span_no: int: the current span index number in the current line.
    '''
    # Determine whether to use the preceeding or the following span to adapt
    # the current spans' rectangle
    # Following span if first span in line, else preceeding one
    idx: int = 1 if span_no == 0 else span_no - 1

    # Get the neighboring span (preceeding or following one)
    _neighbor_span: dict[
        str,
        # flags and color
        int
        # size (fontsize), ascender and descender
        | float
        # font (fontname) and text
        | str
        # origin
        | tuple[float, float]
        # bbox (will be converted from a
        # tuple into a Rect in the loop below)
        | tuple[float, float, float, float],
    ] = line["spans"][
        idx
    ]  # type: ignore

    # Update the y1 of the current span's bbox Rect with the y1
    # of the neighbor span
    span["bbox"].y1 = _neighbor_span["bbox"][3]  # type: ignore


def _make_augmented_span(
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
    line: dict[
        str,
        # wmode
        int
        # dir
        | tuple[float, float]
        # bbox
        | tuple[float, float, float, float]
        # list of spans
        | list[
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
                # bbox (will be converted from a tuple into a Rect here)
                | tuple[float, float, float, float],
            ]
        ],
    ],
    span_bbox_rect: Rect,
    block_no: int,
    line_no: int,
    span_no: int,
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
    # bbox (converted from a tuple into a Rect)
    | Rect,
]:
    '''
    Modify the structure of the span to incorporate line and block information,
    convert its bbox tuple into a Rect and eventually rewrite its text content
    and amend the bbox if the text is superscript.

    Outgoing spans have the following structure:

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

    :param span: dict[
        str,
        int
        | float
        | str
        | tuple[float, float]
        | Rect,
    ]: a span dictionary, as rewriten in the loop [___].

    :param span_bbox_rect: Rect: a Rectangle.

    :param line: dict[
        str,
        int
        | tuple[float, float]
        | tuple[float, float, float, float]
        | list[
            dict[
                str,
                int
                | float
                | str
                | tuple[float, float]
                | tuple[float, float, float, float],
            ]
        ],
    ]: a line extracted from a textblock.

    :param span_bbox_rect: Rect: a pymupdf Rectangle from the span's bbox
        tuple.

    :param block_no: int: the number of the block among the blocks pertaining
        to this page.

    :param line_no: int: the number of the line to which this span belongs.
        This line number is the number of the line among all the lines of
        the page, not among the lines pertaining to the block.

    :param span_no: int: the number of the span among all the spans
        of the current page.
    '''
    # replace the span's tuple version bbox
    # with the Rect version bbox
    span["bbox"] = span_bbox_rect

    # include line/block numbers in the span to facilitate
    # separator insertion
    span["line"] = line_no
    span["block"] = block_no

    # if a superscript, modify bbox of this span with that of the
    # preceding or following span and re-write the text content
    # between square brackets
    if span["flags"] & 1 == 1:  # type: ignore
        _adapt_superscript_span(
            span=span,
            line=line,  # type: ignore
            span_no=span_no,
        )

    return span


def make_spans_list(
    blocks: list[dict],
    clip: Rect | IRect,
) -> list[
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
]:
    '''
    Make a list of the (almost) horizontal text spans that are within
    the clip (usually, a text column Rect).

    The returned spans are augmented in the sense that each returned
    span is a dict where:
    1. the bbox has been transformed into a Rect;
    2. it has two additional keys, `line` and `block` that refers to the
    line and block to which they originally pertain.

    Before turning the bbox into a Rect, superscript spans y1 is adjusted
    to match the neighboring spans y1s.

    It has to be taken into account that the spans have already been
    augmented in the stats_modules with the following keys:
    - `txt_len`
    - `digit_count`

    Accordingly, outgoing spans have the following structure:

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

    :returns: a list of "augmented" spans.

    :param blocks: list[dict]: the blocks extracted from the textpage via
        textpage.extractDICT.

    :param clip: Rect | IRect: a clip inside the page within which the parsing
        shall be made.
    '''
    horizontal_spans_generator: Generator[
        tuple,
        Any,
        Any,
    ] = (
        (
            _span,
            _line,
            Rect(_span["bbox"]),
            _block_no,
            _line_no,
            _span_no,
        )
        for _block_no, _block in enumerate(blocks)
        # keep only textblocks and non empty blocks
        # # NOTE: Redundant; this filtering has already been made in
        # # the stats or layout modules
        # if _block["type"] == 0 and not Rect(_block["bbox"]).is_empty
        # iterate on the lines
        for _line_no, _line in enumerate(_block["lines"])  # type: ignore
        # only accept horizontal lines
        # NOTE: Redundant; this filtering has already been made in
        # the stats or layout modules
        if abs(1 - _line["dir"][0]) <= 1e-3
        # iterate on the spans
        for _span_no, _span in enumerate(_line["spans"])  # type: ignore
        # exclude 'white' spans
        if not is_white(_span["text"])
    )

    return [
        _make_augmented_span(
            span=span_tup[0],
            line=span_tup[1],  # type: ignore
            span_bbox_rect=span_tup[2],
            block_no=span_tup[3],
            line_no=span_tup[4],
            span_no=span_tup[5],
        )
        for span_tup in horizontal_spans_generator
        # make augmented spans only if the spans are inside
        # the clip.
        # (span_tup[2].tl + span_tup[2].br) / 2 computes the
        # middle point of the span's bbox.
        # this middle point is then used to check if the span
        # is in the clip.
        if (((span_tup[2].tl + span_tup[2].br) / 2) in clip)
    ]


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
