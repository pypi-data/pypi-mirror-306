# handle_bullets.py
'''
Module encapsulating bulleted list handling functions.
'''


import logging

import pymupdf  # type: ignore

from pdf_structr.write.line_img_tab import Line

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
# Global variables
#####################


bullet = tuple(
    [
        "-",
        "*",
        "‐",
        "⁃",
        "○",
        "o ",
        "●",
        "◦",
        "–",
        "—",
        "‒",
        "•",
        "∙",
        "‣",
        ">",
        '!"',  # font: 'Mozilla_Bullet'
        chr(0xF0A7),
        chr(0xF0B7),
        chr(0xB6),
        chr(0xB7),
        chr(0xBE),
        chr(0xBE) + " ",
        chr(8226),  # 2022 • BULLET (&bull;, &bullet;)
    ]
    + list(map(chr, range(9642, 9680)))
)


###################################
# Starting bullet points
###################################


def _compute_char_width_for_a_span(span: dict) -> float:
    '''
    Compute the average char width for a given span.

    :param span: dict: the span for which the character width shall be
    computed.
    '''
    # compute the span's width
    _span_width: float = span["bbox"][2] - span["bbox"][0]  # type: ignore

    # compute a character's width
    # cwidth
    return _span_width / len(span["text"])  # type: ignore


def _convert_bullet_to_dash(
    line_o: Line,
) -> None:
    '''
    Convert the starting bullet to a dash.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    '''
    _text: str = line_o.spans[0]['text']  # type: ignore

    # Chop off the beginning of the string
    _text = _text[1:]

    # Define a dash to be added at the beginning of the span's text
    _starting_dash: str
    if len(_text) > 1 and _text[1] == " ":
        _starting_dash = "-"
    else:
        _starting_dash = "- "

    # Add the starting dash at the beginning of the span's text
    line_o.spans[0]['text'] = _starting_dash + _text  # type: ignore


def _add_indent(
    line_o: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    Add some indent if necessary.

    NOTE: inspired by pymupdf/RAG code, commit
    e20b9e7011424e2e4bf77ea15ccd5409b4024eeb
    v.0.0.17
    NOTE: we should rather compute the distance from the line's left mode
    or something contextual depending on the preceeding and/or following
    lines instead of the clip

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous line.
          Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all monospaced
          font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'idx': int: the index number of the current line.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).
    '''
    clip: pymupdf.Rect = context_dict['CLIP']

    # Get the current line's spans
    _spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ] = line_o.spans  # type: ignore

    # compute the distance of the span from the left edge of the clip
    _dist: float = _spans[0]["bbox"][0] - clip.x0  # type: ignore

    # compute a character's width for the span
    # cwidth
    _char_width: float = _compute_char_width_for_a_span(_spans[0])

    # append some white spaces depending on the distance of the span
    # from the left edge of the clip
    line_o.indent_prefix = " " * int(round(_dist / _char_width))

    # Original pymupdf/RAG code, commit
    # e20b9e7011424e2e4bf77ea15ccd5409b4024eeb
    # v.0.0.17
    #
    # if text.startswith(bullet):
    #     text = text[1:]
    #     if len(text) > 1 and text[1] == " ":
    #         t = "-"
    #     else:
    #         t = "- "
    #     text = t + text[1:]
    #     dist = span0["bbox"][0] - clip.x0
    #     cwidth = (span0["bbox"][2] - span0["bbox"][0]) / len(
    #         span0["text"]
    #     )
    #     text = " " * int(round(dist / cwidth)) + text


def _convert_starting_bullet(
    line_o: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    Make the string chunk if there is a bullet at the beginning of the line
    by adding a dash, a space after the dash if necessary and some space before
    as the case may require.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous line.
          Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all monospaced
          font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'idx': int: the index number of the current line.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).
    '''
    # 1. Replace the starting bullet by a dash
    # -------------------------------

    _convert_bullet_to_dash(line_o=line_o)

    # 2. Add indent as the case may be
    # -------------------------------

    _add_indent(
        line_o=line_o,
        context_dict=context_dict,
    )


def handle_starting_bullet(
    line_o: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    If the line starts with a bullet, marks the line as bullet, converts
    the bullet to a dash and adds some indent if necessary.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous line.
          Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all monospaced
          font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'idx': int: the index number of the current line.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current line (or
          0 upon initialization).
    '''

    # Add a dash to the first span if the line startswith a bullet
    _text_span0: str = line_o.spans[0]['text']  # type: ignore

    if _text_span0.startswith(bullet) or _text_span0 == 'o':
        _convert_starting_bullet(
            line_o=line_o,
            context_dict=context_dict,
        )
        # mark the line as a bulleted line
        line_o.line_type = 'bulleted'


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
