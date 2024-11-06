# write_line.py
'''
Stores the functions that write a single line of text.
'''
from typing import Callable

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.classes import Line, Parag, ParagImgTab
from pdf_structr.write.join_lines import (
    is_new_parag_needed,
)
from pdf_structr.write.write_line_allmono import (
    write_monosized_line,
)
from pdf_structr.write.write_line_lib import (
    add_line_to_last_or_new_parag,
    get_paragimgtab_elt,
)
from pdf_structr.write.write_line_nonmono import (
    write_non_monosized_line,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


###################################
# Get variables to process the line
###################################


def _get_line_processing_vars(
    parag_img_tabs: list[ParagImgTab],
    elt_type: str,
    nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str, float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
) -> tuple[
    bool,
    ParagImgTab,
    Parag,
    Line,
]:
    '''
    Get the variable necessary to process the line:
    - whether the line is all monosized
    - the last or a new ParagImgTab instance
    - the last Parag instance in the list of Parag of the ParagImgTab
    - a Line instance to store the line

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param elt_type: str: the type of elt to which this line pertains. 'text'
        or 'embd-text'.

    :param nlines: list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ]: the list of lines as 2-tuples, line Rectangle - corresponding spans'
        list sorted by x0, as extracted by get_raw_lines() for
        the current text or image Rect.

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

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.
    '''

    # ------------------------------------------------
    # Get some variables for easier access
    # ------------------------------------------------

    _nline = nlines[context_dict.get('idx')]  # type: ignore
    # has the user requested that mono be handled as code and
    # is the whole line mono-spaced?
    _is_all_monosized_ft_line: bool = not PARAM['IGNORE_CODE'] and all(
        _span["flags"] & 8 for _span in _nline[1]  # type: ignore
    )

    # ------------------------------------------------
    # Get or update the last ParagImgTab instance or create a new one,
    # as the case may be
    # ------------------------------------------------

    _paragimgtab_elt: ParagImgTab = get_paragimgtab_elt(
        parag_img_tabs=parag_img_tabs,
        nline=_nline,
        elt_type=elt_type,
        context_dict=context_dict,
    )[-1]

    # ------------------------------------------------
    # Get the last Parag element stored in the ParagImgTab
    # ------------------------------------------------

    _parag_elt: Parag = _paragimgtab_elt.parags[-1]

    # ------------------------------------------------
    # Create a Line instance
    # ------------------------------------------------

    _line_elt: Line = Line(
        bbox=_nline[0],  # get the line's rectangle
        str_itr='',
        prefix='',
        indent_prefix='',
        suffix='',
        lr_suffix=0,
        line_type='regular',
        raw_line_no=_nline[1][0]['raw_line_no'],  # type: ignore
        block=_nline[1][0]['block'],  # type: ignore
        spans=_nline[1],
        spans_count=(len(_nline[1]) - 1),
        italic_span_count=-1,
        bold_span_count=-1,
        superscript_span_count=-1,
        il_code_span_count=len(_nline[1]),
    )

    return (
        _is_all_monosized_ft_line,
        _paragimgtab_elt,
        _parag_elt,
        _line_elt,
    )


###################################
# Core line processor
###################################


def _write_text_line_core(
    line_o: Line,
    is_monosized_ft_line: bool,
    nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str, float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    get_header_id: Callable,
    PARAM: dict[str, str | int | bool | None],
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> str:
    '''
    Function that will call the relevant line processing functions,
    depending on whether this line is all mono or not.

    :returns: a string representing the header string of the current line.

    :param line_o: Line: the Line's instance to be populated in this
        function and its subfunctions, corresponding to a line to be
        formatted as an md-string.

    :param is_monosized_ft_line: bool: a boolean indicating whether
        the current line is all mono.

    :param nlines: list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ]: the list of lines as 2-tuples, line Rectangle - corresponding spans'
        list sorted by x0, as extracted by get_raw_lines() for
        the current text or image Rect.

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

    :param get_header_id: Callable: a callable that permits identifying
        header and returns a string to format the md headers.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None: a
        list of the outer links in the current page.
    '''

    # ------------------------------------------------
    # All-mono line handling
    # ------------------------------------------------

    if is_monosized_ft_line:

        return write_monosized_line(
            line_o=line_o,
            context_dict=context_dict,
        )

    # ------------------------------------------------
    # Not-all-mono line handling
    # ------------------------------------------------

    return write_non_monosized_line(
        line_o=line_o,
        nlines=nlines,
        context_dict=context_dict,
        PARAM=PARAM,
        get_header_id=get_header_id,
        links=links,
    )


###################################
# Main API to the line processor
###################################


def write_text_line_core(
    page: pymupdf.Page,
    parag_img_tabs: list[ParagImgTab],
    elt_type: str,
    get_header_id: Callable,
    nlines: list[
        tuple[
            pymupdf.Rect,
            list[
                dict[
                    str, float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ],
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    links: list[dict[str, int | str | pymupdf.Rect]] | None = None,
) -> None:
    '''
    Non-decorated function.
    Called from both `write_text_line_and_above` in module
    `write_lines_in_txt_rect` and from `_write_line_in_img`
    in module `write_lines_in_img`.

    Control switch function that converts a passed-in line tuples contained
    in `nlines`, referenced by the 'idx' key in context_dict, into a "code"
    (all-mono) or non-mono iterable of md-strings.

    :return: the header string for the current line (we do not want to update
        the key 'prev_hdr_string' of the context dict now, because we are going
        to need its value in the calling functions.

    :param page: pymupdf.Page: the current page.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param elt_type: str: the type of elt to which this line pertains. 'text'
        or 'embd-text'.

    :param get_header_id: Callable: a callable that permits identifying
        header and returns a string to format the md headers.

    :param nlines: list[
        tuple[
            pymupdf.Rect,  # line rectangle
            list[  # list of spans in the line rectangle
                dict[
                    str,
                    float | int | str | tuple[float, float] | pymupdf.Rect
                ],
            ],
        ],
    ]: the list of lines as 2-tuples, line Rectangle - corresponding spans'
        list sorted by x0, as extracted by get_raw_lines() for
        the current text or image Rect.

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

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text', 'IGNORE_CODE',
        'image_size_limit', 'FONT_SIZE_LIMIT', 'eol_y_thresholds'.

    :param links: list[dict[str, int | str | pymupdf.Rect]] | None = None: a
        list of the outer links in the current page.
    '''
    # ------------------------------------------------
    # Get some variables for easier access
    # ------------------------------------------------

    (
        _is_all_monosized_ft_line,
        _paragimgtab_elt,
        _parag_elt,
        _line_elt,
    ) = _get_line_processing_vars(
        parag_img_tabs=parag_img_tabs,
        elt_type=elt_type,
        nlines=nlines,
        context_dict=context_dict,
        PARAM=PARAM,
    )

    # ------------------------------------------------
    # Write the line into the _line_elt and get the hdr_string
    # ------------------------------------------------

    _hdr_string: str = _write_text_line_core(
        line_o=_line_elt,
        is_monosized_ft_line=_is_all_monosized_ft_line,
        context_dict=context_dict,
        nlines=nlines,
        PARAM=PARAM,
        get_header_id=get_header_id,
        links=links,
    )

    # ------------------------------------------------
    # Eventually add additional line returns to the previous line
    # ------------------------------------------------

    _need_new_parag: bool = is_new_parag_needed(
        page=page,
        current_line=_line_elt,
        parag=_parag_elt,
        context_dict=context_dict,
        PARAM=PARAM,
        is_monosized_ft_line=_is_all_monosized_ft_line,
    )

    # ------------------------------------------------
    # append the Line to the list[Line] of the last _parag_elt
    # or to a new Parag and extend the rectangles of the _parag_elt
    # ------------------------------------------------

    add_line_to_last_or_new_parag(
        parag_img_tab=_paragimgtab_elt,
        parag_elt=_parag_elt,
        line_elt=_line_elt,
        need_new_parag=_need_new_parag,
    )

    # ------------------------------------------------
    # We update the prev_hdr_string here only because we need to
    # know the previous header string in is_new_parag_needed
    # ------------------------------------------------

    context_dict['prev_hdr_string'] = _hdr_string


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
