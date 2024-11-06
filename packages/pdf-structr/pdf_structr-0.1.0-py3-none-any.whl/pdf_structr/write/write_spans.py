# write_spans.py
'''
Module to store all the spans related formating and writing
functions.
'''
import functools
import logging
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.handle_bullets import (
    handle_starting_bullet,
)
from pdf_structr.write.line_img_tab import Line
from pdf_structr.write.write_span import (
    format_span_in_non_all_mono_line_wrapper,
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


###################################
# Main spans processor
###################################


def build_iter_spans_non_mono_line(
    line_o: Line,
    IGNORE_CODE: bool,
    context_dict: dict,
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> list[tuple[tuple[str, str, str, str, str, str, str], int]]:
    '''
    Make a list of the text of non-monotonic successive spans pertaining to the
    same line.

    Handles the case where the line starts with a bullet.

    Updates the spans count in italics, bold, superscript and mono about
    the current line.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param IGNORE_CODE: bool: the user wants monosized fonts to be treated
        as regular text.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous line.
          Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all monospaced
          font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'idx': int: the index number of the current line.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.

    Returns: the concatenated line as a string.
    '''
    # Get the current line's spans
    _spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ] = line_o.spans  # type: ignore

    # Add a dash to the first span if the line startswith a bullet
    handle_starting_bullet(
        line_o=line_o,
        context_dict=context_dict,
    )

    # Make a partial for easier access
    _format_span_in_non_monot_line_partial: Callable = functools.partial(
        format_span_in_non_all_mono_line_wrapper,
        line_o=line_o,
        spans=_spans,
        IGNORE_CODE=IGNORE_CODE,
        context_dict=context_dict,
        links=links,
    )

    # Walk the spans then extract and format the spans' text strings
    # Return an iterable with md formating elts embedded between the
    # spans' text corresponding to the formatted line
    _formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ] = [
        _format_span_in_non_monot_line_partial(
            current_span=_span,
            current_idx=_idx,
        )
        for _idx, _span in enumerate(_spans)
    ]

    return _formatted_spans_tuples_list


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
