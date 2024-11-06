# compute_zone_rects.py
'''
Computes zones rectangles.
'''

import functools
import logging
from typing import Callable

from pymupdf import Rect  # type: ignore

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
# Playground
#####################


def _convert_zone_to_rect_tuple(
    left_x: float,
    top_y: float,
    right_x: float,
    bottom_y: float,
    zone_type: str,
) -> tuple[Rect, str]:
    '''
    Unique function to convert float-type zone tuple
    to Rect-type tuple.
    '''
    return (
        Rect(
            left_x,
            top_y,
            right_x,
            bottom_y,
        ),
        zone_type,
    )


def _rect_for_unique_or_last_zone(
    zone: tuple[float, str],
    right_x: float,
    bottom_y: float,
) -> list[tuple[Rect, str]]:
    '''
    Returns a list with one tuple Rect-str for the last zone of the
    zones' list or the unique item of the zones' list.

    :param zone: tuple[float, str]: the unique or last item of the zones' list.
    :param right_x: float: the page's right x.
    :param bottom_y: float: the page's bottom y.
    '''
    return [
        _convert_zone_to_rect_tuple(
            0,
            zone[0],
            right_x,
            bottom_y,
            zone[1],
        )
    ]


def _convert_horizontal_zone_to_rect(
    current_zone: tuple[float, str],
    page_right_x: float,
    next_zone_top_y: float,
) -> tuple[Rect, str]:
    '''
    Converts an horizontal zone into a Rect when called
    within a loop iterating on an horizontal zones' list.

    :param current_zone: tuple[float, str]: the current zone tuple
        (actually, in the loop, the one of idx - 1, because zone
        tuples are ordered from top to bottom).
    :param page_right_x: float: the page's width.
    :param next_zone_top_y: float: the next zone top y (actually,
        in the loop, the one of idx, because zone tuples are ordered
        from top to bottom)
    '''
    return _convert_zone_to_rect_tuple(
        0,
        current_zone[0],
        page_right_x,
        next_zone_top_y,
        current_zone[1],
    )


def _rects_several_horizontal_zones(
    horizontal_zones_list: list[tuple[float, str]],
    rect_for_unique_or_last_zone_partial: Callable,
    page_right_x: float,
    len_list: int,
) -> list[tuple[Rect, str]]:
    '''
    Rectangles list for several horizontal zones.

    :param horizontal_zones_list: list[tuple[float, str]]: the list of
        horizontal zones identified in the page.
    :param rect_for_unique_or_last_zone_partial: Callable: the partial
        to transform the unique or last zone in the list of horizontal
        zones.
    :param page_right_x: float: the page's right x.
    :param len_list: int: the length of the list.
    '''
    # Get the last item in the zones' list
    _last_zone: tuple[float, str] = horizontal_zones_list[-1]

    # define and initialize a return list
    _return_list: list[Rect] = rect_for_unique_or_last_zone_partial(_last_zone)

    # prepare a partial for the iteration
    _convert_horizontal_zone_to_rect_partial: Callable = functools.partial(
        _convert_horizontal_zone_to_rect,
        page_right_x=page_right_x,
    )

    # iterate back to front
    _return_list.extend(
        [
            _convert_horizontal_zone_to_rect_partial(
                current_zone=horizontal_zones_list[_idx - 1],
                next_zone_top_y=horizontal_zones_list[_idx][0],
            )
            for _idx in range(len_list - 1, 0, -1)
        ]
    )

    # reverse list front to back (top to bottom)
    return _return_list[::-1]


