# extract.py
'''
Module that stores the main process_page_decorator()
that calls the functions extracting the various elements
from the page and then calls the function that will
process the page into something, such as an md string.

This function prepares the extraction by requesting a page map
from extract_elts_from_page().

Once it has received this map, it calls get_md_string_for_page()
to produce a markdown string out of the page.

'''
import functools
from typing import Callable

# try:
#     import pymupdf as pymupdf  # available with v1.24.3
# except ImportError:
#     import pymupdf
import pymupdf  # type: ignore

from pdf_structr.extract.extract_rects import extract_elts_from_page

# if pymupdf.pymupdf_version_tuple < (1, 24, 2):
#     raise NotImplementedError("PyMuPDF version 1.24.2 or later is needed.")


#####################
# Subfunctions
#####################


def _test_graphics_limits(
    page: pymupdf.Page,
    GRAPHICS_LIMIT: int | None,
) -> str:
    '''
    Test if the page has too many graphics and exclude it if so.
    '''
    # Excluding pages with too many graphics
    # catch too-many-graphics situation
    if GRAPHICS_LIMIT is None:
        return ''

    test_paths = page.get_cdrawings()  # fastest access to graphics
    if (excess := len(test_paths)) > GRAPHICS_LIMIT:
        return (
            f"\n**Ignoring page {page.number} with "
            f"{excess} vector graphics.**"
            "\n\n-----\n\n"
        )

    return ''


def _extract_elts_from_page_wrapper(
    page: pymupdf.Page,
    GRAPHICS_LIMIT: int | None,
    margins,
    textflags,
    table_strategy,
) -> bool | dict:
    '''
    Function that wraps a call to `extract_elts_from_page`
    and returns either False if the page exceeds the graphics
    limit or convert the tuple returned by `extract_elts_from_page`
    into a dict otherwise.

    `extract_elts_from_page` (module `extract_rects`) extracts the
    following elements from a page:
    - a textpage
    - the links
    - information on the images
    - the tables,
    - the vector graphics rectangles and
    - the text rectangles.
    '''
    ###################
    # Remove any rotation to the page
    ###################
    page.remove_rotation()  # make sure we work on rotation=0

    ###################
    # Exclude pages with too many graphics
    ###################

    if _test_graphics_limits(
        page=page,
        GRAPHICS_LIMIT=GRAPHICS_LIMIT,  # type: ignore
    ):
        return False

    ###################
    # Prepare md_string production by mapping the
    # rectangle elements on the page
    ###################

    (
        # the textpage for faster access down the pipe
        _textpage,
        # the blocks extracted via textpage.extractDICT
        # in the multi_column package.
        _blocks,
        # the text rectangles map
        _text_rects,
        # the table rectangles maps composed of:
        # - a list of tables bboxes, rows and columns
        # - a numbered dict of table md strings ordered by y1 and x0
        # - a numbered dict of table rectangles ordered by y1 and x0
        _tables_tuple,
        # the image rectangles map
        _img_info,
        # the vector graphics rectangles maps
        _graphics,  # bugged empty list
        _vg_clusters,  # numbered dict of VG Rect
        # the links rectangles maps
        _links,
        _layout_dict,
    ) = extract_elts_from_page(
        page=page,
        margins=margins,
        textflags=textflags,
        table_strategy=table_strategy,
    )

    return {
        'page': page,
        'textpage': _textpage,
        'blocks': _blocks,
        'text_rects': _text_rects,
        'tables_tuple': _tables_tuple,
        'img_info': _img_info,
        'graphics': _graphics,
        'vg_clusters': _vg_clusters,
        'links': _links,
        'layout_dict': _layout_dict,
    }


#####################
# Decorator
#####################


