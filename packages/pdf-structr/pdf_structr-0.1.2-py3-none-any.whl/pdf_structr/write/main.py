# write_page.py
'''
Stores the high-level functions that write the markdown for a page.
'''

from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.extract.extract import process_page_decorator
from pdf_structr.write.extract_pits import (
    extract_paragimgtabs_for_page,
)
from pdf_structr.write.write_page_md import make_md_string

# from pdf_struct.mo_utils.timer import count_and_avg_timer

#####################
# Main
#####################


# @count_and_avg_timer(name='output - get_md_string_for_page')
@process_page_decorator
def get_md_string_for_page(
    page: pymupdf.Page,
    # we do not need the textpage but we'll keep it for future
    # development
    textpage: pymupdf.TextPage,
    blocks: list[dict],
    text_rects: list[pymupdf.IRect],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    vg_clusters: dict[int, pymupdf.Rect],
    links: list[dict[str, int | str | pymupdf.Rect]],
    get_header_id: Callable,
    PARAM: dict[str, str | int | bool | None],
    *args,
    **kwargs,
) -> str:
    '''
    Extract markdown text iterating over text rectangles.
    We also output any tables and vg cluster. They may live above,
    below or inside the text rectangles.

    :param page: pymupdf.Page: the current page

    :param textpage: pymupdf.TextPage: the current TextPage

    :param blocks: list[dict]: the text blocks extracted via
        `textpage.extractDICT(sort=True)["blocks"]` in the
        `extract_rects` package.

    :param text_rects: list[pymupdf.IRect]: a list of text rectangles
        in the current page.

    :param tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ]: a tuple containing the various table elements extracted from
        the page by extract_tables:
        - a list of tables bboxes, cols and rows
        - a numbered dict of tables md strings, ordered by y1 and x0
        - a numbered dict of tables rectangles, ordered by y1 and x0

    :param vg_clusters: dict[int, pymupdf.Rect]: a numbered dict of vector
        graphics clusters in the current page.

    :param links: list[dict[str, int | str | pymupdf.Rect]]: a list of
        the outer links in the current page.

    :param get_header_id: Callable: the headers identifier callable.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :returns: the page's md_string.
    '''
    return make_md_string(
        extract_paragimgtabs_for_page(
            page=page,
            textpage=textpage,
            blocks=blocks,
            text_rects=text_rects,
            tables_tuple=tables_tuple,
            vg_clusters=vg_clusters,
            links=links,
            get_header_id=get_header_id,
            PARAM=PARAM,
        )
    )