def _special_case_horizontal_zones(
    horizontal_zones_list: list[tuple[float, str]],
    page_rect: Rect,
    rect_for_unique_or_last_zone_partial: Callable,
) -> list[tuple[Rect, str]]:
    '''
    Handles the special cases where the list of horizontal zones contains no
    zones or only one zone.

    :param horizontal_zones_list: list[tuple[float, str]]: the list of
        horizontal zones identified in the page.
    :param page_rect: Rect: the page's mediabox Rectangle.
    :param rect_for_unique_or_last_zone_partial: Callable: the partial
        to transform the unique or last zone in the list of horizontal
        zones.
    '''
    # 2. if the horizontal zones list is empty, return the page's rect as
    # an intertext
    if not horizontal_zones_list:
        return [(page_rect, 'intertext')]

    # 3. if the horizontal zones list has one item only
    return rect_for_unique_or_last_zone_partial(horizontal_zones_list[0])


def compute_horizontal_zones_rects(
    layout_dict: dict,
) -> list[tuple[Rect, str]]:
    '''
    Compute a list of horizontal zone rectangles out of the horizontal
    zones list.

    :param layout_dict: dict: the dict where we store the layout.
    '''
    # Get some variables for easier access
    _horizontal_zones_list: list[tuple[float, str]] = layout_dict[
        'horizontal_zones'
    ]
    _len_list: int = len(_horizontal_zones_list)
    _page_bbox: Rect = layout_dict['page']['bbox']

    # Create a partial to return a single item list of tuple[Rect, str]
    _rect_for_unique_or_last_zone_partial: Callable = functools.partial(
        _rect_for_unique_or_last_zone,
        right_x=_page_bbox.x1,
        bottom_y=_page_bbox.y1,
    )

    # 1. If more than one item in the horizontal zones list
    if _len_list > 1:

        return _rects_several_horizontal_zones(
            _horizontal_zones_list,
            _rect_for_unique_or_last_zone_partial,
            _page_bbox.x1,
            _len_list,
        )

    # 2. Zero or one zone only in the list
    return _special_case_horizontal_zones(
        _horizontal_zones_list,
        _page_bbox,
        _rect_for_unique_or_last_zone_partial,
    )


# NOTE: Refacto: combine with _convert_horizontal_zone_to_rect
def _convert_vertical_zone_to_rect(
    current_zone: tuple[float, str],
    rectangle_top_y: float,
    next_zone_right_x: float,
    rectangle_bottom_y: float,
) -> tuple[Rect, str]:
    '''
    Converts a vertical zone into a Rect when called
    within a loop iterating on a vertical zones' list.

    :param current_zone: tuple[float, str]: the current zone tuple
        (actually, in the loop, the one of idx - 1, because zone
        tuples are ordered from left to right).
    :param rectangle_bottom_y: float: the rectangle's top y.
    :param next_zone_right_x: float: the next zone right x (actually,
        in the loop, the one of idx, because zone tuples are ordered
        from left to right).
    :param rectangle_bottom_y: float: the rectangle's bottom y.
    '''
    return _convert_zone_to_rect_tuple(
        current_zone[0],
        rectangle_top_y,
        next_zone_right_x,
        rectangle_bottom_y,
        current_zone[1],
    )


# NOTE: see how to combine with _rects_several_horizontal_zones()
def _rects_several_vertical_zones(
    horizontal_rect: Rect,
    vertical_zones_list: list[tuple[float, str]],
) -> list[tuple[Rect, str]]:
    '''
    Function encapsulating the computation of vertical
    rectangles-type tuples when an horizontal rectangle
    contains several vertical zones.

    :param horizontal_rect: tuple[Rect, str]: the horizontal Rect
        containing the vertical zones in the vertical_zones_list.

    :param vertical_zones_list: list[tuple[float, str]]: the list of vertical
        zones in the horizontal Rect.
    '''
    # Get the last item in the zones' list
    _last_zone: tuple[float, str] = vertical_zones_list[-1]

    # define and initialize a return list
    _return_list: list[Rect] = _rect_for_unique_or_last_zone(
        _last_zone,
        horizontal_rect.x1,
        horizontal_rect.y1,
    )

    # iterate back to front
    len_list: int = len(vertical_zones_list)
    _return_list.extend(
        [
            _convert_vertical_zone_to_rect(
                current_zone=vertical_zones_list[_idx - 1],
                rectangle_top_y=horizontal_rect.y0,
                next_zone_right_x=vertical_zones_list[_idx][0],
                rectangle_bottom_y=horizontal_rect.y1,
            )
            for _idx in range(len_list - 1, 0, -1)
        ]
    )

    # reverse list front to back (top to bottom)
    return _return_list[::-1]


