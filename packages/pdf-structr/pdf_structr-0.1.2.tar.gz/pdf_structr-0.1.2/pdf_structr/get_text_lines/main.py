# main.py
"""
Refactoring of pymupdf4llm get_text_lines module.


Dependencies
-------------
PyMuPDF v1.24.2 or later

License
----------------------
License GNU Affero GPL 3.0


Additional comments refactoring:
---------------------
This is the main module of the package.
It depends on (by order of apparition):
- make_spans_list (where superscript spans are handled)
- make_raw_lines (which depends on sanitize_spans)
"""


# import sys
from pymupdf import IRect, Rect, TextPage  # type: ignore

from pdf_structr.get_text_lines.make_raw_lines import make_raw_lines
from pdf_structr.get_text_lines.make_spans_list import (
    make_spans_list,
)

###############################
# Main API
###############################


def get_raw_lines_core(
    clip: Rect,
    blocks: list[dict],
    y_delta: float,
    *args,
    **kwargs,
) -> list[
    # one tuple per line
    tuple[
        # the line's rectangle
        Rect,
        # the line's spans
        list[
            # span
            dict[
                str,
                # flags and color
                int
                # size (fontsize), ascender and descender
                | float
                # font (fontname) and text
                | str
                # origin
                | tuple[float, float]
                # bbox
                | Rect,
            ]
        ],
    ]
]:
    """
    Extract the text spans living inside a given Rectangle (the clip) and
    groups them into so-called raw lines.

    This is the core version of the get_raw_lines() below for faster use
    in custrag.

    All spans roughly on the same line are joined to generate an improved line.
    This copes with MuPDF's algorithm that generates new lines also for spans
    whose horizontal distance is larger than some threshold.

    Result is a sorted list of line objects that consist of the recomputed line
    boundary box and the sorted list of spans in that line.

    This result can then easily be converted e.g. to plain or markdown text.

    :param clip: (Rect) specifies a sub-rectangle of the textpage rect (which
             in turn may be based on a sub-rectangle of the full page).

    :param blocks: list[dict]: the text blocks previously extracted via
            textpage.extractDICT (in the multi_column package, for
            instance).

    :param y_delta: float: put spans on the same line if their top or bottom
            coordinate differ by no more than this value.

    :returns: a sorted list of items (rect, [spans]), each representing
        one line. The spans are sorted left to right, the span dictionaries
        have been changed:
        - "bbox" has been converted to a Rect object
        - "line" (new) the line number in TextPage.extractDICT
        - "block" (new) the block number in TextPage.extractDICT
        This allows to detect where MuPDF has generated line breaks to indicate
        large inter-span distances.
    """
    # Get all the spans of the textpage as a list
    _spans: list[
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ] = make_spans_list(
        blocks=blocks,
        clip=clip,
    )

    if not _spans:  # no text at all
        return []

    # sort spans by bottom coord
    _spans.sort(key=lambda _span: _span["bbox"].y1)  # type: ignore

    # make the list of "raw" lines and return it
    return make_raw_lines(spans=_spans, y_delta=y_delta)


def get_raw_lines(
    textpage: TextPage,
    clip: Rect | IRect | None = None,
    y_delta: float = 3,
    blocks: list[dict] | None = None,
) -> list[
    # one tuple per line
    tuple[
        # the line's rectangle
        Rect,
        # the line's spans
        list[
            # span
            dict[
                str,
                # flags and color
                int
                # size (fontsize), ascender and descender
                | float
                # font (fontname) and text
                | str
                # origin
                | tuple[float, float]
                # bbox
                | Rect,
            ]
        ],
    ]
]:
    """
    Extract the text spans from a TextPage in natural reading sequence.

    All spans roughly on the same line are joined to generate an improved line.
    This copes with MuPDF's algorithm that generates new lines also for spans
    whose horizontal distance is larger than some threshold.

    Result is a sorted list of line objects that consist of the recomputed line
    boundary box and the sorted list of spans in that line.

    This result can then easily be converted e.g. to plain or markdown text.

    :param textpage: (mandatory) TextPage object

    :param clip: (Rect) specifies a sub-rectangle of the textpage rect (which
             in turn may be based on a sub-rectangle of the full page).

    :param y_delta: (float) put spans on the same line if their top or bottom
            coordinate differ by no more than this value.

    :param blocks: (list[dict]) the text blocks extracted via
            textpage.extractDICT previously (in the multi_column package, for
            instance).

    :returns: a sorted list of items (rect, [spans]), each representing
        one line. The spans are sorted left to right, the span dictionaries
        have been changed:
        - "bbox" has been converted to a Rect object
        - "line" (new) the line number in TextPage.extractDICT
        - "block" (new) the block number in TextPage.extractDICT
        This allows to detect where MuPDF has generated line breaks to indicate
        large inter-span distances.
    """
    if blocks is None:
        # Extract the img and text blocks
        _blocks: list[dict] = textpage.extractDICT(sort=True)["blocks"]
    else:
        _blocks = blocks

    # check if a clip has been provided and if not, use TextPage rect
    if clip is None:
        clip = textpage.rect

    return get_raw_lines_core(clip, _blocks, y_delta)


