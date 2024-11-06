# table_lib.py
'''
Module providing common functions to both table extractors.
'''


import html
from typing import Any, Generator

import pymupdf  # type: ignore

#####################
# Table header markdown string building
#####################


def _get_header_name(
    header_names: list[str],
    headers_count: int,
    idx: int,
) -> str | None:
    '''
    Get header name if the index is lower than the header's count.

    Return an empty string if the index is higher than the headers' count.
    This may happen in particular when header_names is an empty list.

    :param header_names: list[str]: a list of strings, where each item
        is a column header.

    :param headers_count: int: the number of headers in the table.

    :param idx: int: the index number in the iteration on the headers.

    '''
    if idx < headers_count:
        # theoretically, this may also be an empty string or None
        return header_names[idx]

    return ''


def _extract_or_generate_header_name(
    header_names: list[str],
    headers_count: int,
    clean: bool,
    idx: int,
) -> str:
    '''
    Extracts and cleans the header name or generates a header
    name if _hdr_name is an empty string or is None.

    :param header_names: list[str]: a list of strings, where each item
        is a column header.

    :param headers_count: int: the number of headers in the table.

    :param clean: bool: if clean is true, markdown syntax is removed
        from cell content.

    :param idx: int: the index number in the iteration on the headers.

    '''

    _hdr_name: str | None = _get_header_name(
        header_names=header_names,
        headers_count=headers_count,
        idx=idx,
    )

    # Generate a name if empty
    if _hdr_name is None or _hdr_name == "":
        return f"Col{idx+1}"

    # If not empty, clean the string

    # Remove any line breaks
    _hdr_name = _hdr_name.replace("\n", " ")

    # remove sensitive syntax
    if clean:
        _hdr_name = html.escape(_hdr_name.replace("-", "&#45;"))

    return _hdr_name


def _extract_row_to_markdown(
    table_rows: list[list[str]] | list[Generator[str, Any, Any]],
    table_content: list[str],
    idx: int,
    clean: bool,
):
    '''
    Extracts a row, referenced by its idx number, to markdown.
    '''
    table_content += "|"
    _row: list[str] | Generator[str, Any, Any] = table_rows[idx]

    for cell in _row:
        # output None cells with empty string
        _cell_str: str = "" if cell is None else cell.replace("\n", " ")

        if clean:  # remove sensitive syntax
            _cell_str = html.escape(_cell_str.replace("-", "&#45;"))

        table_content += [_cell_str, "|"]

    table_content += "\n"


def extract_table_to_markdown_generic(
    header_names: list[str],
    header_external_print_first_row: bool,
    table_rows: list[list[str]] | list[Generator[str, Any, Any]],
    col_count: int,
    clean: bool,
) -> str:
    '''
    A more generic version of the `extract_table_to_markdown` function,
    that Output table content as a string in Github-markdown format.

    :param header_names: list[str]: a list of strings, where each item
        is a column header.

    :param header_external: bool: a boolean indicating whether the header
        line is external or part of the table content.
        If set to True, the FIRST line of the table will be used as FIRST
        line of the table.
        If set to False, the FIRST line of the table will be skipped.
        Implicitly, this mean that a list shall be provided as argument
        to parameter `header_names`.

        Accordingly, if a header_names list is provided and this
        header_names list has been extracted from the first line
        of the table, this shall be set to False so that the first
        line be skipped when rendering the table.

        If no header line has been provided, this shall in principle
        never be set to False.

        NOTE: This parameter shall be renamed to something more explicit,
        such as skip_first_row_if_header_provided.
        It could also be deleted all together and be set internally
        based on whether a header has been provided or not.

    :param table_rows: list[list[str]] | list[Generator[str, Any, Any]]: the
        table rows as a list of list of string or a list of generators of
        strings.

    :param col_count: int: the number of columns in the table.

    :param clean: bool:  If clean is true, markdown syntax is removed
        from cell content.

    '''
    # generate header string
    header_names = list(header_names)
    _headers_count: int = len(header_names)

    _hdr_string: str = (
        "|"  # opening "|"
        + "|".join(  # this one comes only after the name
            _extract_or_generate_header_name(
                header_names,
                _headers_count,
                clean,
                _i,
            )
            for _i in range(col_count)
        )
        + "|\n"
    )

    # output the MD underline
    _md_underlines: str = (
        "|" + "|".join("---" for i in range(col_count)) + "|\n"
    )

    # skip first row in details if header is part of the table
    j = 0 if header_external_print_first_row else 1

    # iterate over table content rows
    _table_content: list[str] = []
    for _idx in range(j, len(table_rows)):
        _extract_row_to_markdown(
            table_rows=table_rows,
            table_content=_table_content,
            idx=_idx,
            clean=clean,
        )

    return ''.join([_hdr_string, _md_underlines, *_table_content, "\n"])


#####################
# Make table stores functions
#####################


def create_table_info_dict(
    table_rect,
    row_count,
    col_count,
) -> dict:
    '''
    Creates a table information dict to be returned when detailled
    info are requested.
    '''

    # Create and return a dict per table
    return {
        # get the tables bbox from tab_rects dict to have both the full
        # table bbox (header and content)
        # the bbox: Rect
        "bbox": tuple(table_rect),  # type: ignore
        # the rows count: int
        "rows": row_count,
        # the columns count: int
        "columns": col_count,
    }


def fill_in_table_dicts(
    tab_rects: dict[int, pymupdf.Rect],
    tab_md_strs: dict[int, str],
    table_rect: pymupdf.Rect,
    table_md_str: str,
    row_count: int,
    col_count: int,
    idx: int,
) -> dict[str, tuple[float, float, float, float] | int]:
    '''
    For a given table, fill in numbered dict of table rectangle
    with the smallest common Rectangle (union) of the table and
    its header.

    :returns: another new dict containing the following info about
    the table:

    - the union Rectangle
    - the row_count
    - the col_count

    :param tab_rects: dict[int, pymupdf.Rect]: a numbered dict of table
        rectangles.

    :param tab_md_strs: dict[int, str]: a numbered dict of table md
        strings.

    :param table_rect: pymupdf.Rect: the current table Rectangle.

    :param table_md_str: str: the current table md string.

    :param row_count: int: the row count in the current table.

    :param col_count: int: the col count in the current table.

    :param i: int: the index number of the table in the table finder.
    '''
    # Fill in the numbered dict of table rectangles including the
    # header bbox (which may exist outside tab.bbox)
    tab_rects[idx] = table_rect

    # Fill in the numbered dict of table md string
    tab_md_strs[idx] = table_md_str

    # Create and return a dict per table
    return create_table_info_dict(
        table_rect=table_rect,
        row_count=row_count,
        col_count=col_count,
    )