def process_page_decorator(process_page_func: Callable) -> Callable:
    '''
    Decorator providing a wrapper function that prepares the production
    of an md string by calling the function that extracts everything from
    the page (links, text, image, vg and table rectangles, etc.) and
    passes it to one of the wrapped function for processing.

    :param process_page_func: Callable: the function that will convert
        the page into another structure.
    '''

    @functools.wraps(process_page_func)
    def process_page_wrapper(
        *args,
        **kwargs,
    ) -> tuple[str, list, list, list]:
        '''
        First map and extract rectangles and other elements then process
        the page with the passed in `process_page_func` function.

        returns: a 4-tuple with:
        - the markdown string of page content and image, table and vector
          graphics information
        - a list of image information
        - a list of table information
        - a list of graphic vectors information (empty due to bug)

        The kwargs dictionary shall contain the following arguments:

        :param page: pymupdf.Page: the current page

        :param margins: tuple[float, float, float, float]: a 4-float
            tuple setting the margins from the sides of the page beyond
            which text, tables and graphics shall not be considered.
            ex. (0, 50, 0, 50).

        :param table_strategy: str: the table detection strategy. Valid values
            are "lines", "lines_strict" and "text". Default is "lines_strict"
            (ignores borderless rectangle vector graphics).
            "lines" uses all vector graphics on the page to detect grid lines.
            "text": text positions are used to generate "virtual" column
            and / or row boundaries.

        :param textflags: Union[int, int]: the applicable text flags for the
            TextPages extraction. Union in this context is equivalent to
            adding the values of the respective textflags. Defaults to 192
            as per the main decorator (i.e. TEXT_MEDIABOX_CLIP (64) and
            TEXT_CID_FOR_UNKNOWN_UNICODE (128)).

        :param get_header_id: Callable: the headers identifier callable.

        :param PARAM: dict[str, str | int | bool | None]: a dict containing
            constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
            'GRAPHICS_LIMIT', 'write_images', 'force_text' and 'IGNORE_CODE'.
        '''
        _prep_page_proc: bool | dict = _extract_elts_from_page_wrapper(
            page=kwargs['page'],
            GRAPHICS_LIMIT=kwargs['PARAM']['GRAPHICS_LIMIT'],  # type: ignore
            margins=kwargs['margins'],
            textflags=kwargs['textflags'],
            table_strategy=kwargs['table_strategy'],
        )

        # If too many graphics, _extract_elts_from_page_wrapper will
        # return False
        # We just want to pass the page
        # --> return empty string and empty lists
        if isinstance(_prep_page_proc, bool):
            return '', [], [], []

        # Else:

        # 1. update the kwargs dict with all the values returned by
        # _extract_elts_from_page_wrapper (textpage, text rectangles
        #  tables data structures, image and vector graphics, links, etc.)
        kwargs.update(_prep_page_proc)

        # 2. Process the page
        _md_string = process_page_func(*args, **kwargs)

        # 3. Return the md string and part of the data structures gathered with
        # _extract_elts_from_page_wrapper
        return (
            _md_string,
            _prep_page_proc['img_info'],
            _prep_page_proc['tables_tuple'][0],  # lst tbls bbxs, cols and rows
            _prep_page_proc['graphics'],
        )

    return process_page_wrapper


#######################################
# Extract words: code of line 773 to 788
# coming from commit 1e0f22648b5783b on pymupdf
#######################################


# def extract_unique_words(
#     textpage: pymupdf.TextPage, line_rects: list[pymupdf.Rect],
# ) -> list:
#     '''
#     Extracts the unique words from the page and return them in
#     the order they appear in the md string.

#     Refactoring of line 773 to 788 coming from commit 1e0f22648b5783b

#     :param textpage: pymupdf.TextPage: the textpage of the current page.
#     :param line_rects: list[pymupdf.Rect]: the list of line rectangles.
#     '''
#     # Declare a list of words as temp storage for the words extracted
#     # with textpage.extractWORDS()
#     _rawwords: list[  # old `rawwords`
#         tuple[float, float, float, float, str, int, int, int]
#     ] = textpage.extractWORDS()

#     # Declare a list of words to be returned
#     _words: list[list[float | str | int]] = []

#     # Iterate the line rectangles to sort the words in _rawwords
#     # in the same order as the markdown text
#     for _line_rect in line_rects:

#         # declare a list of words to store the line's words
#         _line_words: list = []

#         # iterate the _rawwords, filter the words to get the words
#         # in the current line and append them to the list of line's words
#         for _rawword in _rawwords:

#             # Get the coordinates out of the current _rawword tuple
#             # and create a Rectangle
#             _rawword_rect: pymupdf.Rect = pymupdf.Rect(_rawword[:4])

#             # If the current word rectangle is in the current
#             # line rectangle, modify the y coordinates of the
#             # current word rectangle and append the _rawword
#             # with the modified rectangle to the list of line's words
#             if _rawword_rect in _line_rect:
#                 # set upper coord to line
#                 _rawword_rect.y0 = _line_rect.y0
#                 # set lower coord to line
#                 _rawword_rect.y1 = _line_rect.y1
#                 # append the modified _rawword to the list of line's words
#                 _line_words.append(
#                     list(_rawword_rect) + list(_rawword[4:])
#                 )
#         # sort the words by x0 and append them to the list of
#         # words to return
#         _words.extend(sorted(_line_words, key=lambda _word: _word[0]))

#     # remove word duplicates without spoiling the sequence
#     # duplicates may occur for multiple reasons

#     # define a list to host the words without duplicates
#     _unique_words: list[list[float | str | int]] = []  # old `nwords`
#     # walk the words
#     for _word in _words:
#         # check if the current _word is in _nwords
#         if _word not in _unique_words:
#             # if not, add it to the _words
#             _unique_words.append(_word)

#     return _unique_words
