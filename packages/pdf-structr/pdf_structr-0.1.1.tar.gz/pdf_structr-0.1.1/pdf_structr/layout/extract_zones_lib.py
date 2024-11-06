# extract_zones_lib.py
'''
Low level horizontal or vertical zones extractions from a page.
'''

import copy
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
# Several text blocks in zone
#####################


def _initialize_zones_computation_variables(
    textblocks: list[dict],
    sort_key: int,
    end_key: int,
) -> tuple[float, list[dict]]:
    '''
    Initialize the variables to extract the zones.

    :returns: a tuple of an int, a float and a list[dict].

        - the int is the second key along the same coordinate axis as
        the sort key within a bbox tuple (if sort_key is 0, corresponding
        to x0, the int is 2, corresponding to x1).

        - the float is the right x or bottom y coordinate of the first text
        block in the search zone.

        - the list[dict] is a deep copy of the list of text blocks in the
        search zone, sorted by the sort_key (x0 or y0).

    :param textblocks: list[dict]: the textblocks between which we want
        compute intertext zone.

    :param sort_key: int: the sort key to sort the textblocks, by targeting
        an element of the bbox tuple. It must be either 0 (to sort by x0 when
        looking for vertical zones) or 1 (to sort by y0 when looking for
        vertical zones).

    :param end_key: int: 2 or 3, to be used to select the right x or the
        bottom y of the text blocks in the bbox tuples. 2 when looking for
        vertical zones and 3 when looking for horizontal zones.
    '''
    # Make a copy of the textblocks
    _temp_textblocks: list[dict] = copy.deepcopy(textblocks)

    # Sort the _temp_textblocks by the sort key (x0 or y0)
    _temp_textblocks.sort(key=lambda _txtblock: _txtblock['bbox'][sort_key])

    # Initialize a control variable _x1_or_y1_first_block with the x1 or y1
    # of the first textblock
    _x1_or_y1_first_block: float = _temp_textblocks[0]['bbox'][end_key]

    return _x1_or_y1_first_block, _temp_textblocks


def _initialize_zones_list(
    start_coord_search_zone: float,
    x0_or_y0_coord_first_text_block: float,
    x1_or_y1_coord_first_text_block: float,
) -> list[tuple[float, str]]:
    '''
    Initializes a zones list by append the first two or three values, depending
    whether the search zone starts on an intertext zone or a text zone.

    :param start_coord_search_zone: float: a float corresponding to the x0
        coordinate of the search zone (when making a list of vertical
        zones) or its y0 coordinate (when making a list of horizontal zones).

    :param x0_or_y0_coord_first_text_block: float: a float corresponding to
        the x0 coordinate of the first text block in the list (when making
        a list of vertical zones) or its y0 coordinate (when making a list of
        horizontal zones).

    :param x1_or_y1_coord_first_text_block: float: a float corresponding to
        the x1 coordinate of the first text block in the list (when making
        a list of vertical zones) or its y1 coordinate (when making a list of
        horizontal zones).
    '''
    # If the starting coord of the search zone is different than the starting
    # coord of the first text block, start the list with an intertext
    # zone.
    if start_coord_search_zone != x0_or_y0_coord_first_text_block:
        return [
            (start_coord_search_zone, 'intertext'),
            (x0_or_y0_coord_first_text_block, 'text'),
            # the start coordinate of the second intertext zone is temporarily
            # defined as the end coordinate of the first text zone
            (x1_or_y1_coord_first_text_block, 'intertext'),
        ]

    # Else if the search zone starts on the starting coordinate of the first
    # text block, start the list with a text zone.
    return [
        (x0_or_y0_coord_first_text_block, 'text'),
        # the start coordinate of the second intertext zone is temporarily
        # defined as the end coordinate of the first text zone
        (x1_or_y1_coord_first_text_block, 'intertext'),
    ]


