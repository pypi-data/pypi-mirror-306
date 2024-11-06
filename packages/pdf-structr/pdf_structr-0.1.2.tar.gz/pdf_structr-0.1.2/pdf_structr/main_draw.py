# main_draw.py
'''
Module to encapsulate the various bboxes' borders drawing feature
and their specific decorators.
'''

import functools
import logging
from typing import Any, Callable

import pymupdf  # type: ignore

from pdf_structr.extract.extract import process_page_decorator
from pdf_structr.main_utils import (
    process_doc_decorator,
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


#####################
# Abstract drawing functions
#####################


def _draw_borders_for_rectangles_collection(
    shape: pymupdf.Shape,
    rects_collection: list[pymupdf.IRect],
    color: dict[Any, tuple],
    dashes: str = "",
    width: float = 1,
) -> None:
    '''
    Draws borders in the specified color around each of the elements of
    the passed-in rects_collection.

    :returns: nothing.

    :param shape: pymupdf.Shape: a shape canvas on which to draw elements.
    :param rects_collection: list[pymupdf.IRect]: a list of rectangles.
    :param color: dict[Any, tuple]: a pymupdf color dict (ex.
        `pymupdf.pdfcolor["red"]`)
    :param dashes: str = "": whether to draw the lines of the rectangles
        in dashes. "" defaults to no dashes. The param shall be as follows:
        "[3 4] 0", meaning dash of 3 pixels, gap of 4 pixels, offset at the
        beginning of 0 pixels.
    :param width: float = 1: the width of the lines of the rectangles.
    '''
    # iterate over the passed-in rects_collection
    for _i, _rect in enumerate(rects_collection):
        # draw a border
        shape.draw_rect(_rect)

        # write sequence number with an x-offset of 5 points
        # and an y-offset of 5 points from the top-left angle
        # of the rectangle.
        shape.insert_text(
            _rect.tl + (5, 5),
            str(_i),
            color=color,
        )

    # finish drawing with the passed in color
    shape.finish(
        color=color,
        dashes=dashes,
        width=width,
    )


#####################
# Decorator
#####################


def draw_elts_collection_on_doc(filename_suffix: str):
    '''
    Decorator to decorate page level drawing functions; the wrapper
    function below includes all the document preprocessing via the decoration
    by `@process_doc_decorator`.

    :param filename_suffix: str: the filename suffix to add at the end
        of the file to be created. This is not an extension, this is
        a suffix that will be inserted between the original filename
        and its extension.
    '''

    def draw_elts_coll_on_doc_decorator(
        page_levl_drawing_func: Callable,
    ) -> Callable:
        '''
        Decorator to decorate page level drawing functions; the wrapper
        function below includes all the document preprocessing via
        the decoration by `@process_doc_decorator`.

        :param page_levl_drawing_func: Callable: the function that draws
            a collection of bbox Rectangles on a page.
        '''

        @functools.wraps(page_levl_drawing_func)
        @process_doc_decorator
        def draw_elts_coll_on_doc_wrapper(*args, **kwargs) -> None:

            [
                page_levl_drawing_func(
                    page=kwargs['doc'][pno],
                    margins=kwargs['margins'],
                    table_strategy=kwargs['table_strategy'],
                    textflags=kwargs['textflags'],
                    get_header_id=kwargs['get_header_id'],
                    PARAM=kwargs['PARAM'],
                )[0]
                for pno in kwargs['pages']
            ]

            _filename: str = kwargs['doc'].name

            # save document with the drawn bboxes
            kwargs['doc'].ez_save(
                _filename.replace(".pdf", f"-{filename_suffix}.pdf")
            )

        return draw_elts_coll_on_doc_wrapper

    return draw_elts_coll_on_doc_decorator


def _draw_borders_for_elt_cat_decorator(
    abs_drawing_func: Callable,
) -> Callable:
    '''
     Decorator for abstract drawing functions (i.e. function drawing shapes
     on PDFs) that needs a shape canvas.

     Usage: for a drawing function called
     `_draw_borders_for_rectangles_collection` that takes:
     - a shape argument,
     - a rects_collection argument,
     - a color argument,
     the function can be decorated and called as follows from within
     Python code:

     ```python

     _draw_borders_for_elt_cat_decorator(
         _draw_borders_for_rectangles_collection
     )(
         page=page,
         rects_collection=[pymupdf.Rect(block['bbox']) for block in blocks],
         color=pymupdf.pdfcolor["red"],
     )

     ```

     Otherwise, the function may also be decorated using the @ notation:
    ` @_draw_borders_for_elt_cat_decorator`.

     :param `abs_drawing_func`: Callable: an abstract drawing function that
         should take, at least, a `shape` keyword argument. The wrapper
         function provides the `shape` argument to the decorated function.
    '''

    @functools.wraps(abs_drawing_func)
    def _draw_borders_for_elt_cat_wrapper(
        page: pymupdf.Page,
        *args,
        **kwargs,
    ) -> None:
        '''
        Initializes the shape on the page for the abstract drawing function,
        passes it to the drawing function, executes the drawing function and
        commits the shape.

        :param page: pymupdf.Page: the page on which the drawing is going to
            be made.
        '''
        # prepare a canvas to draw rectangles and text
        _shape: pymupdf.Shape = page.new_shape()

        # Execute drawing function
        abs_drawing_func(*args, shape=_shape, **kwargs)

        # store to the page
        _shape.commit()

    return _draw_borders_for_elt_cat_wrapper


#####################
# Concrete drawing functions
#####################


@draw_elts_collection_on_doc(filename_suffix='blocks')
@process_page_decorator
def draw_page_blocks_bboxes(
    page: pymupdf.Page,
    blocks: list[dict],
    *args,
    **kwargs,
) -> None:
    '''
    Draws borders around the text blocks identified by the preparatory steps
    of custom RAG.

    :returns: nothing.

    :param page: pymupdf.Page: the current pymupdf Page.
    :param blocks: list[dict]: the blocks extracted from the page via
        textpage.extract_DICT()
    '''
    _draw_borders_for_elt_cat_decorator(
        _draw_borders_for_rectangles_collection
    )(
        page=page,
        rects_collection=[pymupdf.Rect(block['bbox']) for block in blocks],
        color=pymupdf.pdfcolor["red"],
    )


@draw_elts_collection_on_doc(filename_suffix='blocks-lines-spans')
@process_page_decorator
@_draw_borders_for_elt_cat_decorator
def draw_page_blocks_lines_and_spans_bboxes(
    shape: pymupdf.Shape,
    blocks: list[dict],
    *args,
    **kwargs,
) -> None:
    '''
    Draws borders around the blocks, lines and spans
    after cleaning by custrag.

    :returns: nothing.

    :param shape: the shape on the page on which the various elements are
        going to be drawn.
    :param blocks: list[dict]: the blocks extracted from the page via
        textpage.extract_DICT()
    '''
    _RED: dict[Any, tuple] = pymupdf.pdfcolor["red"]
    _GREEN: dict[Any, tuple] = pymupdf.pdfcolor["green"]
    _BLUE: dict[Any, tuple] = pymupdf.pdfcolor["blue"]

    _draw_borders_for_rectangles_collection_partial: Callable = (
        functools.partial(_draw_borders_for_rectangles_collection, shape=shape)
    )

    # Draw the blocks rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=(pymupdf.Rect(_block['bbox']) for _block in blocks),
        color=_RED,
        dashes="[3 6] 0",
        width=1.5,
    )

    # Draw the lines rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=(
            pymupdf.Rect(_line['bbox'])
            for _block in blocks
            for _line in _block['lines']
        ),
        color=_BLUE,
        dashes="[2 4] 3",
        width=1,
    )

    # Draw the spans rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=(
            pymupdf.Rect(_span['bbox'])
            for _block in blocks
            for _line in _block['lines']
            for _span in _line['spans']
        ),
        color=_GREEN,
        dashes="[0.5 0.5] 0",
        width=0.5,
    )


