# tab_extract.py
'''
Module encapsulating the table extraction features for
the simple table detector.

In this context, table extraction is the step that comes
after building tables and consists in converting the tables
to a list of list of list of strings.
'''

import logging
from typing import Any, Generator

# from statistics import geometric_mean, harmonic_mean
import pymupdf  # type: ignore

from pdf_structr.tables.table_lib import (
    extract_table_to_markdown_generic,
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


#####################
# Simple table extractor: table extractor for a list of block_cluster
#####################


def _simple_extract_row_to_list_of_str(lines: list[dict]) -> list[str]:
    '''
    For each line, join the spans' text (in principle, only one span
    per line) into a space separated-string and return the lines' text
    as a list of strings.

    :param lines: list[dict]: a list of lines in a block.
    '''

    return [
        ' '.join(_span['text'].strip() for _span in _line['spans'])
        for _line in lines
    ]


def _simple_extract_table(
    block_cluster: list[dict[str, int | float | tuple | list]]
) -> list[list[str]]:
    '''
    At this stage, a block is a row in the table and each of its lines
    shall be a cell.

    :returns: a list of list of strings, which shall represent a table.

    :param block_cluster: list[dict[str, int | float | tuple | list]]:
        one of the blocks' pertaining to one of the clusters previously
        built by `make_rlb_clusters`.

    '''
    return [
        _simple_extract_row_to_list_of_str(_block['lines'])  # type: ignore
        for _block in block_cluster
    ]


def simple_extract_tables(
    block_clusters: list[list[dict[str, int | float | tuple | list]]]
) -> list[list[list[str]]]:
    '''
    Extract a list of list of list of string from a list of
    `block_clusters` build by stabs. A `block_clusters` is
    a group of text blocks identified as likely to contain a
    table.


    :param block_clusters: list[list[dict[str, int | float | tuple | list]]]:
        the list of blocks' clusters previously built by `make_rlb_clusters`.
    '''
    return [_simple_extract_table(_cluster) for _cluster in block_clusters]


#####################
# Table extractor for table dict
#####################


def _extract_cell(
    cell: dict[str, tuple[float, float, float, float] | list[dict]]
) -> str:
    '''
    Extract the text of the spans contained in a cell. A cell is a dict
    containing a bbox and a list of spans.

    :returns: a string which shall represent a cell in a table.
    '''
    return ' '.join(
        _span['text'].strip() for _span in cell['spans']  # type: ignore
    )


def _extract_row(
    cells: list[dict[str, tuple[float, float, float, float] | list[dict]]]
) -> list[str]:
    '''
    Extract the text of the spans contained in the cells of a given row.

    :returns: a list of strings, which shall represent a row in a table.

    :param cells: list[
        dict[str, tuple[float, float, float, float] | list[dict]]
    ]: the cells from a given row.

    '''
    return [_extract_cell(cell) for cell in cells]


def _extract_rows(
    rows: list[dict[str, tuple[float, float, float, float] | list[dict]]]
) -> list[list[str]]:
    '''
    Extract the rows in the table to a list of list of strings.

    :returns: a list of list of strings, which shall represent a table.

    :param rows: list[
        dict[str, tuple[float, float, float, float] | list[dict]]
    ]: a list of rows dict, where each dict has a key 'bbox' which contains
       the rows bbox as 4-float tuple and a key 'cells' containing a list
       of cells.

    '''
    return [_extract_row(_row['cells']) for _row in rows]  # type: ignore


def extract_table(
    table: dict[
        str,
        pymupdf.Rect
        | float
        | list[dict]
        | list[tuple[float, float, float, float]],
    ]
) -> list[list[str]]:
    '''
    Given a table, returns a list of list of strings, where the outer list
    represents the table and each inner sublists is a row in the table,
    composed of the cells' strings.
    '''
    return _extract_rows(table['rows'])  # type: ignore


#####################
# Make header names
#####################


def _is_first_row_header(
    first_row: dict[str, Any],
    second_row: dict[str, Any],
) -> bool:
    '''
    Uses several criteria to qualify the first row of a table as header.

    :param first_row: dict[str, Any]: the first row of a table. It shall
        have be enriched in properties by `_compute_tables_rows_properties`,
        so that it has the following keys:

        - bold_prop
        - color
        - fs_mode
        - italic_prop

    :param second_row: dict[str, Any]: the second row of a table. It shall
        have be enriched in properties by `_compute_tables_rows_properties`,
        so that it has the following keys:

        - bold_prop
        - color
        - fs_mode
        - italic_prop

    '''
    _italic_bold_prop_diff: float = 0.6

    # If the first row is bolder than the second one
    if (
        first_row['bold_prop'] - second_row['bold_prop']
    ) > _italic_bold_prop_diff:
        return True

    # If there is a difference in color between the two rows
    if first_row['color'][0] != second_row['color'][0]:
        # one of the them is the header
        return True

    # If there is a difference in font size between the two rows
    if first_row['fs_mode'][0] != second_row['fs_mode'][0]:
        # one of the them is the header
        return True

    # If the difference in italics proportion between the two rows is above
    # _italic_bold_prop_diff (one of them is more italic than the other)
    if (
        abs(first_row['italic_prop'] - second_row['italic_prop'])
        > _italic_bold_prop_diff
    ):
        # one of the them is the header
        return True

    # All other cases, return False
    return False


def make_header_names(
    table: dict[  # type: ignore
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple, tuple, tuple, tuple],  # list of cols bbox
    ],
) -> list[str]:
    '''
    If it detects a header row, make a list of header names
    as a list of strings adn returns it.

    :returns: a list of strings corresponding to the header
        names, if it identifies a header or an empty list
        if does not.

    :param table: dict[
        str,
        int  # page number
        | float  # reference y1_gap
        | pymupdf.Rect  # table's bbox
        | list[dict]  # a list of rows[cells[spans]]
        | list[tuple, tuple, tuple, tuple],  # list of cols bbox
    ]: a table dict. The rows in the list of row shall have
        been enlarged to have the keys provided by
        `_compute_tables_rows_properties`.

    '''
    _first_row: dict[str, Any] = table['rows'][0]  # type: ignore
    _second_row: dict[str, Any] = table['rows'][1]  # type: ignore

    # If the first row is a header
    if _is_first_row_header(_first_row, _second_row):
        return _extract_row(_first_row['cells'])

    return []


#####################
# To Markdown
#####################


def extract_stab_to_markdown(
    header_names: list[str],
    table_rows: list[list[str]] | list[Generator[str, Any, Any]],
    col_count: int,
) -> str:
    '''
    Function wrapping and configuring a call to
    `extract_table_to_markdown_generic` depending on
    whether an empty header_names list has been provided
    or not.

    If a populated header_names list has been passed-in,
    it has most likely been extracted from the table
    or by some other method.

    In this case, the first row shall not be considered
    as header row.
    '''
    # Decide whether the first row of the table shall
    # be output as a table row or not
    # hint: If a header_names has been passed-in,
    # it has probably been extracted from the table.
    # Accordingly, in this case, the first table row shall
    # not be printed out as a table row since it will
    # already have been handled as a header row.
    _print_first_row_as_table_row: bool = True

    if header_names:

        _print_first_row_as_table_row = False

    else:

        _print_first_row_as_table_row = True

    # Make the table md string
    return extract_table_to_markdown_generic(
        header_names=header_names,
        header_external_print_first_row=_print_first_row_as_table_row,
        table_rows=table_rows,
        col_count=col_count,
        clean=False,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
