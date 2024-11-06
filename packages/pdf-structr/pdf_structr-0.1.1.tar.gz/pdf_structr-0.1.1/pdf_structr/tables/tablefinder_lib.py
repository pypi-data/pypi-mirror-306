# tablefinder_lib.py
'''
Encapsulation of the functions of the TableFinder class
of pymupdf.
'''

import itertools
from operator import itemgetter

import pymupdf  # type: ignore
from pymupdf import (  # type: ignore
    EMPTY_RECT,
)

from pdf_structr.tables.settings import (
    DEFAULT_JOIN_TOLERANCE,
    DEFAULT_MIN_WORDS_HORIZONTAL,
    DEFAULT_MIN_WORDS_VERTICAL,
    DEFAULT_SNAP_TOLERANCE,
)
from pdf_structr.tables.table_funcs import (
    WordExtractor,
    bbox_getter,
    cluster_objects,
    line_to_edge,
    objects_to_bbox,
    white_spaces,
)

# -------------------------------------------
# TableFinder class __init__ support functions
# -------------------------------------------


def new_cells_to_tables(page, textpage, cells) -> list:
    """
    Given a list of bounding boxes (`cells`), return a list of tables that
    hold those cells most simply (and contiguously).

    This is a copy of the original `cells_to_tables` in pymupdf with
    an additional parameter `textpage`.


    """

    def bbox_to_corners(bbox) -> tuple:
        x0, top, x1, bottom = bbox
        return ((x0, top), (x0, bottom), (x1, top), (x1, bottom))

    # Make a copy of the list
    remaining_cells = list(cells)

    # Iterate through the cells found above, and assign them
    # to contiguous tables

    current_corners = set()
    current_cells: list = []

    tables = []
    while len(remaining_cells):
        initial_cell_count = len(current_cells)
        for cell in list(remaining_cells):
            cell_corners = bbox_to_corners(cell)
            # If we're just starting a table ...
            if len(current_cells) == 0:
                # ... immediately assign it to the empty group
                current_corners |= set(cell_corners)
                current_cells.append(cell)
                remaining_cells.remove(cell)
            else:
                # How many corners does this table share with the
                # current group?
                corner_count = sum(c in current_corners for c in cell_corners)

                # If touching on at least one corner...
                if corner_count > 0:
                    # ... assign it to the current group
                    current_corners |= set(cell_corners)
                    current_cells.append(cell)
                    remaining_cells.remove(cell)

        # If this iteration did not find any more cells to append...
        if len(current_cells) == initial_cell_count:
            # ... start a new cell group
            tables.append(list(current_cells))
            current_corners.clear()
            current_cells.clear()

    # Once we have exhausting the list of cells ...

    # ... and we have a cell group that has not been stored
    if len(current_cells):
        # ... store it.
        tables.append(list(current_cells))

    # PyMuPDF modification:
    # Remove tables without text or having only 1 column
    for i in range(len(tables) - 1, -1, -1):
        r = EMPTY_RECT()
        x1_vals = set()
        x0_vals = set()
        for c in tables[i]:
            r |= c
            x1_vals.add(c[2])
            x0_vals.add(c[0])
        if (
            len(x1_vals) < 2
            or len(x0_vals) < 2
            or white_spaces.issuperset(
                page.get_text('text', clip=r, textpage=textpage)
            )
        ):
            del tables[i]

    # Sort the tables top-to-bottom-left-to-right based on the value of the
    # topmost-and-then-leftmost coordinate of a table.
    tables.sort(key=lambda t: min((c[1], c[0]) for c in t))
    # _sorted = sorted(tables, key=lambda t: min((c[1], c[0]) for c in t))
    return tables