def _initialize(
    textblocks: list[dict],
    start_coord_search_zone: float,
    start_key: int,
    end_key: int,
) -> tuple[list[dict], list[tuple[float, str]]]:
    '''
    Initialize the variables required to build a list of zone
    as well as an initialized list of zones, with the first two
    or three zones, depending on whether the first text zone
    starts on the starting coordinate of the search zone or not.

    :returns: the list of blocks sorted by the start_key and
        the list of zones initialized with the first two or three zones.

    :param textblocks: list[dict]: the textblocks from which we want
        compute zones, sorted by the start_key (0: x0 when looking
        for vertical zones or 1: y0 when looking for horizontal zones).

    :param start_coord_search_zone: float: a float corresponding to the x0
        coordinate of the search zone (when making a list of vertical
        zones) or its y0 coordinate (when making a list of horizontal zones).

    :param start_key: int: 0 or 1, to be used to select the left x or the
        top y of the text blocks in the bbox tuples. 0 when looking for
        vertical zones and 1 when looking for horizontal zones.

    :param end_key: int: 2 or 3, to be used to select the right x or the
        bottom y of the text blocks in the bbox tuples. 2 when looking for
        vertical zones and 3 when looking for horizontal zones.
    '''
    # Initialize the variables for the zones extraction
    # The returned _temp_textblocks is a deep copy of the list
    # of textblocks, sorted by the sort_key (0 or 1 => x0 or y0)
    _x1_or_y1_coord_first_text_block, _temp_textblocks = (
        _initialize_zones_computation_variables(
            textblocks=textblocks,
            sort_key=start_key,
            end_key=end_key,
        )
    )

    # Define and initialize the list of tuples that, for each horizontal zone,
    # will store the starting coordinates of the zone (y0) and its type
    # (text or intertext)
    zone_start_coord_list: list[tuple[float, str]] = _initialize_zones_list(
        start_coord_search_zone=start_coord_search_zone,
        x0_or_y0_coord_first_text_block=_temp_textblocks[0]['bbox'][start_key],
        x1_or_y1_coord_first_text_block=_x1_or_y1_coord_first_text_block,
    )

    return (
        _temp_textblocks,
        zone_start_coord_list,
    )


def _handle_overlapping_text_blocks(
    current_textblock: dict,
    zone_start_coord_list: list[tuple[float, str]],
    end_key: int,
) -> None:
    '''
    Updates the temporary left or top coordinate of the last
    intertext block in the list of zones to match the highest
    of the x1 or y1 of the current text block or such temporary
    left or top coordinate.

    :returns: None. The last element of the zone_start_coord_list
        is updated to the highest coordinates of the temporary
        start of the last intertext zone or the left or bottom
        coordinate of the current text block.

    :param previous_block_x1_or_y1: float: the previous text block x1 or y1,
        depending on the direction.

    :param current_textblock: dict: the current text block.

    :param zone_start_coord_list: list[tuple[float, str]]: a list of tuple,
        where each tuple stores the starting coordinate of a zone ('x0' or
        'y0') and the type of the following zone ('text' or 'intertext').

    :param end_key: int: the end key to select the x1 or y1 in the bbox tuple
        of the current text block. Should be either 2 or 3, for x1 or y1,
        depending on the direction.

    :param intertext_start_key: str: the starting key of an intertext zone
        ('x0' or 'y0').
    '''
    _temporary_x0_or_y0_of_last_intertext_zone: float = zone_start_coord_list[
        -1
    ][0]

    # The last intertext necessarily begins after the highest of the
    # currently registered start of the intertext zone in the list
    # and the end of the current text block.
    #
    # Update the last item of the zone_start_coord_list in case the
    # current text block ends after the end of the last zone.
    if (
        max(
            _temporary_x0_or_y0_of_last_intertext_zone,
            current_textblock['bbox'][end_key],
        )
        > _temporary_x0_or_y0_of_last_intertext_zone
    ):
        zone_start_coord_list[-1] = (
            current_textblock['bbox'][end_key],
            'intertext',
        )