# def get_text_lines(
#     page,
#     *,
#     textpage=None,
#     clip=None,
#     sep="\t",
#     y_delta=3,
#     ocr=False,
# ) -> str:
#     """Extract text by line keeping natural reading sequence.

#     Notes:
#         Internally uses "dict" to select lines and their spans.
#         Returns plain text. If originally separate MuPDF lines in fact have
#         (approximatly) the same baseline, they are joined into one line using
#         the 'sep' character(s).
#         This method can be used to extract text in reading sequence - even in
#         cases of text replaced by way of redaction annotations.

#     Args:
#         page: (pymupdf.Page)
#         textpage: (TextPage) if None a temporary one is created.
#         clip: (rect-like) only consider spans inside this area
#         sep: (str) use this string when joining multiple MuPDF lines.
#     Returns:
#         String of plain text in reading sequence.
#     """
#     textflags = pymupdf.TEXT_MEDIABOX_CLIP
#     page.remove_rotation()
#     prect = page.rect if not clip else pymupdf.Rect(clip)  # area to consider

#     # xsep: str = sep if sep == "|" else ""

#     # make a TextPage if required
#     if textpage is None:
#         if ocr is False:
#             tp = page.get_textpage(clip=prect, flags=textflags)
#         else:
#             tp = page.get_textpage_ocr(dpi=300, full=True)
#     else:
#         tp = textpage

#     lines = get_raw_lines(tp, clip=prect, y_delta=y_delta)

#     if not textpage:  # delete temp TextPage
#         tp = None

#     if not lines:
#         return ""

#     # Compose final text
#     alltext: str = ""

#     if not ocr:
#         prev_bno = -1  # number of previous text block
#         for lrect, line in lines:  # iterate through lines
#             # insert extra line break if a different block
#             bno = line[0]["block"]  # block number of this line
#             if bno != prev_bno:
#                 alltext += "\n"
#             prev_bno = bno

#             line_no = line[0]["line"]  # store the line number of prev span
#             for s in line:  # walk over the spans in the line
#                 lno = s["line"]
#                 stext = s["text"]
#                 if line_no == lno:
#                     alltext += stext
#                 else:
#                     alltext += sep + stext
#                 line_no = lno
#             alltext += "\n"  # append line break after a line
#         alltext += "\n"  # append line break at end of block
#         return alltext

#     """
#     For OCR output, we try a rudimentary table recognition.
#     """
#     rows: list = []
#     xvalues: list = []
#     row: str | list[str]

#     # walk the lines
#     for lrect, line in lines:
#         # if only 1 span in line and no columns identified yet...
#         if len(line) == 1 and not xvalues:
#             alltext += line[0]["text"] + "\n\n\n"
#             continue
#         # multiple spans in line and no columns identified yet
#         elif not xvalues:  # define column borders
#             xvalues = [s["bbox"].x0 for s in line] + [line[-1]["bbox"].x1]
#             col_count = len(line)  # number of columns
#         row = [""] * col_count
#         for r, l in line:
#             for i in range(len(xvalues) - 1):
#                 x0, x1 = xvalues[i], xvalues[i + 1]
#                 if abs(r.x0 - x0) <= 3 or abs(r.x1 - x1) <= 3:
#                     row[i] = l
#         rows.append(row)

#     if rows:
#         row = "|" + "|".join(rows[0]) + "|\n"
#         alltext += row
#         alltext += "|---" * len(rows[0]) + "|\n"
#         for row in rows[1:]:
#             alltext += "|" + "|".join(row) + "|\n"
#         alltext += "\n"

#     return alltext


# if __name__ == "__main__":
#     import pathlib

#     filename = sys.argv[1]
#     doc = pymupdf.open(filename)
#     text = ""
#     for page in doc:
#         text += get_text_lines(page, sep=" ") + "\n" + chr(12) + "\n"
#     pathlib.Path(f"{doc.name}.txt").write_bytes(text.encode())