def edges_to_intersections(edges, x_tolerance=1, y_tolerance=1) -> dict:
    """
    Given a list of edges, return the points at which they intersect
    within `tolerance` pixels.
    """
    intersections: dict = {}
    v_edges, h_edges = [
        list(filter(lambda x: x["orientation"] == o, edges))
        for o in ("v", "h")
    ]
    for v in sorted(v_edges, key=itemgetter("x0", "top")):
        for h in sorted(h_edges, key=itemgetter("top", "x0")):
            if (
                (v["top"] <= (h["top"] + y_tolerance))
                and (v["bottom"] >= (h["top"] - y_tolerance))
                and (v["x0"] >= (h["x0"] - x_tolerance))
                and (v["x0"] <= (h["x1"] + x_tolerance))
            ):
                vertex = (v["x0"], h["top"])
                if vertex not in intersections:
                    intersections[vertex] = {"v": [], "h": []}
                intersections[vertex]["v"].append(v)
                intersections[vertex]["h"].append(h)
    return intersections


# --------------
# intersections_to_cells and subfunctions
# --------------


def obj_to_bbox(obj):
    """
    Return the bounding box for an object.
    """
    return bbox_getter(obj)


def edge_connects(intersections, p1, p2) -> bool:
    def edges_to_set(edges):
        return set(map(obj_to_bbox, edges))

    if p1[0] == p2[0]:
        common = edges_to_set(intersections[p1]["v"]).intersection(
            edges_to_set(intersections[p2]["v"])
        )
        if len(common):
            return True

    if p1[1] == p2[1]:
        common = edges_to_set(intersections[p1]["h"]).intersection(
            edges_to_set(intersections[p2]["h"])
        )
        if len(common):
            return True
    return False


def find_smallest_cell(
    intersections: dict[tuple[float, float], dict[str, list[dict]]],
    n_points: int,
    points: list[tuple[float, float]],
    i: int,
) -> None | tuple[float, float, float, float]:
    '''
    Produces a cell from the passed-in intersections.

    Returns None or a Tuple of coordinates (center point and bottom right)
        which are the coordinates of the cell.

    :intersections: dict[tuple[float, float], dict[str, list[dict]]]:
        the dict of intersections, where the keys are the tuples
        passed-in as points.

    :params n_points: the number of points.

    :params points: a list of tuple indicating the intersections.

    :param i: int: the current idx in the iteration on the points.
    '''
    if i == n_points - 1:
        return None

    pt = points[i]
    # pt is the current point, selected by index

    # Get all the points (intersections) that follow the current point
    new_start = i + 1
    rest = points[new_start:]

    # Get all the points directly below and directly right
    below = [x for x in rest if x[0] == pt[0]]
    right = [x for x in rest if x[1] == pt[1]]

    # Walk the intersections below this one
    for below_pt in below:

        # if the current point and the following points are not connected
        # with each other
        # -> continue
        if not edge_connects(intersections, pt, below_pt):
            continue

        # walk the intersections to the right of this one
        for right_pt in right:
            # if this point is not connected with an intersection to the right
            # -> continue
            if not edge_connects(intersections, pt, right_pt):
                continue

            # save to the bottom right coordinates in a variable
            bottom_right = (right_pt[0], below_pt[1])

            # try to connect the intersections
            if (
                (bottom_right in intersections)
                and edge_connects(intersections, bottom_right, right_pt)
                and edge_connects(intersections, bottom_right, below_pt)
            ):

                # return this point top-left and the identified bottom right
                return (pt[0], pt[1], bottom_right[0], bottom_right[1])

    return None


def intersections_to_cells(
    intersections: dict[tuple[float, float], dict[str, list[dict]]],
):
    """
    Given a list of points (`intersections`), return all rectangular "cells"
    that those points describe.

    `intersections` should be a dictionary with (x0, top) tuples as keys,
    and a list of edge objects as values. The edge objects should correspond
    to the edges that touch the intersection.

    As a matter of fact, `intersections` is just the list of path generated
    by edges_to_intersections, presented as a dict, where the keys are tuple
    of their key coordinates.
    """

    # get the keys of the intersection i.e. their coordinations
    points = sorted(intersections.keys())
    # points is a list of tuple i.e intersection coordinates
    # check how many of them
    n_points = len(points)

    cell_gen = (
        find_smallest_cell(intersections, n_points, points, i)
        for i in range(len(points))
    )

    # return a generator of cells, each cell being a 4-tuple of float
    return list(filter(None, cell_gen))


# -------------------------------------------
# TableFinder class support functions
# -------------------------------------------


def extract_words(chars: list, **kwargs) -> list:
    return WordExtractor(**kwargs).extract_words(chars)


