# write_lib.py
'''
Library of utility functions for the write modules (and beyond).
'''

import pymupdf  # type: ignore  # noqa: I001
import logging
from typing import Callable

from pdf_structr.write.write_image import (
    any_image_processing_requested,
    output_images,
)
from pdf_structr.write.write_img_tab_lib import (
    get_relevant_img_or_tab_rects,
)
from pdf_structr.write.write_table import (
    output_tables,
)
from pdf_structr.write.line_img_tab import ParagImgTab

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
# Filtering functions
#####################


def _filter_rects_above_line_rect_within_clip(
    rect_dict: dict[int, pymupdf.Rect],
    lrect: pymupdf.Rect,
    clip: pymupdf.Rect,
    *args,
    **kwargs,
) -> list[tuple[int, pymupdf.Rect]]:
    '''
    This function selects the image or table rectangles that are above
    the current line rectangle and within a text column rectangle (the clip).

    Takes in a dict of numbered rectangles, filters it to select only the
    rectangles:
    - that are above the passed-in text rectangle and
    - which intersection with the clip form a valid rectangle (i.e. x0 < x1
    and y0 < y1).

    :returns a list of 2-tuples, where:
    - the first item of the tuple is the dict key (i.e. the index number
      of the table rectangle when first returned by the tablefinder)
    - the second item is the corresponding Rectangle.

    Function to be decorated by
    `write_img_tab_lib.get_relevant_img_or_tab_rects` to provide the
    decorator with a filtering of the images or the tables located
    within the `clip` and above the `lrect`.

    :param rect_dict: dict[int, pymupdf.Rect]: a dict of rectangles
        (in practice, image or table rects) where the keys are the
        index numbers of the rectangles at extraction time.

    :param lrect: pymupdf.Rect: the current text line rectangle in the
        iteration over the line text rectangles.

    :param clip: pymupdf.Rect: the zone to parse. May be the page clipped off
        the margins or a text rectangle.
    '''
    return [
        _rect_in_list
        for _rect_in_list in rect_dict.items()
        # Only the table or image rectangle above the current line rectangle
        if _rect_in_list[1].y1 <= lrect.y0
        # and only if the intersection of current table or image rectangle
        # and the clip (i.e. the text column rectangle) form a valid rectangle
        # (i.e. x0 < x1 and y0 < y1)
        and not (_rect_in_list[1] & clip).is_empty
    ]


def filter_rects_above_text_rect(
    *,
    rect_dict: dict[int, pymupdf.Rect],
    text_rect: pymupdf.Rect,
    **kwargs,
) -> list[tuple[int, pymupdf.Rect]]:
    '''
    Takes in a dict of numbered table or image rectangles, filters it
    to select only the rectangles that are above the passed-in text
    rectangle and returns a list of 2-tuples, where:
    - the first item of the tuple is the dict key (i.e. the index number
      of the table rectangle when first returned by the tablefinder)
    - the second item is the corresponding Rectangle.

    Function to be decorated by
    `write_img_tab_lib.get_relevant_img_or_tab_rects` to provide the
    decorator with a filtering of the images or the tables located
    with a filtering of the images or the tables located above the
    `text_rect`.

    :param rect_dict: dict[int, pymupdf.Rect]: a dict of rectangles
        (in practice, image or table rects) where the keys are the
        index numbers of the rectangles at extraction time.
    :param text_rect: pymupdf.Rect: the current text line rectangle in the
        iteration over the line text rectangles.
    :param clip: pymupdf.Rect: the zone to parse. May be the page clipped off
        the margins or a text rectangle.
    '''
    return [
        _rect_in_list
        for _rect_in_list in rect_dict.items()
        # Only the tables or images above the current line rectangle
        if _rect_in_list[1].y1 <= text_rect.y0
    ]


###################################
# Tables and images inside text (column) rectangles
###################################


def add_tabs_and_imgs_living_inside_text_rect(
    parag_img_tabs: list[ParagImgTab],
    clip: pymupdf.Rect,
    img_rects: dict[int, pymupdf.Rect],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    lrect: pymupdf.Rect,
    PARAM: dict[str, str | int | bool | None],
    process_image_partial: Callable,
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> None:
    '''
    Adds the tables and the images that live inside the text rectangle
    and above the current line into the return string.

    :returns: None, because it is extending the return_string_list

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param clip: pymupdf.Rect: the text rectangle that we are currently
        parsing.

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

    :param lrect: pymupdf.Rect: the current line's rectangle.

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
    # ------------------------------------------------------------
    # Pick up tables ABOVE this line lrect
    # ------------------------------------------------------------

    # If there are any tables above this line lrect
    if _relevant_table_rect_list := get_relevant_img_or_tab_rects(
        filtering_func=_filter_rects_above_line_rect_within_clip
    )(
        rect_dict=tables_tuple[2],
        lrect=lrect,
        clip=clip,
    ):

        # output them and store them as new elements in parag_img_tabs
        output_tables(
            parag_img_tabs=parag_img_tabs,
            tables_tuple=tables_tuple,
            tab_list=_relevant_table_rect_list,
        )

    # ------------------------------------------------------------
    # Pick up images / graphics ABOVE this line lrect
    # ------------------------------------------------------------

    # If any image processing has been requested
    if any_image_processing_requested(PARAM=PARAM):
        # and if there are any images/vgs above this text rect
        if _relevant_img_rect_list := get_relevant_img_or_tab_rects(
            filtering_func=_filter_rects_above_line_rect_within_clip,
        )(
            rect_dict=img_rects,
            lrect=lrect,
            clip=clip,
        ):

            # output them and store them as new elements in parag_img_tabs
            output_images(
                process_image_partial=process_image_partial,
                img_list=_relevant_img_rect_list,
            )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
