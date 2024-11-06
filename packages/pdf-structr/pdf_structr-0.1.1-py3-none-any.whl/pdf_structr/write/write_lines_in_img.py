# write_lines_in_img.py
'''
Stores functions that extract the text from images and converts
them to an md string.
'''
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.line_img_tab import ParagImgTab
from pdf_structr.write.write_line import (
    write_text_line_core,
)

###################################
# Undecorated write_lines_in_img stack (encapsulated in a partial in
# the write_page module)
###################################


def write_line_in_img(
    *,
    page: pymupdf.Page,
    parag_img_tabs: list[ParagImgTab],
    get_header_id: Callable,
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
    idx: int,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
    **kwargs,
) -> None:
    '''
    Calls write_text_line_core to convert a line extracted from an image
    rectangle into an md line.

    :param page: pymupdf.Page: the current page.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param get_header_id: Callable: a callable that permits identifying
        header and returns a string to format the md headers.

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
        the current image Rect.

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
        - 'CLIP': Rect: the rectangle of the current clip (the current image
          Rect).
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).

    :param idx: int: the line index in the iteration on the text lines embeddd
        in the image rectangle.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.

    '''
    # Immediately update the idx number
    context_dict['idx'] = idx

    write_text_line_core(
        page=page,
        parag_img_tabs=parag_img_tabs,
        elt_type='embd-text',
        get_header_id=get_header_id,
        nlines=nlines,
        context_dict=context_dict,
        PARAM=PARAM,
        links=links,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