def curve_to_edges(curve) -> list:
    point_pairs = zip(curve["pts"], curve["pts"][1:])
    return [
        {
            "object_type": "curve_edge",
            "x0": min(p0[0], p1[0]),
            "x1": max(p0[0], p1[0]),
            "top": min(p0[1], p1[1]),
            "doctop": min(p0[1], p1[1]) + (curve["doctop"] - curve["top"]),
            "bottom": max(p0[1], p1[1]),
            "width": abs(p0[0] - p1[0]),
            "height": abs(p0[1] - p1[1]),
            "orientation": (
                "v" if p0[0] == p1[0] else ("h" if p0[1] == p1[1] else None)
            ),
        }
        for p0, p1 in point_pairs
    ]


def rect_to_edges(rect) -> list:
    top, bottom, left, right = [dict(rect) for x in range(4)]
    top.update(
        {
            "object_type": "rect_edge",
            "height": 0,
            "y0": rect["y1"],
            "bottom": rect["top"],
            "orientation": "h",
        }
    )
    bottom.update(
        {
            "object_type": "rect_edge",
            "height": 0,
            "y1": rect["y0"],
            "top": rect["top"] + rect["height"],
            "doctop": rect["doctop"] + rect["height"],
            "orientation": "h",
        }
    )
    left.update(
        {
            "object_type": "rect_edge",
            "width": 0,
            "x1": rect["x0"],
            "orientation": "v",
        }
    )
    right.update(
        {
            "object_type": "rect_edge",
            "width": 0,
            "x0": rect["x1"],
            "orientation": "v",
        }
    )
    return [top, bottom, left, right]


def obj_to_edges(obj) -> list:
    t = obj["object_type"]
    if "_edge" in t:
        return [obj]
    elif t == "line":
        return [line_to_edge(obj)]
    else:
        return {"rect": rect_to_edges, "curve": curve_to_edges}[t](obj)


def resize_object(obj, key: str, value):
    assert key in ("x0", "x1", "top", "bottom")
    old_value = obj[key]
    diff = value - old_value
    new_items = [
        (key, value),
    ]
    if key == "x0":
        assert value <= obj["x1"]
        new_items.append(("width", obj["x1"] - value))
    elif key == "x1":
        assert value >= obj["x0"]
        new_items.append(("width", value - obj["x0"]))
    elif key == "top":
        assert value <= obj["bottom"]
        new_items.append(("doctop", obj["doctop"] + diff))
        new_items.append(("height", obj["height"] - diff))
        if "y1" in obj:
            new_items.append(("y1", obj["y1"] - diff))
    elif key == "bottom":
        assert value >= obj["top"]
        new_items.append(("height", obj["height"] + diff))
        if "y0" in obj:
            new_items.append(("y0", obj["y0"] - diff))
    return obj.__class__(tuple(obj.items()) + tuple(new_items))


def join_edge_group(edges, orientation: str, tolerance=DEFAULT_JOIN_TOLERANCE):
    """
    Given a list of edges along the same infinite line, join those that
    are within `tolerance` pixels of one another.
    """
    if orientation == "h":
        min_prop, max_prop = "x0", "x1"
    elif orientation == "v":
        min_prop, max_prop = "top", "bottom"
    else:
        raise ValueError("Orientation must be 'v' or 'h'")

    sorted_edges = sorted(edges, key=itemgetter(min_prop))
    joined = [sorted_edges[0]]
    for e in sorted_edges[1:]:
        last = joined[-1]
        if e[min_prop] <= (last[max_prop] + tolerance):
            if e[max_prop] > last[max_prop]:
                # Extend current edge to new extremity
                joined[-1] = resize_object(last, max_prop, e[max_prop])
        else:
            # Edge is separate from previous edges
            joined.append(e)

    return joined


def filter_edges(
    edges,
    orientation=None,
    edge_type=None,
    min_length=1,
) -> list:
    if orientation not in ("v", "h", None):
        raise ValueError("Orientation must be 'v' or 'h'")

    def test(e) -> bool:
        dim = "height" if e["orientation"] == "v" else "width"
        et_correct = (
            e["object_type"] == edge_type if edge_type is not None else True
        )
        orient_correct = orientation is None or e["orientation"] == orientation
        return bool(et_correct and orient_correct and (e[dim] >= min_length))

    return list(filter(test, edges))


