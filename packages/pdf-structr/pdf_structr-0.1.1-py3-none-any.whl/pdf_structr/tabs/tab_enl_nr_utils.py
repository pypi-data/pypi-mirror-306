# tab_enl_nr_utils.py
'''

Library encapsulating the detection and creation of new
rows (nr) when trying to enlarge (enl) a table previously
detected by stabs (sub module of stabs_tbs_enl).

'''

import logging

from pdf_structr.tabs.tab_fns import (
    compute_cols_max_extension_limits,
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
# Test mergeability of two lines
#####################


def _is_horizontally_contained_within(
    bbox_1: tuple[float, float, float, float],
    bbox_2: tuple[float, float, float, float],
) -> bool:
    '''
    Check whether bbox_2 is horizontally contained within bbox_2.
    '''
    return (bbox_1[0] <= bbox_2[0] < bbox_1[2]) and (
        bbox_1[0] < bbox_2[2] <= bbox_1[2]
    )


def _are_horizontally_contained_within(
    bbox_1: tuple[float, float, float, float],
    bbox_2: tuple[float, float, float, float],
) -> bool:
    '''
    Check if one the two bboxes horizontally contains the other.
    '''
    return _is_horizontally_contained_within(
        bbox_1,
        bbox_2,
    ) or _is_horizontally_contained_within(
        bbox_2,
        bbox_1,
    )


def _are_vertically_mergeable(
    curr_line_bbox: tuple[float, float, float, float],
    next_line_bbox: tuple[float, float, float, float],
) -> bool:
    '''
    Checks whether two lines are "mergeable" into a single
    cell by checking if one of them contains the other horizontally
    and whether they are close vertical neighbors.
    '''
    return (
        # containement check
        _are_horizontally_contained_within(
            curr_line_bbox,
            next_line_bbox,
        )
        # if the two lines are vertically closer than the
        # current line's height
        and (
            next_line_bbox[1] - curr_line_bbox[3]  # y gap
            < curr_line_bbox[3] - curr_line_bbox[1]  # line height
        )
    )


#####################
# Convert lines to cell
#####################


def _merge_lines_into_a_cell(
    curr_line: dict[str, tuple[float, float, float, float] | list[dict]],
    next_line: dict[str, tuple[float, float, float, float] | list[dict]],
) -> dict[str, tuple[float, float, float, float] | list[dict]]:
    '''
    From two lines, returns a cell.
    '''

    # Merge close lines into a single cell
    _spans: list[dict] = (
        curr_line['spans'] + next_line['spans']  # type: ignore
    )

    # Sort the new list of spans
    _spans.sort(key=lambda _span: _span['bbox'][3])

    # Make the cell and return it
    return {
        'bbox': (
            min(curr_line['bbox'][0], next_line['bbox'][0]),  # type: ignore
            min(curr_line['bbox'][1], next_line['bbox'][1]),  # type: ignore
            max(curr_line['bbox'][2], next_line['bbox'][2]),  # type: ignore
            max(curr_line['bbox'][3], next_line['bbox'][3]),  # type: ignore
        ),
        'spans': _spans,
    }


def convert_lines_to_cell(
    curr_line: dict,
    next_line: dict,
    merged: bool,
    tentative_row: list[dict],
) -> bool:
    '''
    Converts a pair of lines into a cell.

    "Merge" the lines into a single cell if one of them horizontally
    contains the other and if they are close vertical neighbors.

    Create a cell with the spans and bbox of the current span otherwise.

    Returns True if it has merged the lines and False otherwise.


    :param curr_line: dict: the current line.

    :param next_line: dict: the following line.

    :param merged: bool: a witness to mark whether the current line
        has already been handled and merged or if it needs to
        be handled. The witness is reset at each iteration to True
        or False by the return value of this function.

    :param tentative_row: list[dict]: the tentative row list of dict
        that we are building.

    '''
    # If this line has already been merged
    if merged is True:
        # reset the _merged witness to False for next iteration
        return False

    # Get the line's bboxes
    curr_line_bbox: tuple[float, float, float, float] = curr_line['bbox']
    next_line_bbox: tuple[float, float, float, float] = next_line['bbox']

    # if two consecutive lines are horizontally contained within
    # one another and are horizontally very close, make a single
    # cell with the two lines
    if _are_vertically_mergeable(curr_line_bbox, next_line_bbox):

        # Merge close lines into a single cell
        _cell = _merge_lines_into_a_cell(curr_line, next_line)

        tentative_row.append(_cell)

        # return True to signal that the next span has already
        # been handled
        return True

    # If the two cells are far apart, add the current line as a cell of its own
    else:

        # Append the current line as a cell
        tentative_row.append(
            {
                'bbox': curr_line['bbox'],
                'spans': curr_line['spans'],
            }
        )

        # return False to signal that the next span still needs to be handled
        return False


#################################
# Test tentative row for compliance with current table structure
#################################


def _do_cells_overlap_horizontally(tentative_row: list[dict]) -> bool:
    '''
    Check whether the cells contained in the tentative row
    overlap each other horizontally.

    NOTE: check module validate_table: there is something similar
    there.

    NOTE: checks for bottom right overlaps.
    '''

    # Now check if the cells do not overlap each other
    for _curr_cell, _next_cell in zip(
        tentative_row[:-1],
        tentative_row[1:],
    ):
        if _curr_cell['bbox'][2] >= _next_cell['bbox'][0]:
            return True

    return False


def _do_row_cells_fit_in_cols(
    tentative_row: list[dict],
    table: dict,
) -> bool:
    '''
    Tests whether a candidate row fits (horizontally) in the
    corresponding table's columns.

    The columns maximum possible lateral extension is recomputed each time.
    '''

    # Declare a column of maximum extension: a tuple of float with
    # the maximumn acceptable extension to the right and to the left
    _max_ext: list[tuple[float, float]] = compute_cols_max_extension_limits(
        cols=table['cols']
    )

    # Walk the cells and the extension limits and
    # for each cell, test whether it fits within the extension
    # limits
    for _cell, _ext_tup in zip(tentative_row, _max_ext):
        if (
            # the cell's x0 must be strictly inferior to the
            # column's max extension to the left
            _cell['bbox'][0]
            < _ext_tup[0]  # type: ignore
        ) or (
            # the cell's x1 must be strictly superior to the
            # column's max extension to the right
            _cell['bbox'][2]
            > _ext_tup[1]  # type: ignore
        ):
            return False

    return True


def is_tentative_row_acceptable(
    tentative_row: list[dict],
    table,
) -> bool:
    '''
    Tests whether a tentative row is acceptable for insertion.

    Criteria:
    - there should be a tentative row
    - its length (number of cells) shall be equal to the number of cols
    - its cells shall not overlap each other horizontally
    - the cells shall fit within the existing columns (up to their maximum
    possible left and right extensions).
    '''
    # If an empty list, return False
    if not tentative_row:
        return False

    # If the tentative row has not the same length (it is basically
    # at this stage just a list of cells dict) as the number
    # of columns, return False
    if not (len(tentative_row) == len(table['cols'])):  # type: ignore
        return False

    # If the cells of the tentative row overlap each other,
    # return False
    if _do_cells_overlap_horizontally(tentative_row):  # type: ignore
        return False

    # Test if the tentative rows' cells fit into the existing
    # columns without breaking the table, prepend the tentative row
    if _do_row_cells_fit_in_cols(
        tentative_row=tentative_row,
        table=table,
    ):
        return True

    return False


#####################
# Main make new tentative row (i.e. list of cells) function
#####################


def make_new_row_from_lines(
    lines: list[dict],
    *args,
    **kwargs,
) -> list[dict]:
    '''
    Try to make a tentative row out of a list of line dicts by
    converting them to a list of cells where cells are dicts
    containing a list of spans and a bbox. Some cells may
    contains several spans deemed close neighbors or overlapping.

    Returns a tentative row, i.e. a list of cells.

    :param lines: list[dict]: a list of lines to convert to a row.
    '''

    # Sort them by x0: in _make_new_row_from_lines,
    # we are going to try and identify lines that
    # are on the same geometrical row and are separated
    # by a gap that could correspond to a column separation.
    lines.sort(key=lambda _line: _line['bbox'][0])

    # Try to build a row of cells
    _tentative_row: list[dict] = []
    _merged: bool = False

    # Walk the lines in the block two by two
    for _curr_line, _next_line in zip(lines[:-1], lines[1:]):

        _merged = convert_lines_to_cell(
            curr_line=_curr_line,
            next_line=_next_line,
            merged=_merged,
            tentative_row=_tentative_row,
        )

    # Handle the last line: if the ultimate line has not
    # been merged with the previous one, we need to get it
    # out of the list of lines and append to the tentative row
    if _merged is False:

        _tentative_row.append(
            {
                'bbox': lines[-1]['bbox'],  # type: ignore
                'spans': lines[-1]['spans'],  # type: ignore
            }
        )

    return _tentative_row


#####################
# Blocks flattening function
#####################


def flatten_lines_in_blocks(neighbor_blocks: list[dict]) -> list[dict]:
    '''
    Flattens the lines living in a list of blocks.

    :param neighbor_blocks: list[dict]: a list of blocks living above
        or below the table.

    '''
    # Flatten the lines in the blocks
    return [_line for _block in neighbor_blocks for _line in _block['lines']]


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
