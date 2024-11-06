# join_lines.py
'''
Module encapsulating the md-lines transition logic, joining them or
making a new line.
'''

import logging

import pymupdf  # type: ignore  # noqa: I001

from pdf_structr.write.classes import Line, Parag

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
# Close code section
#####################


def _close_code_section(
    *,
    line: Line,
    context_dict: dict,
) -> bool:
    '''
    Checks if "code" mode is on and closes it as the case may be by adding
    a triple-tick together with a line returns as suffixes.

    :param line: Line: the line at the end of which we shall close the code
        section.

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
    # If code mode is still on
    if context_dict.get('code') is True:
        line.lr_suffix = 2
        # when concatenating in write_page_md, suffix will be handled
        # before lr_suffix, so if we want to close code properly
        # we need to add a '\n' before the '```'
        line.suffix = '\n```'
        context_dict['code'] = False

        return True

    return False


#####################
# Close text cluster
#####################


def add_lrs_to_last_line_of_txt_cluster(
    last_line: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
) -> None:
    '''
    Adds a line return to the last line of a text rectangle and eventually,
    turns off code mode and append a triple tick as suffix of the last
    line.

    :param last_line: Line: the last line of the ParagImgTab.

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

    :param is_monosized_ft_line: bool: a boolean indicating whether
        the current line is all mono.
    '''
    # If it is an all mono, close the code section
    if context_dict.get('code') is True:
        last_line.suffix = '\n```'
        context_dict['code'] = False

    # Otherwise, just add two line returns (we are at the end of a paragraph).
    last_line.lr_suffix += 1


#####################
# Close code section
#####################


def clean_out_useless_md_formatting_marks(parag_elt: Parag) -> None:
    '''
    Removes useless formatting marks when two consecutive lines
    end and start with the same italic, bold or bold and italic
    md marks.
    '''
    if len(parag_elt.lines) < 2:
        return

    if parag_elt.is_all_mono():
        return

    if (
        (
            (parag_elt.lines[-2].str_itr[-2] == '_')  # type: ignore
            and (parag_elt.lines[-1].str_itr[0] == '_')  # type: ignore
        )
        or (
            (parag_elt.lines[-2].str_itr[-2] == '**')  # type: ignore
            and (parag_elt.lines[-1].str_itr[0] == '**')  # type: ignore
        )
        or (
            (parag_elt.lines[-2].str_itr[-2] == '_**')  # type: ignore
            and (parag_elt.lines[-1].str_itr[0] == '**_')  # type: ignore
        )
    ):
        parag_elt.lines[-2].str_itr[-2] = ''  # type: ignore
        parag_elt.lines[-1].str_itr[0] = ''  # type: ignore


#####################
# Add line returns sections
#####################


def _lines_y_gap_is_above_lines_eol_y_thresholds(
    lrect: pymupdf.Rect,
    prev_lrect: pymupdf.Rect,
    eol_y_thresholds: float,
) -> bool:
    '''
    Tests if the gap between two lines is larger than `_eol_y_thresholds`
    multiplied by the current line's height.

    :param lrect: pymupdf.Rect: the current line's Rectangle.

    :param prev_lrect: pymupdf.Rect: the previous line's Rectangle.

    :param eol_y_thresholds: float: the threshold beyond which the y gap
        between two consecutive lines shall trigger the insertion of
        a line return.
    '''
    if lrect.y1 - prev_lrect.y1 > lrect.height * eol_y_thresholds:

        return True

    return False


def _line_startswith_bullet_or_superscript(
    current_line: Line,
    span0: dict[str, float | int | str | tuple[float, float] | pymupdf.Rect],
) -> bool:
    '''
    Add another line return to the previous line if:
    - the current line starts with a square bracket or a bullet point,
    - the first span in line is superscript (I guess this is a naive way
    to handle footnotes: REFACTO to make detection based on font size,
    position in page, starting pattern and existence of a footnote reference
    elsewhere in the page).

    :param span0: dict[
        str, float | int | str | tuple[float, float]
        | pymupdf.Rect
    ]: first span in line.

    :returns: True if startswith bracket, bullet or superscript.
    '''
    # If the current line is a bulleted line
    if current_line.line_type == 'bulleted':
        return True

    # If the first span in line is superscrit
    if span0["flags"] & 1:  # type: ignore
        return True

    return False


def _lines_same_block_with_large_width_diff(
    currentl_rect: pymupdf.Rect,
    prevl_rect: pymupdf.Rect,
) -> bool:
    '''
    Test if the previous line is much shorter (1/10th) than the current one
    and if so, adds a '\n' to the previous one.

    :param currentl_rect: pymupdf.Rect: the current line's Rectangle.

    :param prevl_rect: pymupdf.Rect: the previous line's Rectangle.

    '''

    # Compute the lines' width
    _width_lrect: float = currentl_rect.x1 - currentl_rect.x0
    _width_prev_lrect: float = prevl_rect.x1 - prevl_rect.x0

    # Compare the lines' width
    return (_width_prev_lrect / _width_lrect) < 0.1


def _add_lrs_if_needed(
    page: pymupdf.Page,
    current_line: Line,
    previous_line: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    is_monosized_ft_line: bool,
) -> bool:
    '''
    Check whether we need to add line returns at the end of the previous line.

    At this stage, we have two types of lines here:
    - the line is all mono: its str_iter attribute is a simple line of
    the text content of each of its spans. md-formatting information
    is contained in the line's prefix and indent prefix. We still need
    to add some suffix information (line returns and eventual code
    closing).
    - the line is not all-mono: its str_iter attribute is a list of string,
    multiple of 8, where each 8-string chunk corresponds to a span:
        - if the line has been determined as being a header, its prefix
        might contain a hdr_line.
        - if not, the prefix is equal to ''.

    At this stage, the current line and the preceeding one do not have any
    line returns. We want to determine whether the preceeding line and the
    current one shall be joined or disjoined. To join lines, nothing needs
    to be done. To disjoin lines, we need to add some line returns as prefix
    to the previous line.

    Cases of disjoining:
    - if this line and the preceeding one are all-mono and the user wants
      mono to be treated as code
    - if this line and the previous one's y gap exceeds a certain thresholds
    - if this line and the previous one do not pertain to the same text block
    - if the first span in this line starts with a square bracket or a bullet
    - if the first span in this line is superscript

    Cases of joining:
    - if this line and the previous one are headers of the same level and their
      y_gap does not exceed a certain thresholds

    This function will add one or two line returns at the end of the
    preceeding line.

    :returns: True if we need to create a new Parag for the current line
    or False if the current line shall simply be added to the current Parag.

    :param page: pymupdf.Page: the current page.

    :param current_line: Line: the Line's instance that has just been populated
        corresponding to a line formatted as an md-string, to be used to
        determine if we need to add it to the previous paragraph or to
        a new paragraph instance.

    :param previous_line: Line: the ultimate line added to the ParagImgTab's
        lines attribute.

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

    :param is_monosized_ft_line: bool: a boolean indicating whether
        the current line is all mono.
    '''
    # if page.number == 4:
    #     pass

    # ------------------------------------------------
    # If the previous line was a monosized line
    # ------------------------------------------------

    if previous_line.line_type == 'all-mono':

        # if this line is monosized also:
        # => previous line not a paragraph
        # => previous line needs a single line return
        # => we need to append this line to the current paragraph
        if is_monosized_ft_line:

            previous_line.lr_suffix = 1

            return False

        # if this line is not monosized
        # => previous line is the end of a paragraph
        # => previous line needs two line returns
        # => previous line needs a suffix '\n```'
        # => we need to create a new paragraph
        else:

            _close_code_section(
                line=previous_line,
                context_dict=context_dict,
            )

            return True

    # ------------------------------------------------
    # Test if the y gap between the lines is above the
    # paragraph's thresholds
    # ------------------------------------------------

    _y_gap_above_thresholds: bool = (
        _lines_y_gap_is_above_lines_eol_y_thresholds(
            lrect=current_line.bbox,
            prev_lrect=previous_line.bbox,
            eol_y_thresholds=PARAM['eol_y_thresholds'],  # type: ignore
        )
    )

    # ------------------------------------------------
    # Large y gap between this line and the previous one:
    # => previous line is a paragraph
    # => previous line needs two line returns
    # => we need to create a new paragraph for the current line
    # ------------------------------------------------

    if _y_gap_above_thresholds:

        previous_line.lr_suffix = 2

        return True

    # ------------------------------------------------
    # This line starts with a bullet or superscript:
    # => previous line is a paragraph
    # => previous line needs two line returns
    # => we need to create a new paragraph for the current line
    # ------------------------------------------------

    if _line_startswith_bullet_or_superscript(
        current_line=current_line,
        span0=current_line.spans[0],  # type: ignore
    ):

        previous_line.lr_suffix = 2

        return True

    # ------------------------------------------------
    # Previous line and this line are of the same type "header wise"
    # (i.e. both are same header level; both are not header)
    # and their y_gap is below the y_gap thresholds
    # (this was checked at previous step):
    # => this line is a chunk of the previous line
    # => previous line is NOT a paragraph: shall have one or no line return
    # => previous line and this line shall be contatenated: shall have no
    # line return: by default, the previous line at this stage does not
    # have any ine return.
    # => this line shall have no header prefix
    # => we need to append the current line to the paragraph
    # NOTE: This is the main lines concatenating instruction
    # ------------------------------------------------

    if context_dict.get('prev_hdr_string') == current_line.prefix:

        current_line.prefix = ''

        return False

    # ------------------------------------------------
    # Previous line is a header (and implicitly, this one is not a
    # header chunk; checked earlier):
    # => previous line is a paragraph
    # => previous line needs two line returns
    # => we need to create a new paragraph for the current line
    # ------------------------------------------------

    if previous_line.line_type == 'header':

        previous_line.lr_suffix = 2

        return True

    # ------------------------------------------------
    # This line is a header (and implicitly, is not a header chunk;
    # checked earlier):
    # => previous line is a paragraph
    # => previous line needs two line returns
    # => we need to create a new paragraph for the current line
    # ------------------------------------------------

    if current_line.line_type == 'header':

        previous_line.lr_suffix = 2

        return True

    # ------------------------------------------------
    # Test if the line pertain to the same block
    # ------------------------------------------------

    _line_in_same_block: bool = current_line.block == previous_line.block

    # ------------------------------------------------
    # Fall back to separate lines that have not been disjoined earlier
    # ------------------------------------------------

    # If the previous line does not already have an '\n'
    if previous_line.lr_suffix == 0:

        # ------------------------------------------------
        # If the lines pertain to two difft blocks
        # => previous line is a paragraph
        # => previous line needs two line returns
        # => we need to create a new paragraph for the current line
        # ------------------------------------------------

        if not _line_in_same_block:

            previous_line.lr_suffix = 2

            return True

        # ------------------------------------------------
        # If the lines have a large width difference
        # => we just need to add a line return
        # => we need to append the current line to the paragraph
        # ------------------------------------------------

        if _lines_same_block_with_large_width_diff(
            currentl_rect=current_line.bbox,
            prevl_rect=previous_line.bbox,
        ):

            previous_line.lr_suffix = 1

            return False

    # ------------------------------------------------
    # In all the other cases, append the line to the current paragraph
    # ------------------------------------------------

    return False


def is_new_parag_needed(
    page: pymupdf.Page,
    parag: Parag,
    current_line: Line,
    context_dict: dict[str, pymupdf.Rect | None | int | bool | str],
    PARAM: dict[str, str | int | bool | None],
    is_monosized_ft_line: bool,
) -> bool:
    '''
    Determines whether a new Parag shall be created to host the current
    Line or if it can be stored in the last Parag of the current ParagImgTab.

    :param page: pymupdf.Page: the current page.

    :param parag: Parag: the last paragraph in the current ParagImgTab.

    :param current_line: Line: the Line's instance that has just been populated
        corresponding to a line formatted as an md-string, to be used to
        determine if we need to add it to the previous paragraph or to
        a new paragraph instance.

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

    :param is_monosized_ft_line: bool: a boolean indicating whether
        the current line is all mono.

    '''
    _need_new_parag: bool = False

    if parag.lines:

        _need_new_parag = _add_lrs_if_needed(
            page=page,
            current_line=current_line,
            previous_line=parag.lines[-1],
            context_dict=context_dict,
            PARAM=PARAM,
            is_monosized_ft_line=is_monosized_ft_line,
        )

    return _need_new_parag


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