def move_object(obj, axis: str, value):
    assert axis in ("h", "v")
    if axis == "h":
        new_items = [
            ("x0", obj["x0"] + value),
            ("x1", obj["x1"] + value),
        ]
    if axis == "v":
        new_items = [
            ("top", obj["top"] + value),
            ("bottom", obj["bottom"] + value),
        ]
        if "doctop" in obj:
            new_items += [("doctop", obj["doctop"] + value)]
        if "y0" in obj:
            new_items += [
                ("y0", obj["y0"] - value),
                ("y1", obj["y1"] - value),
            ]
    return obj.__class__(tuple(obj.items()) + tuple(new_items))


def snap_objects(objs, attr: str, tolerance) -> list:
    axis = {"x0": "h", "x1": "h", "top": "v", "bottom": "v"}[attr]
    list_objs = list(objs)
    clusters = cluster_objects(list_objs, itemgetter(attr), tolerance)
    avgs = [
        sum(map(itemgetter(attr), cluster)) / len(cluster)
        for cluster in clusters
    ]
    snapped_clusters = [
        [move_object(obj, axis, avg - obj[attr]) for obj in cluster]
        for cluster, avg in zip(clusters, avgs)
    ]
    return list(itertools.chain(*snapped_clusters))


def snap_edges(
    edges,
    x_tolerance=DEFAULT_SNAP_TOLERANCE,
    y_tolerance=DEFAULT_SNAP_TOLERANCE,
):
    """
    Given a list of edges, snap any within `tolerance` pixels of one another
    to their positional average.
    """
    by_orientation = {"v": [], "h": []}
    for e in edges:
        by_orientation[e["orientation"]].append(e)

    snapped_v = snap_objects(by_orientation["v"], "x0", x_tolerance)
    snapped_h = snap_objects(by_orientation["h"], "top", y_tolerance)
    return snapped_v + snapped_h


def merge_edges(
    edges,
    snap_x_tolerance,
    snap_y_tolerance,
    join_x_tolerance,
    join_y_tolerance,
):
    """
    Using the `snap_edges` and `join_edge_group` methods above,
    merge a list of edges into a more "seamless" list.
    """

    def get_group(edge):
        if edge["orientation"] == "h":
            return ("h", edge["top"])
        else:
            return ("v", edge["x0"])

    if snap_x_tolerance > 0 or snap_y_tolerance > 0:
        edges = snap_edges(edges, snap_x_tolerance, snap_y_tolerance)

    _sorted = sorted(edges, key=get_group)
    edge_groups = itertools.groupby(_sorted, key=get_group)
    edge_gen = (
        join_edge_group(
            items,
            k[0],
            (join_x_tolerance if k[0] == "h" else join_y_tolerance),
        )
        for k, items in edge_groups
    )
    edges = list(itertools.chain(*edge_gen))
    return edges


def get_bbox_overlap(a, b):
    a_left, a_top, a_right, a_bottom = a
    b_left, b_top, b_right, b_bottom = b
    o_left = max(a_left, b_left)
    o_right = min(a_right, b_right)
    o_bottom = min(a_bottom, b_bottom)
    o_top = max(a_top, b_top)
    o_width = o_right - o_left
    o_height = o_bottom - o_top
    if o_height >= 0 and o_width >= 0 and o_height + o_width > 0:
        return (o_left, o_top, o_right, o_bottom)
    else:
        return None


def bbox_to_rect(bbox) -> dict:
    """
    Return the rectangle (i.e a dict with keys "x0", "top", "x1",
    "bottom") for an object.
    """
    return {"x0": bbox[0], "top": bbox[1], "x1": bbox[2], "bottom": bbox[3]}