def _handle_non_overlapping_text_blocks(
    current_textblock,
    zone_start_coord_list: list[tuple[float, str]],
    start_key: int,
    end_key: int,
) -> None:
    '''
    We have non-overlapping text blocks => we have an intertext block.
    The last element of the list (which is necessarily an intertext)
    is already up to date. We need to add a text zone starting at the
    beginning of the current text block and an intertext zone starting
    (temporarily) at the end of the current text block to the list.

    :returns: None. Updates the zone's list by adding a text and an intertext
        zone.

    :param previous_block_x1_or_y1: float: the previous text block x1 or y1,
        depending on the direction.

    :param current_textblock: dict: the current text block.

    :param zone_start_coord_list: list[tuple[float, str]]: a list of tuple,
        where each tuple stores the starting coordinate of a zone ('x0' or
        'y0') and the type of the following zone ('text' or 'intertext').

    :param start_key: the start key to select the x0 or y0 in the bbox tuple
        of the current text block. Should be either 0 or 1, for x0 or y0,
        depending on the direction.

    :param end_key: the end key to select the x1 or y1 in the bbox tuple
        of the current text block. Should be either 2 or 3, for x1 or y1,
        depending on the direction.
    '''
    # Add a new text zone starting at the start of the current _textblock.
    # and a new temporary intertext zone starting at the end of the current
    # _textblock.
    zone_start_coord_list.extend(
        [
            (current_textblock['bbox'][start_key], 'text'),
            (current_textblock['bbox'][end_key], 'intertext'),
        ]
    )


def _add_or_extend_zone(
    current_textblock: dict,
    zone_start_coord_list: list[tuple[float, str]],
    start_key: int,
    handle_overlapping_text_blocks_partial: Callable,
    handle_non_overlapping_text_blocks_partial: Callable,
) -> None:
    '''
    Adds a new zone or extends the last text zone in the list of
    zones depending on the passed-in text block.

    :param current_textblock: dict: the current text block.

    :param zone_start_coord_list: list[tuple[float, str]]: the list
        of zones tuples (starting coordinates and type of zone)

     :param start_key: int: 0 or 1, to be used to select the left x or the
        top y of the text blocks in the bbox tuples. 0 when looking for
        vertical zones and 1 when looking for horizontal zones.

    :param handle_overlapping_text_blocks_partial: Callable: the function
        that handles text blocks overlapping with the previous text block
        by extending the last zone in the zones' list.

    :param handle_non_overlapping_text_blocks_partial: Callable: the
        function that handles text blocks that do not overlap with the
        previous text block by adding a new intertext zone and a new
        text zone to the list.
    '''
    _previous_text_block_x1_or_y1 = zone_start_coord_list[-1][0]
    # The end of the previous textblock is higher than the beginning
    # of the current one => overlap
    # ---------------------------------
    # The intertext block must start somewhere below the maximum of the
    # `x1`s or `y1`s of the previous text block and this textblock.
    if _previous_text_block_x1_or_y1 > current_textblock['bbox'][start_key]:

        # We update _previous_block_x1_or_y1 to the max value
        # and we also update the temporary start key of the
        # following intertext block
        handle_overlapping_text_blocks_partial(
            current_textblock=current_textblock,
        )

        return

    # The current textblock does not overlap with the previous textblock
    # ---------------------------------
    # => We've got an intertext block.
    # We know where it starts: at the end of the previous textblock.
    # We know where the following text zone starts: at the beginning of
    # this textblock.

    handle_non_overlapping_text_blocks_partial(
        current_textblock=current_textblock,
    )


