# write_line_lib.py
'''
Encapsulation of the functions needed to store a new Line into
a Parag and a ParagImgTab object.
'''

import pymupdf  # type: ignore  # noqa: I001


import logging

from pdf_structr.write.classes import Line, Parag, ParagImgTab
from pdf_structr.write.join_lines import (
    clean_out_useless_md_formatting_marks,
)

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
# Get the ParagImgTab element
###################################


def _new_paragimgtab_elt_needed(
    parag_img_tabs: list[ParagImgTab],
    elt_type: str,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> bool:
    '''
    Checks whether a new ParagImgTab shall be created and returns
    True or False.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param elt_type: str: the type of elt to which this line pertains. 'text'
        or 'embd-text'.

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

    # beginning of the page
    if not parag_img_tabs:

        return True

    # current parag_img_tabs.elt_type would not the same as the elt_type
    # of the previous parag_img_tabs
    if parag_img_tabs[-1].elt_type != elt_type:

        return True

    # current parag_img_tabs.bbox would not the same as the bbox
    # of the previous parag_img_tabs
    if pymupdf.IRect(parag_img_tabs[-1].bbox) != pymupdf.IRect(
        context_dict.get('CLIP')
    ):

        return True

    return False


def _create_and_append_new_paragimgtab_elt(
    parag_img_tabs: list[ParagImgTab],
    nline: tuple[
        pymupdf.Rect,
        list[
            dict[str, float | int | str | tuple[float, float] | pymupdf.Rect],
        ],
    ],
    elt_type: str,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    Creates a new ParagImgTab and prepopulates it.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    nline: tuple[
        pymupdf.Rect,
        list[
            dict[
                str, float | int | str | tuple[float, float] | pymupdf.Rect
            ],
        ],
    ]: the current line as 2-tuples, line Rectangle - corresponding spans'
        as extracted by get_raw_lines().

    :param elt_type: str: the type of elt to which this line pertains. 'text'
        or 'embd-text'.

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
    _parag_elt = Parag(
        bbox=nline[0],  # get the line's rectangle
        parag_type='regular',
        lines=[],
        fs_mode=None,
        bold_prop=None,
        ital_prop=None,
        mono_prop=None,
        flags_mode=None,
        color_mode=None,
        fontname_mode=None,
    )

    _paragimgtab_elt = ParagImgTab(
        bbox=context_dict.get('CLIP'),
        str_itr='',
        prefix='',
        indent_prefix='',
        suffix='',
        lr_suffix=2,
        elt_type=elt_type,
        parags=[_parag_elt],
        spans_count=-1,
        italic_span_count=-1,
        bold_span_count=-1,
        superscript_span_count=-1,
        il_code_span_count=-1,
    )

    parag_img_tabs += [_paragimgtab_elt]


def get_paragimgtab_elt(
    parag_img_tabs: list[ParagImgTab],
    nline: tuple[
        pymupdf.Rect,
        list[
            dict[str, float | int | str | tuple[float, float] | pymupdf.Rect],
        ],
    ],
    elt_type: str,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> list[ParagImgTab]:
    '''
    Gets the last elements of the ParagImgTab or creates a new one if the
    preceeding one is not of the same type as the current one.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    nline: tuple[
        pymupdf.Rect,
        list[
            dict[
                str, float | int | str | tuple[float, float] | pymupdf.Rect
            ],
        ],
    ]: the current line as 2-tuples, line Rectangle - corresponding spans'
        as extracted by get_raw_lines().

    :param elt_type: str: the type of elt to which this line pertains. 'text'
        or 'embd-text'.

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

    # A new paragraph element is needed when there is no
    # ParagImgTab in the list or when the previous
    # ParagImgTab is not the same type as one in which the
    # current line shall be stored in
    if _new_paragimgtab_elt_needed(
        parag_img_tabs=parag_img_tabs,
        elt_type=elt_type,
        context_dict=context_dict,
    ):

        _create_and_append_new_paragimgtab_elt(
            parag_img_tabs=parag_img_tabs,
            nline=nline,
            elt_type=elt_type,
            context_dict=context_dict,
        )

        return parag_img_tabs

    return parag_img_tabs


###################################
# Append the new line to a Parag element
###################################


def _append_new_line_to_last_parag(
    parag_elt: Parag,
    line_elt: Line,
) -> None:
    '''
    Appends the new line to the last Parag element of the list of Parag
    of the current ParagImgTab.

    :param parag_elt: Parag: the last Parag element of the the list of Parag
        of the current ParagImgTab.

    :param line_elt: Line: the current line.
    '''
    parag_elt.lines += [line_elt]
    parag_elt.bbox |= line_elt.bbox

    # clean up useless formating marks
    clean_out_useless_md_formatting_marks(parag_elt)


def _create_new_parag_and_store_new_line(
    parag_img_tab: ParagImgTab,
    line_elt: Line,
) -> None:
    '''
    Create a new Parag, store the new line in the new Parag,
    then append the new Parag to the current ParagImgTab.

    :param parag_img_tab: ParagImgTab: the current ParagImgTab.

    :param line_elt: Line: the current Line element.
    '''

    _parag_elt = Parag(
        bbox=line_elt.bbox,  # get the line's rectangle
        parag_type=line_elt.line_type,
        lines=[line_elt],
        fs_mode=None,
        bold_prop=None,
        ital_prop=None,
        mono_prop=None,
        flags_mode=None,
        color_mode=None,
        fontname_mode=None,
    )

    parag_img_tab.parags += [_parag_elt]


def add_line_to_last_or_new_parag(
    parag_img_tab: ParagImgTab,
    parag_elt: Parag,
    line_elt: Line,
    need_new_parag: bool,
) -> None:
    '''
    Appends the new line either to the last Parag in the parag_img_tab
    or to a new Parag of the parag_img_tab, depending on the value of
    the need_new_parag boolean.

    :param parag_img_tab: ParagImgTab: the current ParagImgTab.

    :param parag_elt: Parag: the current last Parag of the list of
        Parag elements of parag_img_tab.

    :param line_elt: Line: the current Line element.

    :param need_new_parag: bool: a boolean indicating whether the comparison
        of the current Line with the last Line element of the last Parag
        element has determined that a new Parag is needed or not.

    '''

    # If we do not need a new paragraph
    if not need_new_parag:

        _append_new_line_to_last_parag(
            parag_elt=parag_elt,
            line_elt=line_elt,
        )
        return

    # Else we need a new paragraph
    _create_new_parag_and_store_new_line(
        parag_img_tab=parag_img_tab,
        line_elt=line_elt,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
