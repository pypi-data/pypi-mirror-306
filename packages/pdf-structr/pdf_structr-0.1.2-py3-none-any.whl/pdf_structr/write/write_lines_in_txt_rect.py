# write_lines_in_txt_rect.py
'''
Encapsulates functions that extract the text from text rectangles and converts
them to an md string.
'''

import logging
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.utils.utils import (
    intersects_rects,
)
from pdf_structr.write.classes import ParagImgTab
from pdf_structr.write.write_lib import (
    add_tabs_and_imgs_living_inside_text_rect,
)
from pdf_structr.write.write_line import write_text_line_core

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
# Intersection functions
#####################


def _intersect_img_or_tbl_rect(
    lrect: pymupdf.Rect,
    tab_rects0: list[pymupdf.Rect],
    img_rects0: list[pymupdf.Rect],
) -> bool:
    '''
    Test whether the current line rectangle intersects with any of
    the passed-in table or image rectangle.

    :param lrect: pymupdf.Rect: the current line rectangle in the
        line iteration.
    :param tab_rects0: list[pymupdf.Rect]: the list of table
        rectangles identified for the current page.
    :param img_rects0: list[pymupdf.Rect]: the list of images
        rectangles identified for the current page.

    Returns: True or False
    '''
    return intersects_rects(lrect, tab_rects0) or intersects_rects(
        lrect, img_rects0
    )


#####################
# Playground
#####################


def write_text_line_and_above(
    *,
    page: pymupdf.Page,
    parag_img_tabs: list[ParagImgTab],
    get_header_id: Callable,
    img_rects: dict[int, pymupdf.Rect],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    tab_rects0: list[pymupdf.Rect],
    img_rects0: list[pymupdf.Rect],
    nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect,
                ]
            ],
        ],
    ],
    idx: int,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    process_image_partial: Callable,
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
    **kwargs,
) -> None:
    '''
    Main function to process each single line living within a text (column)
    rectangle.

    Analyse the spans of the line in their context, then extract, concat
    and format the spans' text as the case may be. It also updates the
    context dict for the next iteration.

    Note that this function is NOT called for lines contained within image
    rectangles; for such lines, `write_text_line_core` is called via
    `_write_line_in_img`.

    Decorated by `process_lines_decorator()` which:
    - calls `get_raw_lines_wrapper` to:
      - extract the lines contained within the `clip`
      - initialize the context dict
    - and passes them to this function.

    Returns: an iterable of strings, being either a single concatenated
    string inside a generator or chunks of prefixes, span text and suffixes.

    :param page: pymupdf.Page: the current page.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param get_header_id: Callable: a callable that permits identifying
        header and returns a string to format the md headers.

    :param img_rects: dict[int, pymupdf.Rect]: an ordered dict of image and vg
        rectangles in the current page, sorted by by y1 and x0 and where
        the keys are the index numbers at extraction time.

    :param tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ]: a tuple containing the various table elements extracted from
        the page by extract_tables:
        - a list of tables bboxes, cols and rows
        - a numbered dict of tables md strings, ordered by y1 and x0
        - a numbered dict of tables rectangles, ordered by y1 and x0

    :param tab_rects0: list[pymupdf.Rect]: the list of table
        rectangles identified for the current page.

    :param img_rects0: list[pymupdf.Rect]: the list of images
        rectangles identified for the current page.

    :param nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect,
                ],
            ],
        ],
    ]: the list of lines in the current column text rect.

    :param idx: int: the index number of the current line.

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

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param process_image_partial: Callable: a preconfigured partial
        function derived from write_image.process_image to be called
        from within write_image.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.
    '''
    # Immediately update the idx number of the current line in the context dict
    context_dict['idx'] = idx

    # Get the current line
    _nline: tuple[
        pymupdf.Rect,
        list[
            dict[str, float | int | str | tuple[float, float] | pymupdf.Rect],
        ],
    ] = nlines[idx]
    # Get the current line's rectangle
    _lrect: pymupdf.Rect = _nline[0]

    # ------------------------------------------------
    # Skip any line intersecting with a table or image rectangle
    # ------------------------------------------------

    if _intersect_img_or_tbl_rect(_lrect, tab_rects0, img_rects0):

        return None

    # ------------------------------------------------
    # Process any table and image Rect above the current line within
    # the clip and add their text or text refs to the parag_img_tabs
    # ------------------------------------------------

    add_tabs_and_imgs_living_inside_text_rect(
        parag_img_tabs=parag_img_tabs,
        clip=context_dict['CLIP'],  # the current column text Rect
        img_rects=img_rects,
        tables_tuple=tables_tuple,
        lrect=_lrect,  # the current line rectangle
        PARAM=PARAM,
        process_image_partial=process_image_partial,
        links=links,
    )

    # ------------------------------------------------
    # Now process the line itself
    # ------------------------------------------------

    write_text_line_core(
        page=page,
        parag_img_tabs=parag_img_tabs,
        elt_type='text',
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
