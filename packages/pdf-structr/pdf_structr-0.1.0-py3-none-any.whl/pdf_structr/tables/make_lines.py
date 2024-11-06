# make_lines.py
'''
Submodule encapsulating part of the functions from
table_make_edges().
'''


from pymupdf import Point  # type: ignore

# from pdf_struct.mo_utils.timer import count_and_avg_timer

# -------------------------------------------------------------------
# make_line stack
# -------------------------------------------------------------------


# def is_parallel(p1, p2, snap_x, snap_y):
def is_parallel(p1: Point, p2: Point, snap_x: float, snap_y: float) -> bool:
    """Check if line is roughly axis-parallel."""
    if abs(p1.x - p2.x) <= snap_x or abs(p1.y - p2.y) <= snap_y:
        return True
    return False


def make_line(
    p,
    p1,
    p2,
    clip,
    snap_x,
    snap_y,
    page_height,
    page_number,
    doctop_basis,
):
    """
    Given 2 points, make a line dictionary of vertical or horizontal lines
    for table detection.

    Wrapped into a partial in `make_edges` function in module
    `table_make_edges`.
    Parameters snap_x, snap_y, page_height, page_number, doctop_basis
    are argumented into the partial.

    :param p: dict: a path dictionnary.
    :param p1: Point: a point.
    :param p2: Point: a second point.
    :param clip: Rect:
    :param snap_x: float:
    :param snap_y: float:
    :param page_height: float:
    :param page_number: int:
    :param doctop_basis: float:

    """
    # only accepting axis-parallel lines
    if not is_parallel(p1, p2, snap_x, snap_y):
        return {}
    # compute the extremal values
    x0 = min(p1.x, p2.x)
    x1 = max(p1.x, p2.x)
    y0 = min(p1.y, p2.y)
    y1 = max(p1.y, p2.y)

    # check for outside clip
    # exclude lines that would be outside the clip
    if x0 > clip.x1 or x1 < clip.x0 or y0 > clip.y1 or y1 < clip.y0:
        return {}

    # extend to clip boundaries
    if x0 < clip.x0:
        x0 = clip.x0  # adjust to clip boundary

    if x1 > clip.x1:
        x1 = clip.x1  # adjust to clip boundary

    if y0 < clip.y0:
        y0 = clip.y0  # adjust to clip boundary

    if y1 > clip.y1:
        y1 = clip.y1  # adjust to clip boundary

    width = x1 - x0  # from adjusted values
    height = y1 - y0  # from adjusted values
    if width == height == 0:
        return {}  # nothing left to deal with
    line_dict = {
        "x0": x0,
        "y0": page_height - y0,
        "x1": x1,
        "y1": page_height - y1,
        "width": width,
        "height": height,
        "pts": [(x0, y0), (x1, y1)],
        "linewidth": p["width"],
        "stroke": True,
        "fill": False,
        "evenodd": False,
        "stroking_color": p["color"] if p["color"] else p["fill"],
        "non_stroking_color": None,
        "object_type": "line",
        "page_number": page_number,
        "stroking_pattern": None,
        "non_stroking_pattern": None,
        "top": y0,
        "bottom": y1,
        "doctop": y0 + doctop_basis,
    }
    return line_dict
