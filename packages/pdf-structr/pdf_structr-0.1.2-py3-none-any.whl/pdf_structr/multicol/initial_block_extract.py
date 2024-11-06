# initial_block_extract.py
'''
Module to store the initial text blocks extraction.
'''

import functools
import logging
from typing import Callable

import pymupdf  # type: ignore
from pymupdf import IRect, Rect

# from pdf_struct.custrag_get_text_lines.make_spans_list import (
#     is_white,
# )
from pdf_structr.utils.utils import in_bbox

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


def _extend_block_rectangle_from_current_line(
    line: dict,
    lines_union_rect: Rect | IRect,
) -> Rect | IRect:
    '''
    Checks if a line contains text and if so, extend the
    block's Rectangle being rebuilt from the lines with
    this line's bbox Rectangle.

    :param line: dict: a pymupdf line dictionary.
    :param lines_union_rect: Rect | IRect: the block's rectangle
        currently being built from the lines it contains.
    '''
    # get the current line's bbox
    _line_bbox: Rect = Rect(line["bbox"])

    # NOTE: Since the text length of the lines (without white spans)
    # is now computed in the stats module, we can rely on
    # `if line['txt_len] > 0:` instead of the
    # `"".join()` followed by `if not is_white(_text)`
    #
    # Former code
    # # join the text of the spans in the current line
    # # _text: str = "".join([_span["text"] for _span in line["spans"]])
    # # If there is some text in the line
    # # if not is_white(_text):

    # New code
    # If there is some text in the line
    if line['txt_len'] > 0:

        # extend the block rectangle with the line rectangle
        lines_union_rect |= _line_bbox

    return lines_union_rect


def _build_lines_rect(block: dict) -> Rect | IRect:
    '''
    Build a block's rectangle by making the union of its lines' rectangles.

    :param block: dict: a pymupdf block of text.
    '''
    # create an empty rectangle to store the block's Rectangle rebuild
    # from its lines
    _lines_union_rect: Rect | IRect = pymupdf.EMPTY_IRECT()
    # NOTE: Replacing the preeceding by the following is a minor change in
    # b86b33fe985f2b8f33eafd45a4fde3642d5a3805 on pymupdf/RAG, v. 0.0.15
    # but it causes a ValueError: bad operand 2 error when using the
    # resulting Rect/IRect with & in the `write_lib` module.
    # _lines_union_rect: IRect = pymupdf.EMPTY_RECT()

    # iterate on the block's lines and populate the block's rectangle
    for _line in block["lines"]:
        _lines_union_rect = _extend_block_rectangle_from_current_line(
            line=_line,
            lines_union_rect=_lines_union_rect,
        )

    return _lines_union_rect


def _simpler_populate_text_bboxes_lists(
    block: dict,
    bbox: Rect,
    vert_bboxes: list[Rect],
    horiz_bboxes: list[Rect],
) -> None:
    '''
    Populates the lists of bboxes' Rectangles (for the horizontal text blocks
    and for the vertical text blocks) from one of the blocks on the page.

    :param block: dict: a pymupdf text block dictionary.

    :param bbox: Rect: the current block bbox rectangle.

    :param vert_bboxes: list[Rect]: a list of vertical bbox Rectangles
        currently being build for the current page.

    :param horiz_bboxes: list[Rect]: a list of horizontal
        bbox Rectangles currently being build for the current page.
    '''
    # check if first line is horizontal
    # only accept (almost) horizontal text and store non-horizontal blocks
    # bboxes into vert_bboxes
    if abs(1 - block["lines"][0]["dir"][0]) > 1e-3:
        vert_bboxes.append(bbox)
        return

    # adjust the current block's bbox rectangle by the
    # union rectangle of the rectangles of the lines it contains
    # NOTE: adjustement of blocks bboxes to the lines they contain
    # shall have been done in `clean_dicts_augment_spans` at the
    # beginning of extract_rects. Consider deleting.
    bbox = +_build_lines_rect(block=block)

    # If the resulting block's rectangle bbox is empty (i.e. invalid),
    # continue
    if bbox.is_empty:
        return

    # append it to the list of bboxes
    horiz_bboxes.append(bbox)