def _make_zones_list(
    textblocks: list[dict],
    start_coord_search_zone: float,
    end_coord_search_zone: float,
    start_key: int,
    end_key: int,
) -> list[tuple[float, str]]:
    '''
    Creates a zones' list then search for the text and intertext zones
    and append their start coordinates and their type as a tuple to the
    list.

    :returns: a list of tuples, where each tuple defines either a
        "white-space" vertical zone or a text block. "white-space" zones
        may contain images and vector graphics.

    :param textblocks: list[dict]: the textblocks from which we want
        compute zones, sorted by the start_key (0: x0 when looking
        for vertical zones or 1: y0 when looking for horizontal zones).

    :param start_coord_search_zone: float: a float corresponding to the x0
        coordinate of the search zone (when making a list of vertical
        zones) or its y0 coordinate (when making a list of horizontal zones).

    :param end_coord_search_zone: float: a float corresponding to the x1
        coordinate of the search zone (when making a list of vertical
        zones) or its y1 coordinate (when making a list of horizontal zones).

    :param start_key: int: 0 or 1, to be used to select the left x or the
        top y of the text blocks in the bbox tuples. 0 when looking for
        vertical zones and 1 when looking for horizontal zones.

    :param end_key: int: 2 or 3, to be used to select the right x or the
        bottom y of the text blocks in the bbox tuples. 2 when looking for
        vertical zones and 3 when looking for horizontal zones.
    '''
    # Initialize the list of zones and the variables necessary to feed the
    # list
    _temp_textblocks, _zone_start_coord_list = _initialize(
        textblocks=textblocks,
        start_coord_search_zone=start_coord_search_zone,
        start_key=start_key,
        end_key=end_key,
    )

    # Declare and configure two partials to handle overlapping and
    # non-overlapping text blocks
    _handle_overlapping_text_blocks_partial: Callable = functools.partial(
        _handle_overlapping_text_blocks,
        zone_start_coord_list=_zone_start_coord_list,
        end_key=end_key,
    )

    _handle_non_overlapping_text_blocks_partial: Callable = functools.partial(
        _handle_non_overlapping_text_blocks,
        zone_start_coord_list=_zone_start_coord_list,
        start_key=start_key,
        end_key=end_key,
    )

    _add_or_extend_zone_partial: Callable = functools.partial(
        _add_or_extend_zone,
        zone_start_coord_list=_zone_start_coord_list,
        start_key=start_key,
        handle_overlapping_text_blocks_partial=(
            _handle_overlapping_text_blocks_partial
        ),
        handle_non_overlapping_text_blocks_partial=(
            _handle_non_overlapping_text_blocks_partial
        ),
    )

    # Walk the _temp_textblocks and check whether each one overlaps with
    # the previous textblock
    # NOTE: Refacto: on first iteration, we're checking the first text block
    # against itself.
    # NOTE: Refacto: we do not need _previous_text_block_x1_or_y1, since
    # the same value is stored in _temp_textblocks[-1][0]
    # NOTE: Refacto: we could highly simplify the whole stuff and extract
    # the code block into the loop to a stand alone function
    for _this_textblock in _temp_textblocks:

        _add_or_extend_zone_partial(
            current_textblock=_this_textblock,
        )

    # If the last starting coordinate in the list is equal to
    # the end coordinate of the search zone, return the list
    # chopped off its last item
    if _zone_start_coord_list[-1][0] == end_coord_search_zone:
        return _zone_start_coord_list[:-1]

    # Else return the full list
    return _zone_start_coord_list


#####################
# Only one text block in zone
#####################


def _make_zones_list_if_only_one_text_block(
    textblock: dict,
    start_coord_search_zone: float,
    end_coord_search_zone: float,
    start_key: int,
    end_key: int,
) -> list[tuple[float, str]]:
    '''
    Handles the case where there is only one text block in the zone.

    :returns: a list of tuples, where each tuple defines either a
        "white-space" vertical zone or a text block. "white-space" zones
        may contain images and vector graphics.

    :param textblock: dict: the only text block in the zone.

    :param start_coord_search_zone: float: the zone's starting x0 coord (when
        making a list of vertical zones) or y0 coord (when making a list of
        horizontal zones).

    :param end_coord_search_zone: float: the zone's ending x1 coord (when
        making a list of vertical zones) or y1 coord (when making a list of
        horizontal zones).

    :param start_key: int: the key of the x0 (when making of a list of
        vertical zones) or y0 (when making a list of horizontal zones)
        to select in the textblock['bbox'].

    :param end_key: int: the key of the x1 (when making of a list of
        vertical zones) or y1 (when making a list of horizontal zones)
        to select in the textblock['bbox'].
    '''
    # If the textblock does NOT start on the same coord as the search zone,
    # create a zones' list that comprises two zones (an intertext zone
    # starting at the beginning of the search zone and a text zone starting
    # one the blocks starting coordinate).
    if start_coord_search_zone > textblock['bbox'][start_key]:
        logger.error(
            f"The search zone's initial coord `{start_coord_search_zone}`"
            f"is higher than the textblock's initial coord "
            "`{textblock['bbox'][start_key]}`"
        )
        raise Exception

    if start_coord_search_zone != textblock['bbox'][start_key]:
        _zone_start_coord_list = [
            (start_coord_search_zone, 'intertext'),
            (textblock['bbox'][start_key], 'text'),
        ]

    # Else (textblock starting after coord of search zone),
    # create a list with one text zone.
    else:
        _zone_start_coord_list = [(start_coord_search_zone, 'text')]

    # End: check whether the textblock ends on the same coord
    # as the search zone and add an intertext zone, as the case
    # may be
    if end_coord_search_zone != textblock['bbox'][end_key]:
        _zone_start_coord_list.append(
            (textblock['bbox'][end_key], 'intertext')
        )

    # Return the zones' list
    return _zone_start_coord_list


