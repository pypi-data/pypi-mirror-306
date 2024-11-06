# extract_zones.py
'''
High level horizontal or vertical zones extractions from a page.
'''

import logging

from pdf_structr.layout.extract_zones_lib import (
    make_zones_list,
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
# Horizontal intertext zones computation
#####################


def compute_horizontal_text_intertext_zones(
    textblocks: list[dict],
    layout_dict: dict,
) -> list[tuple[float, str]]:
    '''
    Preconfigured call to _compute_text_intertext_zones_list to search
    text and intertext zones, page wide, in the whole page, from top to
    bottom.

    This function is called horizontal, because the text and intertext
    zones to be identified occupy the whole width of the page (or the clip).

    :returns: a list of text and intertext zones vertically ordered
        from top to bottom.

    :param textblocks: list[dict]: the list of all the text blocks on
        the page.
    :param layout_dict: dict: the layout_dict where the layout is being
        stored.
    '''
    return make_zones_list(
        textblocks=textblocks,
        start_coord_search_zone=layout_dict['page']['bbox'].y0,
        end_coord_search_zone=layout_dict['page']['bbox'].y1,
        start_key=1,
    )


#####################
# Vertical intertext zones computation
#####################


def _filter_textblocks_within_horizontal_text_zone(
    textblocks: list[dict],
    y0: float,
    y1: float,
) -> list[dict]:
    '''
    Filters the textblocks that are located within a given text
    zone.

    :returns: a list of the textblocks located within the given
        text zone.

    :param textblocks: list[dict]: the textblocks on the page.
    :param text_zone: dict[str, float]: an horizontal text zone.
    '''
    return [
        _textblock
        for _textblock in textblocks
        if (_textblock['bbox'][1] >= y0 and _textblock['bbox'][3] <= y1)
    ]


def _get_vertical_zones_within_text_zone(
    textblocks: list[dict],
    layout_dict: dict,
    idx: int,
) -> list[tuple[float, str]]:
    '''
    Get the text and intertext vertical zones located within the
    horizontal zone which index idx is passed in. The vertical zone
    is defined by its start (x0) and end (x1) coordinates.

    :returns: a list of text and intertext vertical zones.

    :param layout_dict: dict: the dict where we store the stats' results.

    :param textblocks: list[dict]: the textblocks on the page. They will be
        filtered in this function to retain only those that are located within
        the horizontal_zone.

    :param idx: the index number of the text or intertext horizontal zone
        to parse for vertical zones.
    '''
    # Case where the current_horizontal_zone is an horizontal intertext zone
    # => cannot contain any textblock, so return a vertical intertext zone
    # starting at x0 = 0
    if layout_dict['horizontal_zones'][idx][1] == 'intertext':
        return [(0, 'intertext')]

    # Filter the textblocks to retain only those within the target horizontal
    # zone
    _start_y: float = layout_dict['horizontal_zones'][idx][0]
    _end_y: float = layout_dict['horizontal_zones'][idx + 1][0]
    _textblocks_in_horizontal_text_zone: list[dict] = (
        _filter_textblocks_within_horizontal_text_zone(
            textblocks=textblocks,
            y0=_start_y,
            y1=_end_y,
        )
    )

    # Find and return the text and intertext vertical zones
    return make_zones_list(
        textblocks=_textblocks_in_horizontal_text_zone,
        start_coord_search_zone=layout_dict['page']['bbox'].x0,
        end_coord_search_zone=layout_dict['page']['bbox'].x1,
        start_key=0,
    )


def compute_vertical_text_intertext_zones_within_text_zones(
    textblocks: list[dict],
    layout_dict: dict,
) -> list[list[tuple[float, str]]]:
    '''
    Computes a list of text and intertext vertical zones within the
    text and intertext horizontal zones previously identified by iterating
    the horizontal zones.

    :returns: None: the dicts stored under the key 'horizontal_zones'
        in layout_dict are updated with an additional key 'vert_zones'
        which contains a list of tuple (y0, zone type) which refer the
        identified inner vertical zones.

    :param textblocks: list[dict]: the textblocks on the page.

    :param layout_dict: dict: the dict where we store the layout.
    '''
    # Iterate on the list of horizontal zones and try to identify
    # vertical text and intertext zones within each of them
    return [
        (
            _get_vertical_zones_within_text_zone(
                textblocks=textblocks,
                layout_dict=layout_dict,
                idx=_idx - 1,
            )
        )
        for _idx in range(1, len(layout_dict['horizontal_zones']) + 1, 1)
    ]


if __name__ == "__main__":
    pass
