# extract_pits.py
'''
Stores the high-level functions that write the markdown for a page.
'''

from functools import partial
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.line_img_tab import ParagImgTab
from pdf_structr.write.write_image import (
    any_image_processing_requested,
    output_images,
    process_image,
)
from pdf_structr.write.write_img_tab_lib import (
    get_relevant_img_or_tab_rects,
)
from pdf_structr.write.write_lib import (
    filter_rects_above_text_rect,
)
from pdf_structr.write.write_lines_in_img import (
    write_line_in_img,
)
from pdf_structr.write.write_lines_in_txt_rect import (
    write_text_line_and_above,
)
from pdf_structr.write.write_lines_lib import (
    process_lines_in_rect_decorator,
)
from pdf_structr.write.write_table import (
    output_tables,
)

#####################
# Subfunctions
#####################


def _write_bottom_of_page(
    parag_img_tabs: list[ParagImgTab],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    vg_clusters: dict,
    PARAM: dict[str, str | int | bool | None],
    process_image_partial: Callable,
) -> None:
    '''
    Write the tables and images that are below any text.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

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

    :param get_header_id: Callable: the headers identifier callable.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param process_image_partial: Callable: a preconfigured partial
        function derived from write_image.process_image to be called
        from within write_image.
    '''
    # ------------------------------
    # 1. Process remaining tables
    # ------------------------------

    # If there are any remaining tables
    if _relevant_table_rect_list := get_relevant_img_or_tab_rects(
        lambda *, rect_dict, **kwargs: list(rect_dict.items())
    )(
        rect_dict=tables_tuple[2],
    ):
        # output them and store them as new elements in parag_img_tabs
        output_tables(
            parag_img_tabs=parag_img_tabs,
            tables_tuple=tables_tuple,
            tab_list=_relevant_table_rect_list,
        )

    # ------------------------------
    # 1. Process remaining img/vg_clusters
    # ------------------------------

    # If any image processing has been requested
    if any_image_processing_requested(PARAM=PARAM):
        # and if there are any remaining images/vgs
        if _relevant_img_rect_list := get_relevant_img_or_tab_rects(
            lambda *, rect_dict, **kwargs: list(rect_dict.items())
        )(
            rect_dict=vg_clusters,
        ):
            # output them and store them as new elements in parag_img_tabs
            output_images(
                process_image_partial=process_image_partial,
                img_list=_relevant_img_rect_list,
            )


def _write_top_and_body_of_page(
    page: pymupdf.Page,
    parag_img_tabs: list[ParagImgTab],
    blocks: list[dict],
    text_rect: pymupdf.IRect,
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    vg_clusters: dict[int, pymupdf.Rect],
    links: list[dict[str, int | str | pymupdf.Rect]],
    get_header_id: Callable,
    process_image_partial: Callable,
    PARAM: dict[str, str | int | bool | None],
) -> None:
    '''
    Write the tables, images and text rectangles into a string from top
    to the last text rectangle.

    :param page: pymupdf.Page: the current page.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param blocks: list[dict]: the text blocks extracted via
        `textpage.extractDICT(sort=True)["blocks"]` in the
        `extract_rects` package.

    :param text_rect: pymupdf.IRect: the current text IRectangle.

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

    :param process_image_partial: Callable: a preconfigured partial
        function derived from write_image.process_image to be called
        from within write_image.
    '''
    # ------------------------------
    # 1. Process tables above this text rect
    # ------------------------------

    # If there are any tables above this text rect
    if _relevant_table_rect_list := get_relevant_img_or_tab_rects(
        filter_rects_above_text_rect
    )(
        rect_dict=tables_tuple[2],
        text_rect=text_rect,
    ):
        # output them and store them as new elements in parag_img_tabs
        output_tables(
            parag_img_tabs=parag_img_tabs,
            tables_tuple=tables_tuple,
            tab_list=_relevant_table_rect_list,
        )

    # ------------------------------
    # 2. Process img/vg_cluster above this text rect
    # ------------------------------

    # If any image processing has been requested
    if any_image_processing_requested(PARAM=PARAM):
        # and if there are any images/vgs above this text rect
        if _relevant_img_rect_list := get_relevant_img_or_tab_rects(
            filter_rects_above_text_rect
        )(
            rect_dict=vg_clusters,
            text_rect=text_rect,
        ):
            # output them and store them as new elements in parag_img_tabs
            output_images(
                process_image_partial=process_image_partial,
                img_list=_relevant_img_rect_list,
            )

    # ------------------------------
    # 3. Process the text (and eventually tables img/vg clusters)
    #    inside this text rect
    # ------------------------------

    # output text inside this text rectangle
    process_lines_in_rect_decorator(write_text_line_and_above)(
        page=page,
        parag_img_tabs=parag_img_tabs,
        get_header_id=get_header_id,
        clip=text_rect,  # text_rect=text_rect,
        img_rects=vg_clusters,  # vg_clusters=vg_clusters,
        tables_tuple=tables_tuple,
        tab_rects0=list(tables_tuple[2].values()),
        img_rects0=list(vg_clusters.values()),
        PARAM=PARAM,
        links=links,
        blocks=blocks,
        process_image_partial=process_image_partial,
        # nlines=_nlines,
        # idx: int,
        # context_dict=_context_dict,
    )


