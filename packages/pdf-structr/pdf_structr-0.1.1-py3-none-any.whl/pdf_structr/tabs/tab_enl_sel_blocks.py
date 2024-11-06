# tab_enl_sel_blocks.py
'''
Table enlargement: selection of blocks above and below a table
to try and enlarge.

Encapsulation of functions selecting blocks above or below
the tables, within a certain thresholds.

'''


import functools
import logging
from typing import Callable

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
# Get upper or lower blocks stack: abstract funtions
#####################


def _get_select_blocks(
    page_textblocks: list[dict[str, int | float | tuple | list]],
    select_fn: Callable,
) -> list[dict]:
    '''
    Given a group of textblocks extracted from a page and
    select_fn partial pre-configured with the start and end
    y coordinates where to look for additional blocks,
    return a list of matching blocks.

    :returns: a list of blocks matching the selection function.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        a list of text blocks for the page.

    :param select_fn: Callable: the selection function, as a partial
        pre-configured with coordinates where to look for the matching
        blocks.

    '''

    return [_block for _block in page_textblocks if select_fn(block=_block)]


def _is_bottom_y_in_vertical_clip(
    bbox: tuple[float, float, float, float],
    start_y_coord: float,
    end_y_coord: float,
) -> bool:
    '''
    Tests if a bbox bottom y is strictly within a vertical clip.

    :param bbox: tuple[float, float, float, float]: a bbox in the form
        of a 4-float tuple.

    :param start_y_coord: float: the starting y coordinates in a top-left
        based plan.

    :param end_y_coord: float: the ending y coordinates in a top-left
        based plan.

    '''
    return start_y_coord < bbox[3] < end_y_coord  # type: ignore


#####################
# Get upper or lower blocks stack: applied wrapper
#####################


def _is_block_in_upper_select_zone(
    block: dict,
    start_y_coord: float,
    end_y_coord: float,
) -> bool:
    '''
    Test if a block is between two y coordinates above a given
    start point (`start_y_coord`) but not above the `end_y_coord`.

    :param block: dict: the block on which the test is made.

    :param start_y_coord: float: the starting coordinate of the search
        zone. Since we are looking for blocks above this point, this
        coordinates is LARGER than `end_y_coord` (in a top-left based
        plan) and corresponds to the BOTTOM of the select zone.

    :param end_y_coord: float: the ending coordinate of the search
        zone. Since we are looking for blocks below this point, this
        coordinates is SMALLER than `start_y_coord` (in a top-left based
        plan) and corresponds to the TOP of the select zone.

    '''
    # return start_y_coord > block['bbox'][3] > end_y_coord  # type: ignore
    return _is_bottom_y_in_vertical_clip(
        block['bbox'], start_y_coord=end_y_coord, end_y_coord=start_y_coord
    )


def _is_block_in_lower_select_zone(
    block: dict,
    start_y_coord: float,
    end_y_coord: float,
) -> bool:
    '''
    Test if a block is between two y coordinates below a given
    start point (`start_y_coord`) but not below the `end_y_coord`.

    :param block: dict: the block on which the test is made.

    :param start_y_coord: float: the starting coordinate of the search
        zone. Since we are looking for blocks below this point, this
        coordinates is SMALLER than `end_y_coord` (in a top-left based
        plan) and corresponds to the TOP of the select zone.

    :param end_y_coord: float: the ending coordinate of the search
        zone. Since we are looking for blocks above this point, this
        coordinates is LARGER than `start_y_coord` (in a top-left based
        plan) and corresponds to the BOTTOM of the select zone.


    Select blocks between two y coordinates
    '''
    return _is_bottom_y_in_vertical_clip(
        block['bbox'], start_y_coord=start_y_coord, end_y_coord=end_y_coord
    )
    # return start_y_coord < block['bbox'][3] < end_y_coord  # type: ignore


def get_upper_blocks(
    limit_y_coord: float,
    start_y_coord: float,
    table_ref_y0_gap: float,
    page_textblocks: list[dict[str, int | float | tuple | list]],
) -> list[dict]:
    '''
    Returns a list of the text blocks which are living above the current
    table, but not too much

    :param limit: float: the limit above which we shall not be
        looking for blocks (either the previous table y1 or the top
        of the textpage_bbox).

    :param start_y_coord: float: the current table top y.

    :param table_ref_y0_gap: float: the typical gap between y0 of the
        rows pertaining to this table.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the text blocks in this page.

    '''
    # Define the y coordinate limit beyond which not to look for blocks:
    # the maximum y coord (i.e. the lower in top-left plan) between
    # (i) the top of the page or the previous table bottom y (`limit_y_coord`)
    # or (ii) the top of the current table - minus a certain amount of
    # table_ref_y0_gap.

    _end_y_coord: float = max(
        limit_y_coord,
        # table upper limit - 2.2 times the reference y0 gap
        (start_y_coord - (2.2 * table_ref_y0_gap)),  # type: ignore
    )

    _is_block_in_upper_select_zone_partial: Callable = functools.partial(
        _is_block_in_upper_select_zone,
        start_y_coord=start_y_coord,
        end_y_coord=_end_y_coord,
    )

    return _get_select_blocks(
        page_textblocks, _is_block_in_upper_select_zone_partial
    )


def get_lower_blocks(
    limit_y_coord: float,
    start_y_coord: float,
    table_ref_y0_gap: float,
    page_textblocks: list[dict[str, int | float | tuple | list]],
) -> list[dict]:
    '''
    Returns a list of the text blocks which are living below the current
    table, but not too much

    :param limit_y_coord: float: the limit below which we shall not be
        looking for tables (either the next table y0 or the bottom
        of the textpage_bbox).

    :param start_y_coord: float: the current table bottom y.

    :param table_ref_y0_gap: float: the typical gap between y0 of the
        rows pertaining to this table.

    :param page_textblocks: list[dict[str, int | float | tuple | list]]:
        the text blocks in this page.

    '''
    # Define the y coordinate limit beyond which not to look for blocks:
    # the minimum coord between (i) the bottom of the page or the previous
    # table top y (`limit_y_coord`) or (ii) the bottom of the current
    # table + plus a certain amount of table_ref_y0_gap.
    _end_y_coord: float = min(
        limit_y_coord,
        (start_y_coord + (2 * table_ref_y0_gap)),  # type: ignore
    )

    _is_block_in_lower_select_zone_partial: Callable = functools.partial(
        _is_block_in_lower_select_zone,
        start_y_coord=start_y_coord,
        end_y_coord=_end_y_coord,
    )

    return _get_select_blocks(
        page_textblocks, _is_block_in_lower_select_zone_partial
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