#####################
# Main
#####################


def make_zones_list(
    textblocks: list[dict],
    start_coord_search_zone: float,
    end_coord_search_zone: float,
    start_key: int,
) -> list[tuple[float, str]]:
    '''
    Computes a list of text and intertext horizontal or vertical zones
    from a list of passed-in textblocks.

    A zone is defined as a tuple with two items: its starting
    coordinates (y0 for horizontal zones and x0 for vertical zones)
    and its type.

    The other dimension of the zone ('x' or 'y' respectively) is implied
    from the larger rectangle (vertical or horizontal zone) in which
    the horizontal resp. vertical zones are computed
    => the horizontal zones occupy the whole width of the vertical zone
    to which they pertain (on first call, this vertical zone is usually
    the page).
    => respectively, the vertical zones occupy the whole height of the
    the horizontal zone to which they pertain.

    On first call (when looking for horizontal zones in the page), the
    whole list of text blocks is passed-in.

    On further calls (when looking for vertical zones inside the horizontal
    zones or when looking for horizontal zones within the vertical zones),
    the determination of the container zone is made by pre-filtering the
    passed-in textblocks, so that the passed-in list contains textblocks
    located within the container zone only.

    Horizontal zones permit identifying various coherent horizontal layout
    elements in a document (for instance, headings, subheadings, body text
    paragraphs). Vertical zones are then identified. Such vertical zones
    may in turn contain horizontal zones.

    Vertical zones permits the identification of text columns and/or tables.

    :returns: a list of dict, where each dict defines a "white-space" zone
        between two text blocks contains two keys. Such "white-space" zones
        may however contains images and vector graphics.

    :param textblocks: list[dict]: the text blocks from which we want
        to identify text and intertext horizontal zones corresponding
        to the text blocks pertaining to a pre-identified vertical zone
        (on first call, this pre-identified vertical zone is the entire
        page).

    :param start_coord_search_zone: float: the starting y0 coordinates
        from which we should start looking for text or intertext vertical
        zones. On first call, this is the page's top boundary (1, y0).

    :param end_coord_search_zone: float: the ending y1 coordinates
        after which there will be no horizontal zones to be found.
        On first call, this is the page's bottom boundary (3, y1).

    :param start_key: int: 0 or 1, to be used to select the left x or the
        top y of the text blocks in the bbox tuples and to sort
        the textboxes. 0 when looking for vertical zones and 1
        when looking for horizontal zones.
    '''
    # Set the _end_key (i.e. the key in the bbox tuples that permits
    # selecting the end of the text blocks => x0 = 2 or y0 = 3)
    _end_key = start_key + 2

    # If there is only one text block, no need to sort and make complicated
    # calculations
    if len(textblocks) == 1:
        return _make_zones_list_if_only_one_text_block(
            textblock=textblocks[0],
            start_coord_search_zone=start_coord_search_zone,
            end_coord_search_zone=end_coord_search_zone,
            start_key=start_key,
            end_key=_end_key,
        )

    # Now make the list of starting coordinates of the zones and their types
    return _make_zones_list(
        textblocks=textblocks,
        start_coord_search_zone=start_coord_search_zone,
        end_coord_search_zone=end_coord_search_zone,
        start_key=start_key,
        end_key=_end_key,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