def words_to_edges_v(words, word_threshold: int = DEFAULT_MIN_WORDS_VERTICAL):
    """
    Find (imaginary) vertical lines that connect the left, right, or
    center of at least `word_threshold` words.
    """
    # Find words that share the same left, right, or centerpoints
    by_x0 = cluster_objects(words, itemgetter("x0"), 1)
    by_x1 = cluster_objects(words, itemgetter("x1"), 1)

    def get_center(word):
        return float(word["x0"] + word["x1"]) / 2

    by_center = cluster_objects(words, get_center, 1)
    clusters = by_x0 + by_x1 + by_center

    # Find the points that align with the most words
    sorted_clusters = sorted(clusters, key=lambda x: -len(x))
    large_clusters = filter(
        lambda x: len(x) >= word_threshold, sorted_clusters
    )

    # For each of those points, find the bboxes fitting all matching words
    bboxes = list(map(objects_to_bbox, large_clusters))

    # Iterate through those bboxes, condensing overlapping bboxes
    condensed_bboxes: list = []
    for bbox in bboxes:
        overlap = any(get_bbox_overlap(bbox, c) for c in condensed_bboxes)
        if not overlap:
            condensed_bboxes.append(bbox)

    if len(condensed_bboxes) == 0:
        return []

    condensed_rects = map(bbox_to_rect, condensed_bboxes)
    sorted_rects = sorted(condensed_rects, key=itemgetter("x0"))

    max_x1 = max(map(itemgetter("x1"), sorted_rects))
    min_top = min(map(itemgetter("top"), sorted_rects))
    max_bottom = max(map(itemgetter("bottom"), sorted_rects))

    return [
        {
            "x0": b["x0"],
            "x1": b["x0"],
            "top": min_top,
            "bottom": max_bottom,
            "height": max_bottom - min_top,
            "orientation": "v",
        }
        for b in sorted_rects
    ] + [
        {
            "x0": max_x1,
            "x1": max_x1,
            "top": min_top,
            "bottom": max_bottom,
            "height": max_bottom - min_top,
            "orientation": "v",
        }
    ]


def objects_to_rect(objects) -> dict:
    """
    Given an iterable of objects, return the smallest rectangle (i.e. a
    dict with "x0", "top", "x1", and "bottom" keys) that contains them
    all.
    """
    return bbox_to_rect(objects_to_bbox(objects))


def words_to_edges_h(
    words, word_threshold: int = DEFAULT_MIN_WORDS_HORIZONTAL
):
    """
    Find (imaginary) horizontal lines that connect the tops
    of at least `word_threshold` words.
    """
    by_top = cluster_objects(words, itemgetter("top"), 1)
    large_clusters = filter(lambda x: len(x) >= word_threshold, by_top)
    rects = list(map(objects_to_rect, large_clusters))
    if len(rects) == 0:
        return []
    min_x0 = min(map(itemgetter("x0"), rects))
    max_x1 = max(map(itemgetter("x1"), rects))

    edges = []
    for r in rects:
        edges += [
            # Top of text
            {
                "x0": min_x0,
                "x1": max_x1,
                "top": r["top"],
                "bottom": r["top"],
                "width": max_x1 - min_x0,
                "orientation": "h",
            },
            # For each detected row, we also add the 'bottom' line.  This will
            # generate extra edges, (some will be redundant with the next row
            # 'top' line), but this catches the last row of every table.
            {
                "x0": min_x0,
                "x1": max_x1,
                "top": r["bottom"],
                "bottom": r["bottom"],
                "width": max_x1 - min_x0,
                "orientation": "h",
            },
        ]

    return edges


# -------------------------------------------
# TableFinder class functions
# -------------------------------------------