@draw_elts_collection_on_doc(filename_suffix='elts')
@process_page_decorator
@_draw_borders_for_elt_cat_decorator
def draw_page_elts_bboxes(
    shape: pymupdf.Shape,
    text_rects: list[pymupdf.IRect],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    vg_clusters: dict[int, pymupdf.Rect],
    *args,
    **kwargs,
) -> None:
    '''
    Draws borders around the text, table and image-vg bboxes identified
    by the preliminary steps of custom RAG.

    :returns: nothing.

    :param shape: the shape on the page on which the various elements are
        going to be drawn.

    :param text_rects: list[pymupdf.IRect]: the text rectangles to be drawn
        on the page.

    :param tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ]: a tuple containing the various table elements extracted from
        the page by extract_tables:
        - a list of tables bboxes, cols and rows
        - a numbered dict of tables md strings, ordered by y1 and x0
        - a numbered dict of tables rectangles, ordered by y1 and x0

    :param vg_clusters: dict[int, pymupdf.Rect]: the image and vector-graphic
        rectangles to be drawn on the page.
    '''
    _RED: dict[Any, tuple] = pymupdf.pdfcolor["red"]
    _GREEN: dict[Any, tuple] = pymupdf.pdfcolor["green"]
    _BLUE: dict[Any, tuple] = pymupdf.pdfcolor["blue"]

    _draw_borders_for_rectangles_collection_partial: Callable = (
        functools.partial(_draw_borders_for_rectangles_collection, shape=shape)
    )

    # Draw the text rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=text_rects,
        color=_RED,
    )

    # Draw the table rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=tables_tuple[2].values(),  # type: ignore
        color=_GREEN,
    )

    # Draw the image and vg clusters rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=vg_clusters.values(),  # type: ignore
        color=_BLUE,
    )