def _create_process_image_partial(
    parag_img_tabs: list[ParagImgTab],
    page: pymupdf.Page,
    blocks: list[dict],
    vg_clusters: dict[int, pymupdf.Rect],
    links: list[dict[str, int | str | pymupdf.Rect]],
    get_header_id: Callable,
    PARAM: dict[str, str | int | bool | None],
) -> Callable:
    '''
    Creates a first partial to wrap `write_line_in_img` decorated
    by `process_lines_in_rect_decorator` and passes it as argument
    to a second partial wrapping `process_image`.

    Both `write_line_in_img` and `process_image` are functions that
    live in module `write_image`.

    `process_image` processes the images, by saving them on the disk,
    converting them to a base64 representation and extracting text
    that may live inside the images and saving them to the returning
    list of ParagImgTabs.

    `write_line_in_img` extracts the text that may live inside an image
    and saves it to the Lines of a ParagImgTabs.

    :param parag_img_tabs: list[ParagImgTab]: the list of ParagImgTab
        instances to be populated by the submodules in this package, by
        iterables of strings corresponding to a line or an md-string
        formatted elements such as a table or the string associated
        with an image or vector graphic.

    :param page: pymupdf.Page: the current page

    :param blocks: list[dict]: the text blocks extracted via
        `textpage.extractDICT(sort=True)["blocks"]` in the
        `extract_rects` package.

    :param vg_clusters: dict[int, pymupdf.Rect]: a numbered dict of vector
        graphics clusters in the current page.

    :param links: list[dict[str, int | str | pymupdf.Rect]]: a list of
        the outer links in the current page.

    :param get_header_id: Callable: the headers identifier callable.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    '''
    # Create a partial function with write_lines_in_img that will
    # be called from within write_image
    _write_text_for_write_image: Callable = partial(
        process_lines_in_rect_decorator(
            process_line_func=write_line_in_img,
        ),
        page=page,
        parag_img_tabs=parag_img_tabs,
        blocks=blocks,
        links=links,
        get_header_id=get_header_id,
        PARAM=PARAM,
    )

    # Create a partial function with process_image that will
    # be called from within write_image
    return partial(
        process_image,
        parag_img_tabs=parag_img_tabs,
        page=page,
        write_lines_for_write_image=_write_text_for_write_image,
        img_rects=vg_clusters,
        PARAM=PARAM,
    )


#####################
# Main
#####################


def extract_paragimgtabs_for_page(
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
) -> list[ParagImgTab]:
    '''
    Extract a list of ParagImgTabs for the passed-in page by iterating
    over text rectangles. While doing so, it also output any table
    or vg graphics, as the case may be. They may live above, below
    or inside the text rectangles.

    :returns: a list[ParagImgTab] of all the ParagImgTab objects in
        the current page.

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
    # Declare the list of dicts that will store the returning lines and other
    # md-string elements (images and tables)
    parag_img_tabs: list[ParagImgTab] = []

    # Create a partial function with write_lines_in_img that will
    # be called from within write_image
    # Create a partial function with process_image that will
    # be called from within write_image
    _process_image_partial: Callable = _create_process_image_partial(
        parag_img_tabs=parag_img_tabs,
        page=page,
        blocks=blocks,
        vg_clusters=vg_clusters,
        links=links,
        get_header_id=get_header_id,
        PARAM=PARAM,
    )

    # Create a partial function with _write_top_and_body_of_page()
    # that will be called from within the list comprehension below
    _write_top_and_body_of_page_partial: Callable = partial(
        _write_top_and_body_of_page,
        page=page,
        parag_img_tabs=parag_img_tabs,
        blocks=blocks,
        tables_tuple=tables_tuple,
        vg_clusters=vg_clusters,
        links=links,
        get_header_id=get_header_id,
        PARAM=PARAM,
        process_image_partial=_process_image_partial,
    )

    # Iterate on the text rectangles and write the tables, images and texts
    # above and inside them
    for text_rect in text_rects:
        _write_top_and_body_of_page_partial(text_rect=text_rect)

    # Write the last tables and images
    _write_bottom_of_page(
        parag_img_tabs=parag_img_tabs,
        tables_tuple=tables_tuple,
        vg_clusters=vg_clusters,
        PARAM=PARAM,
        process_image_partial=_process_image_partial,
    )

    return parag_img_tabs
