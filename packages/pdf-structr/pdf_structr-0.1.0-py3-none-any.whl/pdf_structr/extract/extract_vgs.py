# extract_vgs.py
'''
Storing utility functions that extract vg_clusters Rectangles from a PDF page.
'''


from collections import deque

import pymupdf  # type: ignore

from pdf_structr.utils.utils import (
    intersects_rects,
    sort_rect_key_by_bottom_y_left_x,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


def _poly_area(points: list[pymupdf.Point]) -> float:
    """
    Compute the area of the polygon represented by the given points.

    We are using the shoelace algorithm (Gauss) for this.

    Accepts a list of Point items and returns a float.
    """
    # make a local copy of points (do not change the original)
    _points = points[:]
    # remove duplicated connector points first
    for i in range(len(_points) - 1, 0, -1):
        if _points[i] == _points[i - 1]:
            del _points[i]

    area = 0
    for i in range(len(_points) - 1):
        p0 = _points[i]
        p1 = _points[i + 1]
        area += p0.x * p1.y - p1.x * p0.y

    return abs(area) / 2


def _is_in_rects(
    rect: pymupdf.Rect,
    rect_list: list[pymupdf.Rect],
):
    """
    Check if rect is contained in a rect of the list.
    """
    for i, rectangle in enumerate(rect_list, start=1):
        if rect in rectangle:
            return i
    return 0


def _is_significant(
    box: pymupdf.Rect,
    paths: list[
        dict[
            str,
            str
            | int
            | float
            | bool
            | tuple[int, int, int]
            | tuple[float, float, float]
            | list[tuple[str, pymupdf.Point, pymupdf.Point]]
            | pymupdf.Rect
            | None,
        ]
    ],
) -> bool:
    '''
    Check whether the rectangle "box" contains 'signifiant' drawings.

    'Significant' means that at least one stroked path must cover an area
    less than 90% of box.
    Not significant means that the graphic is decoration only (highlighting,
    border-only etc.). It will not be considered further.

    :param box: pymupdf.Rect: a Rect items wrapping line-art items
        that are close enough to be considered forming a common
        vector graphic

    :param paths: list[
        dict[
            str,
            str
            | int
            | float
            | bool
            | tuple[int, int, int]
            | tuple[float, float, float]
            | list[tuple[str, pymupdf.Point, pymupdf.Point]]
            | pymupdf.Rect
            | None,
        ]
    ]: a list of paths in the page not contained in any table and
        not a full page graphic.
    '''
    # 90% of area of box
    box_area: float = abs(box) * 0.9

    # Walk the path
    for path in paths:

        # Check if the path's rectangle is contained within the box rectangle
        # If not, ignore the path
        if path["rect"] not in box:
            continue

        # path["items"] is a list of tuple, each containing a string flag
        # indicating the type of the item ('c': curve, 'l': line,
        # 'q': quad) and two pymupdf.Point.
        list_items_in_path: list[
            tuple[str, pymupdf.Point, pymupdf.Point]
        ] = path[
            "items"
        ]  # type: ignore

        # Check if any borderless rectangles are contained
        # If so, ignore the path
        if (
            path["type"] == "f"
            # This is a set comprehension; we check if any item of the
            # path is a rectangle
            and {item[0] for item in list_items_in_path}
        ) == {"re"}:
            continue

        # Walk the Points in the items' list and append all the points
        # as they occur.
        #
        _points: list = []  # list of points represented by the items.
        for item in list_items_in_path:
            # item[0] is the type of the item
            # if the item is a line or a curve, append all its points
            if item[0] in ("l", "c"):  # line or curve
                # append all the points
                _points.extend(item[1:])
            # If the item is a quad, append all its points
            elif item[0] == "qu":
                quad = item[1]
                # follow corners anti-clockwise
                _points.extend([quad.ul, quad.ll, quad.lr, quad.ur, quad.ul])
            # If the item is something else, it is a rectangle
            # rectangles come in two flavors.
            else:
                # starting point is always top-left
                rect = item[1]
                if item[-1] == 1:  # anti-clockwise (the standard)
                    _points.extend(
                        [rect.tl, rect.bl, rect.br, rect.tr, rect.tl]
                    )
                else:  # clockwise: area counts as negative
                    _points.extend(
                        [rect.tl, rect.tr, rect.br, rect.bl, rect.tl]
                    )

        # Once all the points have been added to the points' list,
        # compute area of the polygon
        area = _poly_area(_points)

        # less than threshold: graphic is significant
        if area < box_area:
            return True

    return False


def _refine_boxes(boxes: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    '''
    Join any rectangles with a pairwise non-empty overlap.
    Accepts and returns a list of Rect items.

    Note that rectangles that only "touch" each other (common point or edge)
    are not considered as overlapping.

    :param boxes: list[pymupdf.Rect]: list of Rectangles.
    '''
    # Return list
    new_rects: list[pymupdf.Rect] = []

    # make a copy of the list of all vector graphic rectangles
    # p_rects: list[pymupdf.Rect] = boxes[:]
    p_rects: deque[pymupdf.Rect] = deque(boxes)

    # Define a control sentinel
    repeat: bool

    # Walk the vector graphic rectangles, set the largest contiguous
    # rectangles as possible and append them to the new_rects return list
    while p_rects:  # the algorithm will empty this list

        # make a copy of first rectangle
        rect: pymupdf.Rect = +p_rects[0]

        # initialize condition
        repeat = True

        while repeat:
            repeat = False  # set false as default

            # Walk the vector graphic rectangles from back to front
            # and if any intersect with the first rectangle, enlarge the first
            # rectangle
            for i in range(len(p_rects) - 1, 0, -1):

                _current_rect: pymupdf.Rect = p_rects[i]

                # if the current rect intersect with the first rectangle
                if rect.intersects(_current_rect):
                    # enlarge first rect with this rectangle
                    rect |= _current_rect
                    # delete this rect
                    del p_rects[i]
                    # indicate we must try again (because the first
                    # rectangle is now larger)
                    repeat = True

        # We're now out of the 'repeat' 'while' => the first
        # graphic rectangle is complete,
        # append it to the return list
        # first rect now includes all overlaps
        # new_rects.append(rect)
        new_rects += [rect]

        # delete it from the list
        del p_rects[0]

    # Sort the new_rects list by left x and top y
    new_rects = sorted(set(new_rects), key=lambda rect: (rect.x0, rect.y0))

    # Return the sorted list
    return new_rects


def _accept_rect(
    path: dict[
        str,
        str
        | int
        | float
        | bool
        | tuple[int, int, int]
        | tuple[float, float, float]
        | list[tuple[str, pymupdf.Point, pymupdf.Point]]
        | pymupdf.Rect
        | None,
    ],
    tab_rects0: list[pymupdf.Rect],
    page_clip: pymupdf.Rect,
) -> bool:
    '''
    Only accept paths that:

    - are not contained in any table
    - are not out of the page clip
    - are not full page graphics

    '''
    _path_rect: pymupdf.Rect = path["rect"]

    return (
        not intersects_rects(_path_rect, tab_rects0)
        # Ignore out of page graphics
        and _path_rect in page_clip
        # Ignore full page graphics
        and _path_rect.width < page_clip.width
        and _path_rect.height < page_clip.height
    )


# @count_and_avg_timer(name='prep - vg_clusters_and_paths')
def make_lists_and_dict_of_vg_clusters_and_paths(
    page: pymupdf.Page,
    drawings: list[dict],
    tab_rects0: list[pymupdf.Rect],
    img_info: list[
        dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ]
    ],
) -> tuple[
    list[pymupdf.Rect],
    dict[int, pymupdf.Rect],
    list[
        dict[
            str,
            str
            | int
            | float
            | bool
            | tuple[int, int, int]
            | tuple[float, float, float]
            | list[tuple[str, pymupdf.Point, pymupdf.Point]]
            | pymupdf.Rect
            | None,
        ]
    ],
]:
    '''
    Make a list and dict of vector graphic clusters and a list of relevant
    paths.

    :param page: pymupdf.Page: the current page.

    :param drawings: list[dict]: the list of drawings for the current page.

    :param tab_rect0: list[pymupdf.Rect]: list of table rectangles on the page.

    :param img_info: list[
        dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ]
    ]: information about images in the pdf, among which its
        bbox, its index, its size, a transformation matrix,
        its colorspace, etc.

    '''
    # Define a page clip to ignore full page grapics
    page_clip: pymupdf.Rect = page.rect + (36, 36, -36, -36)

    # Select paths NOT contained in any table AND ignore full page graphics
    # ----------------------------------------------

    _page_paths: list[
        dict[
            str,
            str
            | int
            | float
            | bool
            | tuple[int, int, int]
            | tuple[float, float, float]
            | list[tuple[str, pymupdf.Point, pymupdf.Point]]
            | pymupdf.Rect
            | None,
        ]
    ] = [
        path
        for path in drawings
        if _accept_rect(
            path=path,
            tab_rects0=tab_rects0,
            page_clip=page_clip,
        )
    ]

    # Make list of vector graphics Rectangles
    # ----------------------------------------------

    # We also ignore vector graphics that only represent "text
    # emphasizing sugar".
    # walk through all vector graphics outside any table
    vg_clusters0: list[pymupdf.Rect] = [
        vg_graph_rect
        # vg_graph_rect is a Rect item wrapping line-art items
        # that are close enough to be considered forming a common
        # vector graphic
        for vg_graph_rect in _refine_boxes(
            # page.cluster_drawings() joins paths that live close
            # together into (vg cluster) Rectangles
            page.cluster_drawings(drawings=_page_paths)
        )
        if _is_significant(vg_graph_rect, _page_paths)
    ]

    # Filter out paths that are within the vector graphics Rectangles
    # ----------------------------------------------

    # keep only paths that are in the list of relevant graphics we just created
    actual_page_paths: list[
        dict[
            str,
            str
            | int
            | float
            | bool
            | tuple[int, int, int]
            | tuple[float, float, float]
            | list[tuple[str, pymupdf.Point, pymupdf.Point]]
            | pymupdf.Rect
            | None,
        ]
    ] = [
        path
        for path in _page_paths
        if _is_in_rects(path["rect"], vg_clusters0)
    ]

    # Add image's rectangles to the list of Rectangles of vector graphics
    # ----------------------------------------------

    # also add image rectangles to the list
    if img_info:
        vg_clusters0.extend([pymupdf.Rect(img["bbox"]) for img in img_info])

    # Harmonize into larger Rectangles
    # ----------------------------------------------

    # Because the vg_clusters0 list has been extended,
    # the vg in the vg_clusters_list may no longer be pairwise disjoint:
    # remove area overlaps by joining into larger rects
    vg_clusters0 = _refine_boxes(vg_clusters0)

    # Sort the Rectangles by top y and left x
    # ----------------------------------------------

    # Now sort them
    vg_clusters0.sort(key=sort_rect_key_by_bottom_y_left_x)

    # Create a numbered dict of vg_clusters
    # ----------------------------------------------

    vg_clusters: dict[int, pymupdf.Rect] = dict(enumerate(vg_clusters0))

    return (
        vg_clusters0,  # the list of Rect containing graphic clusters
        vg_clusters,  # the numbered dict of Rect containing graphic clusters
        actual_page_paths,  # the list of relevant paths on the page
    )
