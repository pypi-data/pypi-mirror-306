# write_table.py
'''
Storing the write table functions.
'''
import functools
from typing import Callable

import pymupdf  # type: ignore

from pdf_structr.write.line_img_tab import ParagImgTab


def _output_table(
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    i: int,
) -> ParagImgTab:
    '''
    Outputs a 2-tuple of strings corresponding to a single table selected
    by index ('i') and converted to_markdown together with the preceeding
    and following "\n\n".

    Deletes the output rectangle from the dictionary of rectangles
    to progressively reduce its size.

    :param tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ]: a tuple containing the various table elements extracted from
        the page by extract_tables:
        - a list of tables bboxes, cols and rows
        - a numbered dict of tables md strings, ordered by y1 and x0
        - a numbered dict of tables rectangles, ordered by y1 and x0

    :param i: int: the index number of the table in the table finder.
    '''

    # Output the table as an md string
    _table_md_string: str = tables_tuple[1][i]

    # Store it in a ParagImgTab
    _table_elt: ParagImgTab = ParagImgTab(
        bbox=pymupdf.Rect(
            x0=tables_tuple[2][i].x0,
            y0=tables_tuple[2][i].y0,
            x1=tables_tuple[2][i].x1,
            y1=tables_tuple[2][i].y1,
        ),
        str_itr=_table_md_string,
        prefix='\n',
        indent_prefix='',
        suffix='',
        lr_suffix=0,
        elt_type='table',
        parags=[],
        spans_count=-1,
        italic_span_count=-1,
        bold_span_count=-1,
        superscript_span_count=-1,
        il_code_span_count=-1,
    )

    # Delete the current table from the dict of tables rectangles
    # so that on the next iteration of the list of lines,
    # we don't consider this dict as needing to be printed
    # and we don't have to include in the list of sorted dict this dict
    del tables_tuple[2][i]

    # Also delete the current table from the dict of tables md-string
    # to free some memory
    del tables_tuple[1][i]

    return _table_elt


def output_tables(
    parag_img_tabs: list[ParagImgTab],
    tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ],
    tab_list: list[tuple[int, pymupdf.Rect]],
) -> None:
    '''
    Receives a list of table Rectangles identified as needing to be
    output and added to parag_img_tabs and adds them to it.

    :param parag_img_tabs: list[ParagImgTab]: a list of ParagImgTab
        instances, each containing an iterable of strings corresponding to
        a line or an md-string formatted elements such as a table or the
        string associated with an image or vector graphic.

    :param tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
    ]: a tuple containing the various table elements extracted from
        the page by extract_tables:
        - a list of tables bboxes, cols and rows
        - a numbered dict of tables md strings, ordered by y1 and x0
        - a numbered dict of tables rectangles, ordered by y1 and x0

    :param tab_list: list[tuple[int, pymupdf.Rect]]: the list of relevant
        table Rectangles to be ouput and added to parag_img_tabs.

    '''
    # Make a partial to reduce number of params passed through
    _output_table_partial: Callable = functools.partial(
        _output_table,
        tables_tuple=tables_tuple,
    )

    # Now process the filtered tables and extend the parag_img_tabs
    # with any collected table
    parag_img_tabs.extend([_output_table_partial(i=i) for i, _ in tab_list])
