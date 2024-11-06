# write_image.py
'''
Module to store the images related functions.
'''
import os
from binascii import b2a_base64
from typing import Callable

import pymupdf  # type: ignore

from pdf_structr.write.classes import ParagImgTab

#####################
# Global variables
#####################


GRAPHICS_TEXT = "\n![](%s)\n"


#####################
# Core write and embed image functions
#####################


def _write_image(
    page: pymupdf.Page,
    i: int,
    pix: pymupdf.Pixmap,
    PARAM: dict[str, str | int | bool | None],
) -> str:
    '''
    Save the image on the drive and returns the path to the image.
    '''
    # Build the path
    # ----------------

    # Get the filename of the PDF
    _filename: str = os.path.basename(page.parent.name).replace(" ", "-")
    # Use the filename of the PDF to create the filename of the file
    _image_filename: str = os.path.join(
        PARAM['IMG_PATH'],  # type: ignore
        (f"{_filename}-{page.number}-{i}.{PARAM['IMG_EXTENSION']}"),
    )
    # Save the file
    pix.save(_image_filename)

    # return the filename to insert it into the markdown
    # ----------------

    return _image_filename.replace("\\", "/")


def _embed_image(
    pix: pymupdf.Pixmap,
    PARAM: dict[str, str | int | bool | None],
) -> str:
    '''
    Makes a base64 encoded string of the image and returns it.
    '''
    # make a base64 encoded string of the image
    # ----------------

    _data: str = b2a_base64(pix.tobytes(PARAM['IMG_EXTENSION'])).decode()
    return f"data:image/{PARAM['IMG_EXTENSION']};base64," + _data


def _small_image(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    PARAM: dict[str, str | int | bool | None],
) -> bool:
    '''
    Identifies small images. Small images are identified as a proportion
    of the page's dimension weighted by the passed-in image size limit
    parameter living in the high level PARAM dict.
    '''
    return (
        rect.width < page.rect.width * PARAM['image_size_limit']
        or rect.height < page.rect.height * PARAM['image_size_limit']
    )


def _save_or_embed_image(
    parag_img_tabs: list[ParagImgTab],
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    i: int,
    PARAM: dict[str, str | int | bool | None],
) -> None:
    '''
    Save the image to the image directory or makes a base64 representation
    of the image.

    We will ignore images that are empty or that have an edge smaller
    than x% of the corresponding page edge.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param page: pymupdf.Page: the current Page.

    :param rect: pymupdf.Rect: the image Rectangle.

    :param i: the index number of the Rect in the dict of rect.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.
    '''
    # Ignore small images
    # ----------------

    if _small_image(
        page=page,
        rect=rect,
        PARAM=PARAM,
    ):
        return

    # Get the pixmap for the image rectangle
    # ----------------

    pix: pymupdf.Pixmap = page.get_pixmap(clip=rect, dpi=PARAM['DPI'])

    # Ignore invalid image
    # ----------------

    if pix.height <= 0 or pix.width <= 0:
        return

    # Create a ParagImgTab instance
    # ----------------

    _img_elt: ParagImgTab = ParagImgTab(
        bbox=rect,
        str_itr='',
        prefix='',
        indent_prefix='',
        suffix='',
        lr_suffix=1,
        elt_type='image_vg',
        parags=[],
        spans_count=-1,
        italic_span_count=-1,
        bold_span_count=-1,
        superscript_span_count=-1,
        il_code_span_count=-1,
    )

    if PARAM['write_images'] is True:

        _img_ref: str = _write_image(
            page=page,
            i=i,
            pix=pix,
            PARAM=PARAM,
        )

        _img_elt.str_itr = (GRAPHICS_TEXT % _img_ref,)

    if PARAM['embed_images'] is True:

        _img_repr: str = _embed_image(
            pix=pix,
            PARAM=PARAM,
        )

        _img_elt.str_itr = (_img_repr,)

    parag_img_tabs.append(_img_elt)

    return


def process_image(
    parag_img_tabs: list[ParagImgTab],
    page: pymupdf.Page,
    img_rect: pymupdf.Rect,  # This is the image to be processed
    write_lines_for_write_image: Callable,
    i: int,
    img_rects: dict[int, pymupdf.Rect],
    PARAM: dict[str, str | int | bool | None],
) -> None:
    '''
    Converted into a partial in write_page; the partial is then called
    from output_images.

    Saves the image / vector graphic it is passed in to the specified
    directory with the specified resolution, extensions, etc. if
    PARAM['write_images'] is True.

    Converts the image / vector graphic to a base64 representation if
    PARAM['embed_images'] is True.

    Collects the corresponding filepath or base64 repr are saved into a dict
    that is added to parag_img_tabs.

    If PARAM['force_text'] is True, looks up text embedded within the
    images / vector graphics using the write_lines_in_img function within
    a clip limited to the image rectangle and appends any text line
    detected within the image as dict to parag_img_tabs.

    Returns a string list.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param page: pymupdf.Page: the current page.

    :param img_rect: pymupdf.Rect: the image rectangle.

    :param write_lines_for_write_image: Callable: a preconfigured partial
        function derived from write_line_in_img to be called from
        within write_image. write_lines_in_img contains a reference
        to dict_list.

    :param i: int: the image index in the list of images
        for the curent page.

    :param img_rects: dict[int, pymupdf.Rect]: a dict of image rectangles
        where the keys are the index numbers of the rectangles at
        extraction time.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.

    '''
    if PARAM['write_images'] is True or PARAM['embed_images'] is True:

        # get the string to the saved image or the string representing
        # the embedded image
        _save_or_embed_image(
            parag_img_tabs=parag_img_tabs,
            page=page,
            rect=img_rect,
            i=i,
            PARAM=PARAM,
        )

    # Collect any text that lives inside the image
    # param force_text is also usefull to ignore an image
    # background (ex. OCRed documents)
    if PARAM['force_text']:

        # NOTE: write_lines_for_write_image is a partial of
        # function `write_line_in_img` decorated with
        # `process_lines_in_rect_decorator` already configured
        # with the `parag_img_tabs`
        write_lines_for_write_image(
            clip=img_rect,
        )

    # Delete the image rectangle out of the dict of image rectangles
    # so that it not be filtered upon next iteration
    del img_rects[i]


#####################
# Output images iterator
#####################


def output_images(
    process_image_partial: Callable,
    img_list: list[tuple[int, pymupdf.Rect]],
) -> None:
    '''
    Receives a list of tuples idx-image rectangles, sorted by bottom y
    and left x and returns an iterable of strings, which may consists,
    for each image rectangle, of a filepath to the saved image if the
    write_images parameter is True, the identified embedded text chunks
    if force_text is True and/or the image embedded as a Base64-code
    line of data.

    :param process_image_partial: Callable: a preconfigured partial
        function derived from write_image.process_image to be called
        from within write_image.

    :param img_list: list[tuple[int, pymupdf.Rect]]: the filtered list
        of tuples idx-image Rectangles that are to be saved
        or converted to md_string or both.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
        a list of links for the current page.
    '''

    for i, img_rect in img_list:
        process_image_partial(
            img_rect=img_rect,
            i=i,
        )


def any_image_processing_requested(
    PARAM: dict[str, str | int | bool | None]
) -> bool:
    '''
    Returns False if any of the image processing parameter has been
    turned on.

    Returns True if all of the image processing parameters has been
    turned off.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.
    '''
    return any(
        [
            PARAM['write_images'] is True,
            PARAM['embed_images'] is True,
            PARAM['force_text'] is True,
        ]
    )
