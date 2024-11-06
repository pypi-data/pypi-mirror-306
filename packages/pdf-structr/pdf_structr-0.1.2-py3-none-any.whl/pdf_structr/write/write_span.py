# write_span.py
'''
Encapsulating the functions that write and format individual spans.
'''

import logging

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.classes import Line
from pdf_structr.write.write_links import resolve_links

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
# Spans in non all-monospaced line
###################################


def _build_text_content(
    links: list[dict[str, int | str | pymupdf.Rect]] | None,
    current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ],
) -> str:
    '''
    Build the text content of the span.

    :returns: the span's string, eventually as modified to include a link.

    :param links: list[dict[str, int | str | pymupdf.Rect]]: a list of
        the links dict in the page.

    :param current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ]: the current span in the list.

    :param prefix: str: the bold and/or italics prefix, if the span's text
        has been identified bold or italics.

    :param suffix: str: the bold and/or italics suffix, if the span's text
        has been identified bold or italics.
    '''
    _link_text: str | None = resolve_links(links, current_span)

    return (
        _link_text
        if _link_text
        else current_span['text'].strip()  # type: ignore
    )


def _format_non_mono_fnt_span_in_non_monot_line(
    line_o: Line,
    md_prefix_suffix_tuple: tuple[str, str, str, str],
    span_is_superscript: bool,
    current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ],
    current_idx: int,
    spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> tuple[tuple[str, str, str, str, str, str, str], int]:
    '''
    Format a span that uses a non-monosized font in a non-monotonic line.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param md_prefix_suffix_tuple: tuple[str, str, str, str]: a 4-tuple
        of prefixes and suffixes for superscript and inline code (inline
        code inside superscript marks).

    :param span_is_superscript: bool: a boolean indicating whether this span
        is superscript or not.

    :param current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ]: the current span in the list.

    :param current_idx: int: the current span's index in the list as currently
        ordered.

    :param spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ]: the list of spans in the line.

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

    :param links: list[dict[str, int | str | pymupdf.Rect]]: a list of
        the links dict in the page.
    '''
    # Build the text content, depending on whether its overlaps with a link
    # ---------------------
    _content_text: str = _build_text_content(
        links=links,
        current_span=current_span,
    )

    # Check the flags and build the prefixes for italics and bold
    # ---------------------
    _bold: int = current_span["flags"] & 16  # type: ignore
    _italic: int = current_span["flags"] & 2  # type: ignore

    _prefix: str = ''
    _suffix: str = ''

    if _italic:
        line_o.italic_span_count += 1  # type: ignore
        _prefix = '_'
        _suffix = '_'

    if _bold:
        line_o.bold_span_count += 1  # type: ignore
        _prefix = '**' + _prefix
        _suffix = _suffix + '**'

    # Add a trailing space if necessary
    # ---------------------------
    _ws: int = _add_trailing_space(
        line_o=line_o,
        content_text=_content_text,
        span_is_superscript=span_is_superscript,
        current_idx=current_idx,
        spans=spans,
        context_dict=context_dict,
    )

    return (
        (
            _prefix,  # the italic and bold prefix
            *md_prefix_suffix_tuple[:2],  # the inline and supscript prefixes
            _content_text,
            *md_prefix_suffix_tuple[2:4],  # the inline and supscript suffixes
            _suffix,  # the italic and bold suffix
        ),
        _ws,
    )


