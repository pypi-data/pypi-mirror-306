# main.py
"""
Base: pymupdf4llm/helpers/multi_column.py
Commit on pymupdf/RAG: 1e0f226

This is an advanced PyMuPDF utility for detecting multi-column pages.
It can be used in a shell script, or its main function can be imported and
invoked as descript below.

Features
---------
- Identify text belonging to (a variable number of) columns on the page.
- Text with different background color is handled separately, allowing for
  easier treatment of side remarks, comment boxes, etc.
- Uses text block detection capability to identify text blocks and
  uses the block bboxes as primary structuring principle.
- Supports ignoring footers via a footer margin parameter.
- Returns re-created text boundary boxes (integer coordinates), sorted
  ascending by the top, then by the left coordinates.

Restrictions
-------------
- Only supporting horizontal, left-to-right text
- Returns a list of text boundary boxes - not the text itself. The caller is
  expected to extract text from within the returned boxes.
- Text written above images is ignored altogether (option).
- This utility works as expected in most cases. The following situation cannot
  be handled correctly:
    * overlapping (non-disjoint) text blocks
    * image captions are not recognized and are handled like normal text

Usage
------
- As a CLI shell command use

  python multi_column.py input.pdf footer_margin header_margin

  Where margins are the height of the bottom / top stripes to ignore on each
  page.
  This code is intended to be modified according to your need.

- Use in a Python script as follows:

  ----------------------------------------------------------------------------------
  from multi_column import column_boxes

  NOTE: see the new return value of column_boxes() below.
  # for each page execute
  bboxes = column_boxes(page, footer_margin=50, no_image_text=True)

  bboxes is a list of pymupdf.IRect objects, that are sorted ascending by their
  y0, then x0 coordinates. Their text content can be extracted by all PyMuPDF
  get_text() variants, like for instance the following:
  for rect in bboxes:
      print(page.get_text(clip=rect, sort=True))
  ----------------------------------------------------------------------------------

Dependencies
-------------
PyMuPDF v1.24.2 or later

Copyright and License
----------------------
Copyright 2024 Artifex Software, Inc.
License GNU Affero GPL 3.0

Additional comments to the refactored version
---------------------------------------------

This is the main module of the package.

Submodules by order of call in column_boxes():
- img_path_extract
- initial_block_extract
- make_column_bboxes
- post_processing
"""

import pymupdf  # type: ignore
from pymupdf import IRect, Page, Rect  # type: ignore

from pdf_structr.multicol.img_path_extract import (
    get_path_bboxes_list,
    make_avoid_bboxes_list,
)
from pdf_structr.multicol.initial_block_extract import (
    populate_initial_bboxes_list,
)
from pdf_structr.multicol.make_columns import make_column_bboxes

# from pdf_struct.mo_utils.timer import count_and_avg_timer


# NOTE: The following is a major change in
# b86b33fe985f2b8f33eafd45a4fde3642d5a3805 on pymupdf/RAG, v. 0.0.15
pymupdf.TOOLS.set_small_glyph_heights(True)


#####################
# Main API
#####################


def _prepare_column_extraction(
    page: Page,
    blocks: list[dict],
    *,
    paths: list[dict],
    no_image_text: bool = True,
    # Actually, it is not None, but it may be an empty list
    avoid: list[Rect] | None = None,
) -> tuple[list[Rect], list[Rect], list[Rect]]:
    '''
    Get an horizontal, a vertical and a paths rectangles' list and return
    them to the caller.

    :param page: Page: required. The current page.

    :param blocks: list[dict]: the list of blocks extracted from the
        current page via textpage.extractDICT(sort=True)["blocks"].

    :param no_image_text: bool = True: ignore text inside image bboxes.

    :param paths: list[dict]: a list of the previously extracted paths.

    :param avoid: list[Rect] | None = None: ignore text in any of these areas.
        This is a list of Rect-likes, whichhave been extracted previously
        and covering vector graphic clusters and tables.
    '''
    # --------------------------------------------------------------------
    # Get path and image blocks from the page
    # --------------------------------------------------------------------
    # Declare a list of vg bboxes and populate it
    _path_rects: list[Rect] = get_path_bboxes_list(paths=paths)

    # Declare a list of bboxes to avoid in case no_image_text is True
    # and populate it
    # # # Declare a list of image bboxes and populate it
    # NOTE: maybe an empty list if no_image_text is True
    _avoid_bboxes: list[Rect] = make_avoid_bboxes_list(
        page=page,
        avoid=avoid,
        no_image_text=no_image_text,
    )

    # --------------------------------------------------------------------
    # Get text blocks from the page
    # --------------------------------------------------------------------

    # Get two lists of bboxes' Rectangles from the page:
    # - one for the horizontal text blocks
    # - one for the vertical text blocks
    _horiz_txt_bboxes, _vert_txt_bboxes = populate_initial_bboxes_list(
        blocks=blocks,
        no_image_text=no_image_text,
        # img_bboxes=_img_bboxes,
        avoid_bboxes=_avoid_bboxes,
        path_rects=_path_rects,
    )

    return _horiz_txt_bboxes, _vert_txt_bboxes, _path_rects


