# utils.py
'''
Module to encapsulate common utilities to the other packages of custrag.
'''
import logging

# from math import ceil, floor
from typing import Iterable

import pymupdf  # type: ignore  # noqa: I001

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
# Sorting functions
#####################


def sort_rect_key_by_bottom_y_left_x(
    rect: pymupdf.Rect,
) -> tuple[float, float]:
    '''
    The sorting key to sort a list of (int, Rect) tuples or a list of
    ((int, int), Rect) tuples, by Rectangles bottom y and left x.

    :param rect: pymupdf.Rect: a tuple with two items, an index
    (an int or a tuple[int, int]) and a value.
    '''
    return rect.y1, rect.x0


def sort_key_idx_rect_by_bottom_y_left_x(
    idx_rect_tup: tuple[int | tuple[int, int], pymupdf.Rect]
) -> tuple[float, float]:
    '''
    The sorting key to sort a list of (int, Rect) tuples or a list of
    ((int, int), Rect) tuples, by Rectangles bottom y and left x.

    :param idx_rect_tup: tuple[int | tuple[int, int], pymupdf.Rect]: a
        tuple with two items, an index (an int or a tuple[int, int]) and
        a values.
    '''
    return idx_rect_tup[1].y1, idx_rect_tup[1].x0


def sort_rects_tuples_list_by_y1_x0(
    idx_rect_iterable: (
        list[tuple[int, pymupdf.Rect]] | Iterable[tuple[int, pymupdf.Rect]]
    )
) -> list[tuple[int, pymupdf.Rect]]:
    '''
    Sorts the passed-in iterable or list of 2-tuples (int, pymupdf.Rectangles)
    by bottom y and left x and returns the sorted list of 2-tuples (int,
    pymupdf.Rectangle).

    :returns: the sorted list of 2-tuples (int, pymupdf.Rectangle).

    :param idx_rect_iterable: (
        list[tuple[int, pymupdf.Rect]] | Iterable[tuple[int, pymupdf.Rect]]
    ): either (i) a list of 2-tuples, in which the first item is an index
        number and the second is a rectangle and sorts the list by
        bottom y and left x; or (ii) a dict.items() where the keys are index
        numbers and the values are rectangle.

    '''
    return sorted(
        idx_rect_iterable,
        # Sort by bottom y (top to bottom) and left x (left to right)
        key=sort_key_idx_rect_by_bottom_y_left_x,
        # key=lambda _rect: (_rect[1].y1, _rect[1].x0),
    )


#####################
# Intersection functions
#####################


def intersects_rects(
    rect: pymupdf.Rect | pymupdf.IRect,
    rect_list: Iterable[pymupdf.Rect | pymupdf.IRect],
) -> bool:
    """
    Check if middle of rect is contained in a rect of the list.

    :param rect: pymupdf.Rect | pymupdf.IRect: a rectangle.
    :param rect_list: pymupdf.Rect | pymupdf.IRect: a list of rectangles.
    """
    # enlarge rect_list members somewhat by this
    # _delta: tuple = (-1, -1, 1, 1)

    _middle_point: pymupdf.Point = (rect.tl + rect.br) / 2
    _middle_point_x: float = _middle_point.x
    _middle_point_y: float = _middle_point.y

    for rectangle in rect_list:
        # middle point is inside rectangle
        # if (rect.tl + rect.br) / 2 in rectangle + _delta:
        _rect_x0: float = rectangle.x0 - 1
        _rect_y0: float = rectangle.y0 - 1
        _rect_x1: float = rectangle.x1 + 1
        _rect_y1: float = rectangle.y1 + 1
        if (_rect_x0 <= _middle_point_x <= _rect_x1) and (
            _rect_y0 <= _middle_point_y <= _rect_y1
        ):
            return True
    return False


#####################
# Rectangle containment check
#####################


def in_bbox(
    bb: pymupdf.Rect | pymupdf.IRect,
    bboxes: list[pymupdf.Rect | pymupdf.IRect],
) -> int:
    '''
    Return 1 or more if a bbox contains bb, else return 0.

    :param bb: pymupdf.Rect | pymupdf.IRect: the Rectangle we want to check
        whether it is contained in another one.

    :param bboxes: list[pymupdf.Rect | pymupdf.IRect]: the list of Rectangle
        we want to parse for containment.

    '''
    for i, bbox in enumerate(bboxes):
        # Rectangle containment check
        if bb in bbox:
            return i + 1
    return 0


#####################
# Container bbox computer
#####################


def compute_container_bbox_from_list_of_bboxes(
    list_bboxes: list[tuple[float, float, float, float]],
) -> tuple[float, float, float, float]:
    '''
    Compute the largest bbox containing all the bboxes in
    the list.

    :param list_bboxes: list[tuple[float, float, float, float]]: a list
        of bbox in the form of tuples of floats.
    '''
    _min_x: float = min(list(zip(*list_bboxes))[0])
    _min_y: float = min(list(zip(*list_bboxes))[1])
    _max_x: float = max(list(zip(*list_bboxes))[2])
    _max_y: float = max(list(zip(*list_bboxes))[3])

    return (_min_x, _min_y, _max_x, _max_y)


def compute_container_bbox_from_list_dicts_bbox_key(
    dicts_with_bbox: list[dict],
) -> tuple[float, float, float, float]:
    '''
    For a list of dict having a 'bbox' key where bboxes are stored
    as 4-tuples of float, compute the largest bbox contained the
    bboxes in the list.

    :param dicts_with_bbox: list[dict]: a list of 'blocks', 'lines'
        or 'spans'.

    '''

    if len(dicts_with_bbox) == 1:
        return dicts_with_bbox[0]['bbox']

    list_bboxes: list[tuple[float, float, float, float]] = [
        _textblock['bbox'] for _textblock in dicts_with_bbox  # type: ignore
    ]

    return compute_container_bbox_from_list_of_bboxes(list_bboxes)


def compute_container_bbx_from_contained_dict_bbxs(
    container: dict, subdict_key: str
) -> tuple[float, float, float, float]:
    '''
    Computes a bbox adjusted to the size of the bboxes
    of the items stored under the subdict_keys.

    :param container: dict: the container where the list
        of elements with bboxes is stored (usually a block
        to reduce its bbox to the size of its lines or a line
        to reduce its bbox to the size of its spans).

    :param subdict_key: str: the key under which the list of
        elements from which the container bbox coordinates
        shall be computed (usually 'lines' or 'spans').

    '''

    return compute_container_bbox_from_list_dicts_bbox_key(
        dicts_with_bbox=container[subdict_key],
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
