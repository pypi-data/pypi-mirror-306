# write_lines_lib.py
'''
Provides low level functions to write_page,
write_lines_in_img, write_lines_in_txt_rect,
write_spans and join_lines modules.
'''

import functools
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.get_text_lines.main import (
    get_raw_lines_core,
)
from pdf_structr.write.join_lines import (
    add_lrs_to_last_line_of_txt_cluster,
)
from pdf_structr.write.line_img_tab import ParagImgTab

#####################
# Process lines iterator decorator
#####################


def process_lines_iterator_decorator(process_line_func: Callable) -> Callable:
    '''
    This decorator provides a wrapper around an iterator that, for each line
    in a lines list, passes its index (and the lines list) to one of the
    process_line_func (which may be the function processing the lines in a
    text (column) Rectangle or the one processing the lines in an image
    Rectangle).

    :param process_line_func: Callable: may be one of:
        `write_text_line_and_above()` in module `write_line` or
        `_write_line_in_img()` in module `write_lines_in_img`.
    '''

    @functools.wraps(process_line_func)
    def process_lines_iterator(*args, **kwargs) -> None:
        # Walk the lines calling the line processing function
        # on each of them
        # The conversion result of each line is stored in
        # parag_img_tabs
        for _idx in range(0, len(kwargs['nlines'])):
            process_line_func(
                *args,
                **kwargs,
                # nlines=kwargs['nlines'],
                idx=_idx,
            )

    return process_lines_iterator


#####################
# Get raw lines wrapper
#####################


def get_raw_lines_wrapper(
    clip: pymupdf.Rect,
    blocks: list[dict],
    y_delta: float = 3,
) -> tuple[
    list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect,
                ]
            ],
        ]
    ],  # _nlines: list of lines extracted by get_raw_lines()
    dict[str, pymupdf.Rect | None | int | bool | str],  # context dict
]:
    '''
    Wrapper around the `get_raw_lines_core` function.

    Prepares the parsing of the lines by:
    - extracting the lines from the current rectangle (defined in the
    clip param of the kwargs) via a call to the `get_raw_lines_core`
    function,
    - initializing the context_dict to be used within the iteration
    on the lines.

    :returns: a 2-tuple with:
    - the list of lines within the clip, as 2-tuples
    "line rectangle - list of spans"
    - the initialized context dict

    :param y_delta: float: thresholds (in pts) below which spans
        will be put on the same line if their top or bottom
        coordinates differ by no more than this value.

    Param within the kwargs dict:

    :param clip: pymupdf.Rect: the current rectangle to be parsed for
        text lines.

    :param blocks: list[dict]: the list of blocks for the
        current page.

    '''
    # This is a list of tuples, where each tuple contains:
    # - a line Rect
    # - the list of spans pertaining to the line
    _nlines: list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect,
                ]
            ],
        ]
    ] = get_raw_lines_core(
        clip=clip,
        blocks=blocks,
        y_delta=y_delta,
    )

    # store line rectangles
    # coming from commit 1e0f22648b5783b
    # line_rects.extend([__line[0] for __line in nlines])

    # Define a context dict to hold information about the previous
    # lines when processing the lines
    _context_dict: dict[str, pymupdf.Rect | None | int | bool | str] = {
        'prev_lrect': None,  # previous line rectangle
        'prev_bno': -1,  # block number of the previous line
        'code': False,  # is code mode on
        'prev_hdr_string': None,  # the previous header string
        'NLINES_COUNT': len(_nlines),  # the number of nlines
        # NOTE: refacto: NLINES_COUNT might no longer be used; remove?
        'idx': 0,  # the index number when iterating on the lines returned
        # by get_raw_lines
        'CLIP': clip,  # the clip within which the lines lived
    }

    return _nlines, _context_dict


#####################
# Process lines iterator decorator
#####################