def format_span_in_non_all_mono_line_wrapper(
    line_o: Line,
    current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ],
    current_idx: int,
    spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ],
    IGNORE_CODE: bool,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> tuple[tuple[str, str, str, str, str, str, str], int]:
    '''
    Formats the text of a span belonging to a non-monotonic line (the
    span itself may be using a monospaced font, but all the spans are
    not either all mono, or a header or whatever else where all the
    spans are formatted in the same way).

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ]: the current span in the list.

    :param current_idx: int: the current span's index in the list as
        currently ordered.

    :param spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ]: the list of spans in the line.

    :param IGNORE_CODE: bool: the user wants monosized fonts to be treated
        as regular text.

    :param context_dict: dict[str, pymupdf.Rect | None | int | bool | str]:
        the context dict containing:
        - prev_lrect: pymupdf.Rect | None: the Rectangle of the previous
            line. Usefull to compute y_gap between lines.
        - prev_bno: int: block number of the previous line.
        - code: bool: flag to memorize whether the line is in an all
            monospaced font block or not.
        - prev_hdr_string: str | None: header string of the previous line.
        - 'NLINES_COUNT': int: the number of lines in the current clip.
        - 'idx': int: the index number of the current line.
        - 'CLIP': Rect: the rectangle of the current clip.
        - 'spans_count_in_line': int: the spans' count for the current
            line.

    :param links: list[pymupdf.Link] | None = None: a list of links for
        the current page.

    Returns: the concatenated text of the span, with eventual prefixes
    and suffixes.
    '''
    _md_prefix_suffix_tuple: tuple

    # 1. this span uses a monosized font and IGNORE_CODE is False (user
    # wants mono treated as code)
    # ---------------------------
    if (current_span["flags"] & 8) and (IGNORE_CODE is False):  # type: ignore
        line_o.il_code_span_count += 1  # type: ignore
        _md_prefix_suffix_tuple = ('`', '`')
    else:
        _md_prefix_suffix_tuple = ('', '')

    # 2. this span is superscript -- append square brackets
    # ---------------------------
    # NOTE: see `get_md_string_for_page()` in module `write_page`
    # for the cleaning required by the insertion of a traling white space
    # in some cases

    _span_is_superscript: bool = False
    if current_span["flags"] & 1 == 1:  # type: ignore
        _span_is_superscript = True
        line_o.superscript_span_count += 1  # type: ignore
        _md_prefix_suffix_tuple = ('[', *_md_prefix_suffix_tuple, ']')
    else:
        _md_prefix_suffix_tuple = ('', *_md_prefix_suffix_tuple, '')

    # 3. this span is not monosized font and not superscript
    # ---------------------------

    formatted_span: tuple[tuple[str, str, str, str, str, str, str], int] = (
        _format_non_mono_fnt_span_in_non_monot_line(
            line_o=line_o,
            md_prefix_suffix_tuple=_md_prefix_suffix_tuple,
            span_is_superscript=_span_is_superscript,
            current_span=current_span,
            current_idx=current_idx,
            links=links,
            spans=spans,
            context_dict=context_dict,  # type: ignore
        )
    )

    return formatted_span


#####################
# Trailing space stack
#####################


def _next_span_is_superscript(
    line_o: Line,
    current_idx: int,
    spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> bool:
    '''
    Checks whether the next span is superscript and if so, deletes the
    whitespace at the end of the current span and at the beginning of
    the next span.

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param current_idx: int: the current span's index in the list as currently
        ordered.

    :param spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ]: the list of spans in the line.

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
    # Do not check the next span in line if this span is the last span in
    # line...
    if current_idx == line_o.spans_count:
        return False

    # Check if the next span is superscript
    if spans[current_idx + 1]["flags"] & 1 == 1:  # type: ignore

        return True

    return False


def _add_trailing_space(
    line_o: Line,
    content_text: str,
    span_is_superscript: bool,
    current_idx: int,
    spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> int:
    '''
    Checks cases where a whitespace shall be added to the end of the span:
    - no whitespace if this span is not superscript and next span is
      superscript
    - no whitespace if this span is not superscript and ends with a dash

    :param line_o: Line: a Line instance, containing an iterable of
        strings corresponding to a line in the pdf.

    :param content_text: str: the span's text, eventually with an embedded
        link.

    :param md_prefix_suffix_tuple: tuple[str, str, str, str]: a 4-tuple
        of prefixes and suffixes for superscript and inline code (inline
        code inside superscript marks).

    :param current_span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ]: the current span in the list.

    :param current_idx: int: the current span's index in the list as currently
        ordered.

    :param spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ]: the list of spans in the line.

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
    # Do not add a whitespace if the next span is superscript
    if (not span_is_superscript) and _next_span_is_superscript(
        line_o=line_o,
        current_idx=current_idx,
        spans=spans,
        context_dict=context_dict,
    ):
        return 0

    # Do not add a whitespace if the current span is the last of the line
    # and ends with a dash
    if (
        (not span_is_superscript)
        and (current_idx == line_o.spans_count)
        and (content_text.rstrip().endswith('-'))
    ):
        return 0

    return 1


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
