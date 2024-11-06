# make_chars.py
'''
Encapsulation of the `table.make_chars()` function into its own module
for refactoring purposes.
'''

from typing import Any, Generator

from pymupdf import (  # type: ignore
    Matrix,
    Page,
    Point,
    Rect,
    TextPage,
    sRGB_to_pdf,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


def _make_char_dict(
    char,
    ctm,
    matrix,
    upright,
    doctop_base,
    fontname,
    color,
    page_number,
    fontsize,
):
    '''
    Function encapsulating the final stage of making the char_dict
    in `make_chars`.
    '''

    bbox = Rect(char["bbox"])
    bbox_ctm = bbox * ctm
    origin = Point(char["origin"]) * ctm
    matrix.e = origin.x
    matrix.f = origin.y
    text = char["c"]

    return {
        "adv": (bbox.x1 - bbox.x0 if upright else bbox.y1 - bbox.y0),
        "bottom": bbox.y1,
        "doctop": bbox.y0 + doctop_base,
        "fontname": fontname,
        "height": bbox.y1 - bbox.y0,
        "matrix": tuple(matrix),
        "ncs": "DeviceRGB",
        "non_stroking_color": color,
        "non_stroking_pattern": None,
        "object_type": "char",
        "page_number": page_number,
        "size": fontsize if upright else bbox.y1 - bbox.y0,
        "stroking_color": color,
        "stroking_pattern": None,
        "text": text,
        "top": bbox.y0,
        "upright": upright,
        "width": bbox.x1 - bbox.x0,
        "x0": bbox.x0,
        "x1": bbox.x1,
        "y0": bbox_ctm.y0,
        "y1": bbox_ctm.y1,
    }


def _make_char_dicts(
    span,
    ctm,
    matrix,
    upright,
    doctop_base,
    page_number,
) -> Generator[dict, Any, Any]:
    '''
    Function encapsulating the final stage of making the char_dict
    in `make_chars`.
    '''

    fontname = span["font"]
    fontsize = span["size"]
    color = sRGB_to_pdf(span["color"])
    span["chars"].sort(key=lambda c: c["bbox"][0])
    return (
        _make_char_dict(
            char,
            ctm,
            matrix,
            upright,
            doctop_base,
            fontname,
            color,
            page_number,
            fontsize,
        )
        for char in span["chars"]
    )


def _make_char_dicts_for_line(
    line,
    ctm,
    doctop_base,
    page_number,
) -> Generator[dict, Any, Any]:
    ldir = line["dir"]  # = (cosine, sine) of angle
    ldir = (round(ldir[0], 4), round(ldir[1], 4))
    matrix = Matrix(ldir[0], -ldir[1], ldir[1], ldir[0], 0, 0)
    if ldir[1] == 0:
        upright = True
    else:
        upright = False
    #
    line["spans"].sort(key=lambda s: s["bbox"][0])
    return (
        char
        for span in line["spans"]
        for char in _make_char_dicts(
            span,
            ctm,
            matrix,
            upright,
            doctop_base,
            page_number,
        )
    )


# -----------------------------------------------------------------------------
# Extract all page characters to fill the CHARS list
# -----------------------------------------------------------------------------


# @count_and_avg_timer(name='prep - make_chars')
def make_chars(page: Page, textpage: TextPage) -> Generator[dict, Any, Any]:
    """
    Extract text as "rawdict" to fill CHARS.

    :returns: a generator of char dict for the current page.

    :param page: Page: the current page.

    :param textpage: TextPage: the corresponding textpage.

    """
    page_number = page.number + 1
    page_height = page.rect.height
    ctm = page.transformation_matrix

    # Save in global TEXTPAGE for reuse
    # Timing: 4.616 milliseconds

    # rawdict: extracts at the level of char dict
    # Timing: 4.619 milliseconds
    blocks = page.get_text("rawdict", textpage=textpage)["blocks"]

    doctop_base = page_height * page.number

    # Timing: 4.655 milliseconds
    return (
        char
        for block in blocks
        if block.get('type') == 0  # filter out image blocks
        for line in block["lines"]
        for char in _make_char_dicts_for_line(
            line=line,
            ctm=ctm,
            doctop_base=doctop_base,
            page_number=page_number,
        )
    )