#####################
# Concrete drawing functions for zones
# NOTE: Dead code - zones are no longer identified in the document.
#####################


@draw_elts_collection_on_doc(filename_suffix='horiz-zones')
@process_page_decorator
@_draw_borders_for_elt_cat_decorator
def draw_page_horizontal_zones_bboxes(
    shape: pymupdf.Shape,
    layout_dict: dict[str, list | dict],
    *args,
    **kwargs,
) -> None:
    '''
    Draws borders around the so-called horizontal text "zones"
    identified by the preliminary steps of custom RAG and stored
    in the `layout_dict`.

    :returns: nothing.

    :param shape: the shape on the page on which the various elements are
        going to be drawn.
    :param layout_dict: dict[str, list | dict]: the layout dict containing
        layout zones to be drawn on the page.
    '''
    _RED: dict[Any, tuple] = pymupdf.pdfcolor["red"]

    _draw_borders_for_rectangles_collection_partial: Callable = (
        functools.partial(_draw_borders_for_rectangles_collection, shape=shape)
    )

    # Draw the horizontal zones rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=(rect[0] for rect in layout_dict['horizontal_rects']),
        color=_RED,
    )


@draw_elts_collection_on_doc(filename_suffix='vertic-zones')
@process_page_decorator
@_draw_borders_for_elt_cat_decorator
def draw_page_vertical_zones_bboxes(
    shape: pymupdf.Shape,
    layout_dict: dict[str, list | dict],
    *args,
    **kwargs,
) -> None:
    '''
    Draws borders around the so-called vertical text "zones"
    identified by the preliminary steps of custom RAG.

    :returns: nothing.

    :param shape: the shape on the page on which the various elements are
        going to be drawn.

    :param layout_dict: dict[str, list | dict]: the layout dict containing
        layout zones to be drawn on the page.
    '''
    _RED: dict[Any, tuple] = pymupdf.pdfcolor["red"]
    # _GREEN: dict[Any, tuple] = pymupdf.pdfcolor["green"]

    _draw_borders_for_rectangles_collection_partial: Callable = (
        functools.partial(_draw_borders_for_rectangles_collection, shape=shape)
    )

    # Draw the vertical zones rectangles
    _draw_borders_for_rectangles_collection_partial(
        rects_collection=(
            rect[0]
            for hzone_container in layout_dict['vertical_rects']
            for rect in hzone_container
            if rect[1] != 'intertext'
        ),
        color=_RED,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