def _is_acceptable_block(
    block_lines: list[dict],
    bbox: Rect,
    no_image_text: bool,
    avoid_bboxes: list[Rect],
) -> bool:
    '''
    Check whether a block is not inside an "avoid" zones (a table, an image
    or a vg cluster) and returns True or False.

    block_lines: list[dict]: the lines in the block.

    :param bbox: Rect: the current block bbox rectangle.

    :param no_image_text: bool: a boolean indicating whether we want to ignore
        text inside image bboxes. True = ignore.

    :param avoid_bboxes: list[Rect]: a list of bbox Rectangles for the images,
        tables and vg clusters on the current page, to be avoid if
        `no_image_text` is True.
    '''
    # the text is inside an avoid_bbox (image, table or vg_cluster)
    if no_image_text and (in_bbox(bbox, avoid_bboxes)):
        return False

    # there are no lines inside the blocks
    # NOTE: so-called "white blocks" have been filtered earlier in the process
    # consider removing this
    if not block_lines:
        return False

    return True


def populate_initial_bboxes_list(
    blocks: list[dict],
    no_image_text: bool,
    avoid_bboxes: list[Rect],
    path_rects: list[Rect],
) -> tuple[list[Rect], list[Rect]]:
    '''
    Iterates on the blocks extracted from the textpage via
    `extractDICT()["blocks"]`. For each block, make the block's
    rectangle from its lines rectangles.

    The bboxes of each horizontal text block are appended to a list
    of bbox Rectangles.
    The bboxes of the some of the vertical text blocks are appended
    to a second list of bbox Rectangles.

    :returns: a 2-tuple, with two lists of bboxes' Rectangles from the page:
    - the horizontal text blocks
    - the vertical text blocks

    :param blocks: list[dict]: a list of blocks extracted by
        textpage.extractDICT()["blocks"].

    :param no_image_text: bool: a boolean indicating whether we want to ignore
        text inside image bboxes. True = ignore.

    :param avoid_bboxes: list[Rect]: a list of bbox Rectangles for the images,
        tables and vg clusters on the current page, to be avoid if
        `no_image_text` is True.

    :param path_rects: list[Rect]: a list of bbox Rectangles for the paths
        on the current page.
    '''
    # Declare a list of bboxes
    _horiz_bboxes: list[Rect] = []

    # Declare a list of non-horizontal text bboxes to
    # avoid when expanding horizontal text boxes
    _vert_bboxes: list[Rect] = []

    # Make block rectangles, ignoring non-horizontal text
    # and text living inside images if so requested
    _populate_text_bboxes_lists_partial: Callable = functools.partial(
        _simpler_populate_text_bboxes_lists,
        vert_bboxes=_vert_bboxes,
        horiz_bboxes=_horiz_bboxes,
    )

    # Make an _is_acceptable_block partial, to simplify the test inside
    # the loop
    _is_acceptable_block_partial: Callable = functools.partial(
        _is_acceptable_block,
        no_image_text=no_image_text,
        avoid_bboxes=avoid_bboxes,
    )

    # Walk the blocks
    for _block in blocks:

        # Get the block's bbox
        _bbox: Rect = Rect(_block["bbox"])

        # If the block is not text embedded in an image
        # or an identified table and the block contains lines
        if _is_acceptable_block_partial(
            block_lines=_block['lines'],
            bbox=_bbox,
        ):

            # push the vertical blocks in the vert_bboxes list
            # push the horizontal blocks in the horiz_bboxes list
            _populate_text_bboxes_lists_partial(
                block=_block,
                bbox=_bbox,
            )

    # Sort horizontal text bboxes by:
    # 1. text with no background > text with no background
    # 2. then top coordinates
    # 3. then left coordinates
    _horiz_bboxes.sort(
        key=lambda _horiz_bb: (
            in_bbox(_horiz_bb, path_rects),  # no background > background
            _horiz_bb.y0,  # top to bottom
            _horiz_bb.x0,  # left to right
        )
    )

    # Extend _horiz_bboxes to the right where possible
    # _horiz_bboxes = extend_right(
    #     _horiz_bboxes, int(page.rect.width),
    #     _path_bboxes, _vert_bboxes, img_bboxes
    # )

    return _horiz_bboxes, _vert_bboxes


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