def get_edges_tf(
    page: pymupdf.Page,
    settings,
    chars: list[dict],
    edges: list[dict],
) -> list:
    '''
    Function that extract what are to be likely edges for tables from:
    - the previously extracted edges list (in strategy 'lines'
    and 'lines_strict') OR
    - by building them from an analysis of the word positions in the document
    (in strategy 'text') OR
    - by building them out of the passed in list of lines coordinates in
    case of strategy 'explicit' (or if any lines have been passed in via
    arguments to parameters 'horizontal_lines' or 'vertical_lines').

    Code extracted from `get_edges()` method of the TableFinder.

    :param page: pymupdf.Page: the current pymupdf.Page.

    :param settings: TableSettings: a TableSettings object, which eventually
        contains 'horizontal_lines' or 'vertical_lines' and definitely
        contains a table extraction strategy.

    # NOTE: make param chars | None. It is only required for the
    # text strategy. We might want to be able to skip it altogether.

    :param chars: list[dict]: the list of characters' dict, made out of
        the page characters extracted via function `make_chars` in module
        `table_make_chars`.

    :param edges: list[dict]: the list of edges' dict, made by function
        `make_edges` in module `table_make_edges`.

    '''
    # settings = self.settings

    for orientation in ["vertical", "horizontal"]:
        strategy = getattr(settings, orientation + "_strategy")
        if strategy == "explicit":
            lines = getattr(settings, "explicit_" + orientation + "_lines")
            if len(lines) < 2:
                raise ValueError(
                    f"If {orientation}_strategy == 'explicit', "
                    f"explicit_{orientation}_lines "
                    f"must be specified as a list/tuple of two or more "
                    f"floats/ints."
                )

    v_strat = settings.vertical_strategy
    h_strat = settings.horizontal_strategy

    # strategy 'text': extract text
    if v_strat == "text" or h_strat == "text":
        words = extract_words(chars, **(settings.text_settings or {}))
    else:
        words = []

    # ----------------------------------------
    # Find vertical lines
    # ----------------------------------------

    # v_explicit: convert provided each explicit vertical lines to a dict
    v_explicit = []
    for desc in settings.explicit_vertical_lines or []:
        if isinstance(desc, dict):
            for e in obj_to_edges(desc):
                if e["orientation"] == "v":
                    v_explicit.append(e)
        else:
            v_explicit.append(
                {
                    "x0": desc,
                    "x1": desc,
                    "top": page.rect[1],
                    "bottom": page.rect[3],
                    "height": page.rect[3] - page.rect[1],
                    "orientation": "v",
                }
            )

    # v_base: vertical line base
    if v_strat == "lines":
        v_base = filter_edges(edges, "v")
    elif v_strat == "lines_strict":
        v_base = filter_edges(edges, "v", edge_type="line")
    # vertical_strategy: 'text'
    elif v_strat == "text":
        v_base = words_to_edges_v(
            words, word_threshold=settings.min_words_vertical
        )
    # vertical_strategy: 'explicit': only use v_explicit
    elif v_strat == "explicit":
        v_base = []
    else:
        v_base = []

    v = v_base + v_explicit
    # now we have a base of vertical lines as dict

    # ----------------------------------------
    # Find horizontal lines
    # ----------------------------------------

    # h_explicit: convert provided each explicit horizontal lines to a dict
    h_explicit = []
    for desc in settings.explicit_horizontal_lines or []:
        if isinstance(desc, dict):
            for e in obj_to_edges(desc):
                if e["orientation"] == "h":
                    h_explicit.append(e)
        else:
            h_explicit.append(
                {
                    "x0": page.rect[0],
                    "x1": page.rect[2],
                    "width": page.rect[2] - page.rect[0],
                    "top": desc,
                    "bottom": desc,
                    "orientation": "h",
                }
            )

    # h_base: horizontal line base
    if h_strat == "lines":
        h_base = filter_edges(edges, "h")
    elif h_strat == "lines_strict":
        h_base = filter_edges(edges, "h", edge_type="line")
    # horizontal_strategy: 'text'
    elif h_strat == "text":
        h_base = words_to_edges_h(
            words, word_threshold=settings.min_words_horizontal
        )
    # horizontal_strategy: 'explicit': only use h_explicit
    elif h_strat == "explicit":
        h_base = []
    else:
        h_base = []

    h = h_base + h_explicit

    # ----------------------------------------
    # Combine the lists, merge the edges and filter them
    # ----------------------------------------

    # Combine the lists
    edges = list(v) + list(h)

    edges = merge_edges(
        edges,
        snap_x_tolerance=settings.snap_x_tolerance,
        snap_y_tolerance=settings.snap_y_tolerance,
        join_x_tolerance=settings.join_x_tolerance,
        join_y_tolerance=settings.join_y_tolerance,
    )

    return filter_edges(edges, min_length=settings.edge_min_length)
