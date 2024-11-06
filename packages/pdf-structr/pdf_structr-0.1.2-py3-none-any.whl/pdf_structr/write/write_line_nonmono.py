# write_line_nonmono.py
'''
Encapsulating the non all-monosized font lines printing.
'''

import logging
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

# from pdf_struct.custrag_write.join_lines import (
#     add_lrs_if_needed,
# )
from pdf_structr.write.classes import Line
from pdf_structr.write.flatten_spans_list import (
    flatten_and_clean_str_itr,
)

# from pdf_struct.custrag_write.write_headers import (
#     handle_header,
# )
from pdf_structr.write.write_spans import (
    build_iter_spans_non_mono_line,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


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


# @count_and_avg_timer(name='output - write_non_monosized_line', prnt_freq=100)
def write_non_monosized_line(
    line_o: Line,
    nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str, float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    get_header_id: Callable,
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> str:
    '''
    Handling of all text lines which are not all-monosized font.

    :return: the hdr_string.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param nlines: list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ]: the list of lines as 2-tuples, line Rectangle - corresponding spans'
        list sorted by x0, as extracted by get_raw_lines() for
        the current text or image Rect.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous line.
          Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all monospaced
          font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param get_header_id: Callable: a callable that permits identifying
        header and returns a string to format the md headers.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.
    '''

    # ------------------------------------------------
    # Write the line
    # ------------------------------------------------

    _formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ] = build_iter_spans_non_mono_line(
        line_o=line_o,
        IGNORE_CODE=PARAM['IGNORE_CODE'],  # type: ignore
        context_dict=context_dict,
        links=links,
    )

    line_o.str_itr = flatten_and_clean_str_itr(
        formatted_spans_tuples_list=_formatted_spans_tuples_list,
        span_count=line_o.spans_count,  # type: ignore
        bold_span_count=line_o.bold_span_count,
        italics_span_count=line_o.italic_span_count,
    )

    # ------------------------------------------------
    # Update the context dict
    # ------------------------------------------------

    # Update the context dict
    context_dict['prev_bno'] = line_o.block
    context_dict['prev_lrect'] = line_o.bbox

    # ------------------------------------------------
    # Identify headers
    # ------------------------------------------------

    # Check if this line is a header
    _hdr_string: str = get_header_id(line_o.spans[0])  # type: ignore

    # Start handling header building
    if _hdr_string:
        line_o.line_type = 'header'
        line_o.prefix = _hdr_string

    return _hdr_string


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
