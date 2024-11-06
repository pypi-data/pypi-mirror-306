# write_line_allmono.py
'''
Encapsulation of handling of all mono lines.
'''


import logging

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.classes import Line

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


###################################
# Monosized line processor
###################################


def _get_code_mode_start_str(
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> str:
    '''
    Returns the code mode start string as the case may be.

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
        - 'spans_count_in_line': int: the spans' count for the current line.

    '''
    if context_dict.get('code') is False:
        return "\n\n```\n"
    return ""


def _build_iter_spans_all_mono_line(
    line_o: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    Builds an iterable of the text of the spans pertaining to a single line
    where all the spans are in monosized font, prepending three backticks if
    the "code" mode is not turned on, turning on the concat mode if it is not
    yet on.

    :param line_o: Line: a Line's instance, corresponding to a line to be
        formatted as an md-string.

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
        - 'spans_count_in_line': int: the spans' count for the current line.

    '''
    # NOTE: BUG when the first item in an all mono-line is a bullet; it is
    # assumed to be part of the "code", when in fact, it shall be handled as
    # a starting bullet point
    _lrect = line_o.bbox
    _spans = line_o.spans

    # ------------------------------------------------
    # Compute the left indent
    # ------------------------------------------------

    # compute approx. distance from left - assuming a width
    # of 0.5*fontsize.
    _delta: int = int(
        (_lrect.x0 - context_dict['CLIP'].x0)  # type: ignore
        / (_spans[0]["size"] * 0.5)  # type: ignore
    )
    _indent: str = " " * _delta

    # ------------------------------------------------
    # Update the ParagImgTab
    # ------------------------------------------------

    # the strings iterable
    line_o.str_itr = [_span['text'] for _span in _spans]  # type: ignore
    # the prefixes: `_code_mode_start_str` and `_indent`
    line_o.indent_prefix = _indent
    line_o.prefix = _get_code_mode_start_str(
        context_dict=context_dict,
    )


def write_monosized_line(
    line_o: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> str:
    '''
    Handling of all text lines which are whole mono-fontsized (prepending
    3-backticks and indents as necessary; switching on code mode), together
    with the table and/or image blocks preceeding them.

    :returns: an empty string to be used as hdr_string.

    :param line_o: Line: a Line's instance, corresponding to a line to be
        formatted as an md-string.

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
    # Update the line_type of the Line instance
    line_o.line_type = 'all-mono'

    # Prepend backticks and indents if necessary and switch
    # on code flag
    _build_iter_spans_all_mono_line(
        line_o=line_o,
        context_dict=context_dict,
    )

    # Update the context dict
    context_dict['prev_bno'] = line_o.block
    context_dict['prev_lrect'] = line_o.bbox
    # Turn code mode to True
    # !!! Do not do it before calling _build_iter_spans_all_mono_line()
    context_dict['code'] = True

    return ''


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