# NOTE: Refacto: see how to combine it with compute_horizontal_zones_rects
def _compute_vertical_rects_in_horizontal_rect(
    horizontal_rect: tuple[Rect, str],
    vertical_zones_list: list[tuple[float, str]],
) -> list[tuple[Rect, str]]:
    '''
    Rectangles list for several vertical zones.

    :param horizontal_rect: tuple[Rect, str]: the horizontal Rect-type
        tuple which Rectangle contains the vertical zones in the
        vertical_zones_list.

    :param vertical_zones_list: list[tuple[float, str]]: the list of vertical
        zones in the horizontal Rect.
    '''
    _horizontal_rect: Rect = horizontal_rect[0]

    if len(vertical_zones_list) == 1:
        return _rect_for_unique_or_last_zone(
            vertical_zones_list[0],
            _horizontal_rect.x1,
            _horizontal_rect.y1,
        )

    return _rects_several_vertical_zones(
        horizontal_rect=_horizontal_rect,
        vertical_zones_list=vertical_zones_list,
    )


def _special_case_vertical_zones(
    horizontal_rect: tuple[Rect, str],
    vertical_zones_list: list[tuple[float, str]],
) -> list[list[tuple[Rect, str]]]:
    '''
    Handles the special cases where the list of horizontal Rect list contains
    only one Rect.

    :param horizontal_rect: tuple[Rect, str]: the unique horizontal Rect-type
        tuple in the list of horizontal Rect.
    :param vertical_zones_list: list[tuple[float, str]]: the list of vertical
        zones in the horizontal Rect.
    '''
    # if the horizontal rectangle is an intertext or if there is only one
    # item in the vertical zone list for the horizontal rectangle
    if horizontal_rect[1] == 'intertext' or len(vertical_zones_list) == 1:
        return [[horizontal_rect]]

    return [
        _compute_vertical_rects_in_horizontal_rect(
            horizontal_rect=horizontal_rect,
            vertical_zones_list=vertical_zones_list,
        )
    ]


def compute_vertical_zones_rects(
    layout_dict: dict,
) -> list[list[tuple[Rect, str]]]:
    '''
    Compute a list of vertical zone rectangles out of the vertical
    zones list.

    The function returns a list of list of tuples (Rect, str).
    The first list level corresponds to the horizontal zones.
    The second level corresponds to the vertical zones identified
    within the horizontal zone.
    The tuples are composed of a Rectangle corresponding to the
    intersection of the vertical zone with the horizontal zone
    (i.e. its y coordinates are those of the horizontal zone and
    its x coordinates are those of the vertical zone) and a string
    identifying the type of Rectangle zone ('text' or 'intertext').

    :param layout_dict: dict: the dict where we store the layout.
    '''
    _horizontal_rect_list: list[tuple[Rect, str]] = layout_dict[
        'horizontal_rects'
    ]
    _vertical_zones_list: list[list[tuple[float, str]]] = layout_dict[
        'vertical_zones'
    ]
    _len_lists: int = len(_horizontal_rect_list)

    # 1. If more than one item in the horizontal zones list
    if _len_lists > 1:

        return [
            _compute_vertical_rects_in_horizontal_rect(
                _horizontal_rect_list[_idx],
                _vertical_zones_list[_idx],
            )
            for _idx in range(0, _len_lists)
        ]

    # 2. One horizontal zone only in the list
    return _special_case_vertical_zones(
        _horizontal_rect_list[0],
        _vertical_zones_list[0],
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