# @count_and_avg_timer(name='prep - column_boxes')
def column_boxes(
    page: Page,
    blocks: list[dict],
    *,
    paths: list[dict],
    no_image_text: bool = True,
    # Actually, it is not None, but it may be an empty list
    avoid: list[Rect] | None = None,
    join_distant_y_rect: bool = True,
) -> list[Rect | IRect]:
    """
    Determine bboxes which wrap the so-called "columns" on the page.

    Columns correspond to a series of geometrically homogeneous paragraphs
    eventually separated from other similar series by a whitespace larger
    than is usual between the members of the column.

    This function returns a list of IRect, where each IRect corresponds
    to one such grouping. Every such IRect can then be used as a clip
    in one of the textpage text extraction methods.

    The processing goes along these lines:
    1. get the bboxes for the paths and the images on the page.
    2. transform the passed-in list of blocks bboxes extracted via
       textpage.extractDICT()["blocks"] into two list, one for each of the
       vertical and horizontal text direction.
    3. create geometrically homogeneous groups of horizontal text
       blocks by detecting a first text block on the page and
       extending its rect to the following.

    :returns: list[IRect: a list of the Rect containing text on the
        current page.

    :param page: Page: required. The current page.

    :param blocks: list[dict]: the list of blocks extracted from the
        current page via textpage.extractDICT(sort=True)["blocks"].

    :param no_image_text: bool = True: ignore text inside image bboxes.

    :param paths: list[dict]: a list of the previously extracted paths.

    :param avoid: list[Rect] | None = None: ignore text in any of these areas.
        This is a list of Rect-likes, whichhave been extracted previously
        and covering vector graphic clusters and tables.

    :param join_distant_y_rect: bool = True: if set to True, will try to join
        text rectangles that are separated by a large vertical white space but
        which x coordinates are not covering any other left or right columns
        into a single column. If set to False, the text rectangles will remaing
        separated and sorted by y0 and x0, resulting in the conversion of a
        'table like' layout to a linear one.

    """
    # --------------------------------------------------------------------
    # Get three Rectangles' list for the horizontal text blocks,
    # the vertical text blocks and the paths.
    # --------------------------------------------------------------------
    _horiz_txt_bboxes, _vert_txt_bboxes, _path_rects = (
        _prepare_column_extraction(
            page=page,
            blocks=blocks,
            paths=paths,
            no_image_text=no_image_text,
            avoid=avoid,
        )
    )

    # immediately return if no horizontal text found
    if not _horiz_txt_bboxes:
        return []

    # --------------------------------------------------------------------
    # Join bboxes to establish some column structure
    # --------------------------------------------------------------------

    # Iterate the horizontal text bbox Rectangles
    # and make columns' bboxes
    return make_column_bboxes(
        # we prepopulate the column_bboxes with the first horizontal
        # text bbox Rectangle in the _horiz_txt_bboxes list
        column_bboxes=[_horiz_txt_bboxes[0]],
        # we pass it only the remaining horizontal text bbox Rectangles
        # the first one has already been added to _column_blocks
        horiz_bboxes=_horiz_txt_bboxes[1:],
        path_bboxes=_path_rects,
        vert_bboxes=_vert_txt_bboxes,
        path_rects=_path_rects,
        join_distant_y_rect=join_distant_y_rect,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == "__main__":
    pass
