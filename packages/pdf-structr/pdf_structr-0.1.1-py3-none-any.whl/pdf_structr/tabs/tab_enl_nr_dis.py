# tab_enl_nr_dis.py
'''

Library encapsulating the detection and creation of new
new rows (nr) when trying to enlarge (enl) a table previously
detected by stabs (sub module of stabs_tbs_enl) when
there is a discrepancy between the identified number
of blocks or spans above or below the table.

'''


import copy
import logging
import statistics
from operator import itemgetter
from typing import Any, Callable, Generator

from pdf_structr.tabs.tab_fns import (
    compute_cols_max_extension_limits,
)
from pdf_structr.tabs_clust.clustc_blocks_to_rows import (
    convert_blocks_to_candidate_rows,
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
# Subfunctions for not enough blocks (need to add virtual cells)
#####################


def _determine_list_dict_vertical_alignment(
    dict_list: list[dict],
) -> int:
    '''
    Determine the vertical alignment of the dict (which must
    have a tuple 4-float bbox) by computing three standard dev
    for the top y, middle y and bottom y of the passed-in blocks.

    returns: 0, 1 or 2. 0 for top alignement, 1 for middle
        and 2 for bottom.

    :param dict_list: list[dict]: a list of blocks or a list of already
        made cells. Each of the elements must have a bbox 4-float tuple

    '''
    _stdev_top_y: float = statistics.stdev(
        round(_dict['bbox'][1]) for _dict in dict_list
    )

    _stdev_mid_y: float = statistics.stdev(
        _compute_middle_y_coord(_dict['bbox']) for _dict in dict_list
    )

    _stdev_bot_y: float = statistics.stdev(
        round(_dict['bbox'][3]) for _dict in dict_list
    )

    # Compute and return the index of the minimun stdv
    return min(
        enumerate([_stdev_top_y, _stdev_mid_y, _stdev_bot_y]),
        key=itemgetter(1),
    )[0]


def _compute_middle_y_coord(bbox: tuple[float, float, float, float]) -> float:
    '''
    Computes the middle y coordinates from a passed in bbox
    tuple.

    :param bbox: tuple[float, float, float, float]: a bbox
        tuple.
    '''
    return round(bbox[1] + ((bbox[3] - bbox[1]) / 2))


def _compute_middle_y_coord_series(
    dicts_with_bbox: list[dict],
) -> Generator[float, Any, Any]:
    '''
    Computes a series of middle y coordinates for a list
    of dict containing a 'bbox' key storing a bbox as
    4-float tuple.

    Returns a generator of floats.
    '''
    return (
        _compute_middle_y_coord(_dict_with_bbox['bbox'])
        for _dict_with_bbox in dicts_with_bbox
    )


def _get_ref_y_coordinate_for_list_dict(
    vert_align: int,
    dict_list: list[dict],
) -> int:
    '''
    Compute the reference y coordinate to be used
    to create virtual cells depending on the smallest
    standard deviation on the top ys, middle ys and bottom ys.

    :param vert_align: int: one of 0, 1 or 2. 0 for top alignement,
        1 for middle and 2 for bottom.

    :param dict_list: list[dict]: a list of blocks or a list of already
        made cells. Each of the elements must have a bbox 4-float tuple
    '''
    _ref_y_coord: float | int

    # top alignement
    if vert_align == 0:
        # top aligned
        _ref_y_coord = statistics.fmean(
            round(_dict['bbox'][1]) for _dict in dict_list
        )

    # bottom alignement
    elif vert_align == 2:
        # bottom aligned
        _ref_y_coord = statistics.fmean(
            round(_dict['bbox'][3]) for _dict in dict_list
        )

    # centered
    else:
        _ref_y_coord = statistics.fmean(
            _compute_middle_y_coord_series(dict_list)
        )

    return round(_ref_y_coord)


def _get_ref_y_coordinate_for_new_row(
    dict_list: list[dict],
) -> float:
    '''
    Compute the y reference coordinate for the passed-in list of dicts.
    We take the average of the series of top ys, middle ys and bottom ys
    which has the lowest standard deviation.

    :param dict_list: list[dict]: a list of blocks or a list of already
        made cells. Each of the elements must have a bbox 4-float tuple

    '''

    if len(dict_list) > 2:

        # NOTE: need to check that the dicts do not overlap horizontally

        # Sort the dicts by x0
        dict_list.sort(key=lambda _dict: _dict['bbox'][0])

        # Compute the dict's alignment (standard dev method)
        _vert_align: int = _determine_list_dict_vertical_alignment(dict_list)

        # Get the corresponding fmean
        return _get_ref_y_coordinate_for_list_dict(_vert_align, dict_list)

    # This is the case when the list of dict_list contains only
    # one single block or cell
    # NOTE: we should first try to identify the table rows vertical
    # alignment to choose between the top, bottom or middle y coord.
    return _compute_middle_y_coord(dict_list[0]['bbox'])


def _prep_list_dict_iteration(
    dict_list: list[dict],
    table: dict,
) -> tuple:
    '''
    Prepares the iteration on the dict elements to generate a row with virtual
    cells by getting the required variables.

    :returns: a 5-tuple with:

    - a list of 2-float tuple for each column in the existing table
    - a reference y coordinate for the virtual cells to be created
    - an empty list of cells to store the new cells that will be created
    - a initial item index set at 0
    - the dicts' count to control the access to the items

    :param dict_list: list[dict]: a list of blocks or a list of already
        made cells. Each of the elements must have a bbox 4-float tuple

    :param table: dict: the table which we are trying to extend.

    '''
    # Declare and get a list of columns maximum lateral extension:
    # a list of 2-float tuples with the coordinates of the maximum
    # possible extensions of each column to the right and to the left
    _cols_max_ext: list[tuple[float, float]] = (
        compute_cols_max_extension_limits(cols=table['cols'])
    )

    # Compute a y reference coordinate for the new row: this will be used
    # when building the virtual cells' bboxes.
    _ref_y_coord: float = _get_ref_y_coordinate_for_new_row(dict_list)

    # Declare a cells list to store the cells that will be made
    _cells: list = []

    # Declare two control variables to access the blocks when iterating
    _elt_idx: int = 0
    _max_elt_idx: int = len(dict_list)

    return (
        _cols_max_ext,
        _ref_y_coord,
        _cells,
        _elt_idx,
        _max_elt_idx,
    )


def _get_virtual_span_template(
    source_dict: dict,
) -> dict:
    '''
    Returns a virtual span template from a passed-in dict.

    :param source_dict: dict: the source dict to provide
        values to span's template. It should have the following
        keys: 'size', 'flags', 'font', 'color', 'ascender',
        'descender'
    '''
    # NOTE: for the moment, we pass the last span of the blocks
    # (neighbor_blocks[-1]['lines'][-1]['spans'][-1]) or cells
    # (_relevant_row_candidate[-1]['spans'][-1]) to
    # _get_virtual_span_template() to fill in the values for the
    # following keys:
    # - 'size'
    # - 'flags'
    # - 'font'
    # - 'color'
    # - 'ascender'
    # - 'descender'
    #
    # Ideally, we should either:
    # - compute the mode values (taking into account the char length
    # of each of theses spans) for all the spans of all the blocks
    # for each of the values that need to be updated
    # - take the immediately neighboring span

    # {
    #     'size': source_dict['size'],
    #     'flags': source_dict['flags'],
    #     'font': source_dict['font'],
    #     'color': source_dict['color'],
    #     'ascender': source_dict['ascender'],
    #     'descender': source_dict['descender'],
    #     'text': '-',
    #     # 'origin': tuple[float, float],
    #     # 'bbox': tuple[float, float, float, float]
    #     'txt_len': 1,
    #     'trail_ws': 0,
    #     'punct_count': 1,
    #     'digit_count': 0,
    # }

    # Define the keys and values to be updated in the source dict
    _virtual_spans_keys_vals: dict = {
        'text': '-',
        'txt_len': 1,
        'trail_ws': 0,
        'inner_ws': 0,
        'punct_count': 1,
        'digit_count': 0,
    }

    # Make a deepcopy of the source dict
    source_dict = copy.deepcopy(source_dict)

    # Update the source dict
    source_dict.update(_virtual_spans_keys_vals)

    return source_dict


def _add_imaginary_cell(
    cells: list[dict],
    ext_tup: tuple[float, float],
    ref_y_coord: float,
    spans_templat: dict,
) -> None:
    '''
    Creates an imaginary cell and appends it to the cells list.

    :param cells: list[dict]: the cells list.

    :param ext_tup: tuple[float, float]: the maximum x possible
        lateral extensions for the current column.
    '''
    # Determine the x coordinate of the imaginary cell as
    # the middle point between the x coordinates of the current
    # column
    _x_coord: float = ext_tup[0] + (ext_tup[1] - ext_tup[0]) / 2

    # Create a virtual span's dict
    _span: dict = copy.deepcopy(spans_templat)
    _span['bbox'] = (_x_coord, ref_y_coord, _x_coord, ref_y_coord)
    _span['origin'] = (_x_coord, ref_y_coord)

    # Append it to the cells
    # NOTE: the bbox is artifically reduced to a single point in the
    # plan. This is on purpose as it permits to identify the virtual
    # cells.
    cells.append(
        {
            'bbox': (_x_coord, ref_y_coord, _x_coord, ref_y_coord),
            'spans': [_span],
        }
    )


def _safe_get_curr_elt_by_idx(
    list_dict: list[dict],
    elt_idx: int,
    max_elt_idx: int,
) -> dict | None:
    '''
    Gets an element (a block or a cell) from the passed-in list of dict
    without exceeding the list.

    :returns: the element by index or None if the elements' count has
    been exceeded.

    :param list_dict: list[dict]: the list of blocks or cells from which we
        want to pick an element.

    :param elt_idx: int: the target index.

    :param max_elt_idx: int: the maximum index.

    '''
    # Get the current block if any block remains
    _curr_elt: dict | None = None
    if elt_idx < max_elt_idx:
        _curr_elt = list_dict[elt_idx]

    return _curr_elt


def _convert_block_to_cell(
    block: dict,
) -> dict:
    '''
    Given a block, returns a cell.
    '''
    return {
        'bbox': block['bbox'],  # type: ignore
        'spans': [
            _span
            for _line in block['lines']  # type: ignore
            for _span in _line['spans']
        ],
    }


def _make_cell_or_virtual_cell_core(
    curr_block: dict | None,
    block_idx: int,
    cells: list[dict],
    ext_tup: tuple[float, float],
    ref_y_coord: float,
    spans_template: dict,
    elt_to_cell_convrt_fn: Callable,
) -> int:
    '''
    Makes a cell or a virtual cell for a given column.

    :param curr_block: dict | None: a block dict to test if it fits
        or None if the block's count has been exceeded.

    :param max_block_idx: int: the maximum block index (block count - 1).

    :param block_idx: int: the current block index in the iteration.

    :param cells: list[dict]: the list of cells currently being built.

    :param ext_tup: tuple[float, float]: the maximum possible left and right
        extensions coordinates tuple.

    :param ref_y_coord: float: the reference y coordinate for the row (list
        of cells currently being built).

    :param spans_template: dict: the span's template.

    :param elt_to_cell_convrt_fn: Callable: a function to convert the
        passed-in elements into a cell.

    '''
    # 1. If no block remains in the list or if the current block
    #    is fully to the right of the current column or if the current
    #    block overlaps to the right of the maximum extension
    #
    #   -> add a virtual cell
    # -----------------------------------------------------------------

    if curr_block is None:
        _add_imaginary_cell(cells, ext_tup, ref_y_coord, spans_template)
        return block_idx

    # Get the current block's or cell's bbox for convience
    _curr_bbox: tuple[float, float, float, float] = curr_block['bbox']

    if (
        # Current block is fully to the right
        _curr_bbox[0] > ext_tup[1]
        # NOTE: ideally, we should assess whether the current block
        # left side would be higher than the next column maximum
        # left extension.
        # Current block is overlapping to the right
        or (_curr_bbox[2] >= ext_tup[1])
    ):

        _add_imaginary_cell(cells, ext_tup, ref_y_coord, spans_template)
        return block_idx

    # 2. If the current block width matches the width of the current
    #    column, append it as a cell to the current row
    #
    #   -> create a true cell
    # -----------------------------------------------------------------

    if (_curr_bbox[0] >= ext_tup[0]) and (  # type: ignore
        _curr_bbox[2] <= ext_tup[1]  # type: ignore
    ):

        cells.append(elt_to_cell_convrt_fn(curr_block))

        # increment the blocks index; upon next iteration,
        # we want to get the following block as current block
        block_idx += 1

        return block_idx

    # Fallback: the block starts to the left of the current column
    # -> in this case, we do not want to add a virtual cell
    # and we just want to return the current block idx
    # NOTE: actually, this should mean that this row does not fit
    # See how to refactor this.

    return block_idx


def _make_cell_or_virtual_cell(
    neighbor_blocks: list[dict],
    max_block_idx: int,
    block_idx: int,
    cells: list[dict],
    ext_tup: tuple[float, float],
    ref_y_coord: float,
    spans_template: dict,
    elt_to_cell_convrt_fn: Callable,
) -> int:
    '''
    Makes a cell or a virtual cell for a given column.

    :param neighbor_blocks: list[dict]: the list of neighbor blocks
        (above or below the table within reasonable distance).

    :param max_block_idx: int: the maximum block index (block count - 1).

    :param block_idx: int: the current block index in the iteration.

    :param cells: list[dict]: the list of cells currently being built.

    :param ext_tup: tuple[float, float]: the maximum possible left and right
        extensions coordinates tuple for a given column.

    :param ref_y_coord: float: the reference y coordinate for the row (list
        of cells currently being built).

    :param spans_template: dict: the span's template.

    :param elt_to_cell_convrt_fn: Callable: a function to convert the
        passed-in elements into a cell.

    '''
    # Get the current block if any block remains
    _curr_block: dict | None = _safe_get_curr_elt_by_idx(
        neighbor_blocks, block_idx, max_block_idx
    )

    return _make_cell_or_virtual_cell_core(
        curr_block=_curr_block,
        block_idx=block_idx,
        cells=cells,
        ext_tup=ext_tup,
        ref_y_coord=ref_y_coord,
        spans_template=spans_template,
        elt_to_cell_convrt_fn=elt_to_cell_convrt_fn,
    )


#####################
# Main subcases:
# - too many blocks (need to clean up)
# - not enough blocks (need to add virtual cells)
#####################


def _make_new_row_block_count_exceed_columns_count(
    neighbor_blocks: list[dict],
    table: dict,
    ext_direction: int,
) -> list[dict]:
    '''
    Try to make a row when the neighbor blocks' count exceeds
    that of the columns.

    :param neighbor_blocks: list[dict]: the list of neighbor blocks
        (above or below the table within reasonable distance).

    table: dict: the current table dictionary.

    :param ext_direction: int: -1 or 0, with -1 being when extending
        upwards and 0 when extending downwards.

    '''
    # Convert the blocks to candidate rows; the returned candidate rows
    # are lists of cells which each may not match with the columns' count
    # or sizes of the table.
    _candidate_rows_list: list[list[dict]] = convert_blocks_to_candidate_rows(
        neighbor_blocks
    )

    # Shortcut if no rows returned
    if not _candidate_rows_list:
        return []

    # Select the relevant candidate row (if we're trying to extend upwards,
    # we take the last one [-1]; if we're extending up, we take the first one)
    _relevant_row_candidate = _candidate_rows_list[ext_direction]

    return _make_new_row_with_virtual_cells(
        neighbor_blocks=_relevant_row_candidate,
        # we pass the last span as source_span for the spans' template
        source_span=_relevant_row_candidate[-1]['spans'][-1],
        table=table,
        elt_to_cell_convrt_fn=(lambda _cell: _cell),
    )


def _make_new_row_with_virtual_cells(
    neighbor_blocks: list[dict],
    source_span: dict,
    table: dict,
    elt_to_cell_convrt_fn: Callable,
) -> list[dict]:
    '''
    Makes a new row by adding "virtual" cells when the collected blocks,
    do not fill all the cells to make a full row with all its columns.

    :param neighbor_blocks: list[dict]: the list of neighbor blocks
        (above or below the table within reasonable distance).

    :param table: dict: the current table dictionary.

    :param elt_to_cell_convrt_fn: Callable: a function to convert the
        passed-in elements into a cell.

    '''
    # Prepare the blocks iteration by generating a list of variables
    (
        _cols_max_ext,
        _ref_y_coord,
        _cells,
        _block_idx,
        _max_block_idx,
    ) = _prep_list_dict_iteration(neighbor_blocks, table)

    # Declare a span's template
    _spans_template: dict = _get_virtual_span_template(source_span)

    # Sort the blocks
    # NOTE: To be completed

    # Walk the maximum extensions tuples for the columns of the table
    # = walk the columns
    for _ext_tup in _cols_max_ext:

        _block_idx = _make_cell_or_virtual_cell(
            neighbor_blocks,
            _max_block_idx,
            _block_idx,
            _cells,
            _ext_tup,
            _ref_y_coord,
            _spans_template,
            elt_to_cell_convrt_fn=elt_to_cell_convrt_fn,
        )

    # Just to make sure that all the blocks have been converted to cells
    # Otherwise, it means something went wrong
    if _block_idx == len(neighbor_blocks):
        return _cells

    return []


#####################
# Main API
#####################


def make_new_row_when_discrepancy(
    neighbor_blocks: list[dict],
    table: dict,
    ext_direction: int,
) -> list[dict]:
    '''
    Tries to make a new row when there is a discrepancy between the number of
    blocks and the number of columns in the blocks collected from above or from
    below.

    :param neighbor_blocks: list[dict]: the list of neighbor blocks
        (above or below the table within reasonable distance).

    table: dict: the current table dictionary.

    :param ext_direction: int: -1 or 0, with -1 being when extending
        upwards and 0 when extending downwards.

    '''

    # When too many blocks compared to the columns count
    if len(neighbor_blocks) > len(table['cols']):

        return _make_new_row_block_count_exceed_columns_count(
            neighbor_blocks=neighbor_blocks,
            table=table,
            ext_direction=ext_direction,
        )

    # When not enough blocks compared to the columns count

    return _make_new_row_with_virtual_cells(
        neighbor_blocks=neighbor_blocks,
        # we pass the last span as source_span for the spans' template
        source_span=neighbor_blocks[-1]['lines'][-1]['spans'][-1],
        table=table,
        elt_to_cell_convrt_fn=_convert_block_to_cell,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