def process_lines_in_rect_decorator(process_line_func: Callable) -> Callable:
    '''
    This decorator is called from module 'write_page' to process lines inside
    text rectangles and 'write_lines_in_image' to process lines inside image
    rectangles.

    :param process_line_func: Callable: the line processing function, which may
        be `write_text_line_and_above` when called from module 'write_page'
        or `write_line_in_img` when called from module 'write_lines_in_image'.
    '''

    @functools.wraps(process_line_func)
    def process_lines_wrapper(*args, **kwargs) -> None:
        '''
        This function gets a list of raw text lines extracted from a text or
        and image rectangle given as the argument to the `clip` parameter.

        It then passes each of these lines to the process_line_func function
        (either `write_text_line_and_above` or `write_line_in_img`, each
        decorated by the `process_lines_iterator_decorator`).

        The decorator iterates on each line and passes it to output
        its content (as well as, when walking the lines inside a text
        rectangle, any table and/or image living inside such rectangle)
        as elements in a ParagImgTab instance, that is stored inside a list.

        The returning list is then processed in write_page to form an
        md-string.

        -----------

        This is an alternative for plain text in that it outputs text
        enriched with markdown styling.

        The logic is capable of recognizing headers, body text, code blocks,
        inline code, bold, italic and bold-italic styling.
        There is also some effort for list supported (ordered / unordered) in
        that typical characters are replaced by respective markdown characters.

        'tab_rects'/'img_rects' are dictionaries of table, respectively image
        or vector graphic rectangles.

        General Markdown text generation skips these areas. Tables are written
        via their own 'to_markdown' method. Images and vector graphics are
        optionally saved as files and pointed to by respective markdown text.

        -----------

        The following parameters are required for both decorated functions
        (`write_text_line_and_above` and `write_line_in_img`):

        :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
            instances, each containing an iterable of strings corresponding to
            a line or an md-string formatted elements such as a table or the
            string associated with an image or vector graphic.

        :param line_os: list[Line]: a list of Line instances, which will
            hold each of the lines of the current rectangle.

        :param blocks: list[dict]: the text blocks previously extracted via
                textpage.extractDICT (in the multi_column package, for
                instance).

        :param get_header_id: Callable: a callable that permits identifying
            header and returns a string to format the md headers.

        :param clip: pymupdf.Rect: the zone to parse: a text or image
            rectangle.

        :param PARAM: dict[str, str | int | bool | None]: a dict containing
            constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
            'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
            'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

        :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None:
            a list of links for the current page.

        -----------

        The following additional parameters are required for
        `write_text_line_and_above`:

        :param page: pymupdf.Page: the current page.

        :param tables_tuple: tuple[
            list[dict[str, tuple[float, float, float, float] | int]],
            dict[int, str],
            dict[int, pymupdf.Rect],
        ]: a tuple containing the various table elements extracted from
            the page by extract_tables:
            - a list of tables bboxes, cols and rows
            - a numbered dict of tables md strings, ordered by y1 and x0
            - a numbered dict of tables rectangles, ordered by y1 and x0

        :param img_rects: dict[int, pymupdf.Rect]: an ordered dict of image
            and vg rectangles in the current page, sorted by by y1 and x0
            and where the keys are the index numbers at extraction time.

        :param tab_rects0: list[pymupdf.Rect]: the list of table
            rectangles identified for the current page, as updated
            with the remaining rectangles at the stage when the decorated
            function is being called.

        :param img_rects0: list[pymupdf.Rect]: the list of images
            rectangles identified for the current page, as updated
            with the remaining rectangles at the stage when the decorated
            function is being called.

        :param process_image_partial: Callable: a preconfigured partial
            function derived from write_image.process_image to be called
            from within write_image.

        -----------

        The following parameters are provided by the decorators:

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
            - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous
              line.
            Usefull to compute y_gap between lines.
            - prev_bno: int: block number of the previous line.
            - code: bool: flag to memorize whether the line is in an all
              monospaced font block or not.
            - prev_hdr_string: str | None: header string of the previous line.
            - 'NLINES_COUNT': int: the number of lines in the current clip.
            - 'idx': int: the index number of the current line.
            - 'CLIP': Rect: the rectangle of the current clip.
            - 'spans_count_in_line': int: the spans' count for the current
               line (or 0 upon initialization).

        '''
        # ------------------------------------------------
        # Set the _parag_img_tabs variables from the kwargs
        # ------------------------------------------------

        _parag_img_tabs: list[ParagImgTab] = kwargs.get(  # type: ignore
            'parag_img_tabs'
        )

        # ------------------------------------------------
        # Get the raw lines and the context dict
        # ------------------------------------------------

        # Define and set the variables to be used for the lines parsing:
        # - _nlines: the list of lines in the current rect.
        # - _context_dict: a context dict to hold information about the
        #   previous lines and processing stage when processing the lines.

        # NOTE: get_raw_lines_decorator does not take any value, because
        # it is only used to wrap `get_raw_lines_core`.
        kwargs['nlines'], kwargs['context_dict'] = get_raw_lines_wrapper(
            clip=kwargs.get('clip'),
            blocks=kwargs.get('blocks'),  # type: ignore
            # y_delta=3,
        )

        # ------------------------------------------------
        # Walk the lines into a list of ParagImgTab
        # ------------------------------------------------

        # Walk the lines calling the processing function
        # on each of them and store the processing result
        # in a list of Line instances (list[Line]).

        # The `process_line_func` may be either `write_text_line_and_above`
        # or `write_line_in_img`.

        process_lines_iterator_decorator(process_line_func=process_line_func)(
            *args, **kwargs
        )

        # ------------------------------------------------
        # Close rect
        # ------------------------------------------------

        # If nothing to close, return
        if (
            not _parag_img_tabs
            or not _parag_img_tabs[-1].parags
            or not _parag_img_tabs[-1].parags[-1].lines
        ):
            return

        # Else close the ParagImgTab
        # NOTE: will need to be refactored upon full integration of
        # parags
        add_lrs_to_last_line_of_txt_cluster(
            last_line=_parag_img_tabs[-1].parags[-1].lines[-1],
            context_dict=kwargs['context_dict'],
        )

        return

    return process_lines_wrapper


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
