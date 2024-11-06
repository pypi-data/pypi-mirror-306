# make_edges.py
'''
Encapsulation of formerly nested functions into make_edges().
'''

from functools import partial

from pymupdf import (  # type: ignore
    Page,
    Point,
    Rect,
)

from pdf_structr.tables.make_lines import make_line
from pdf_structr.tables.settings import (
    TableSettings,
)
from pdf_structr.tables.table_funcs import (
    line_to_edge,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


# -------------------------------------------------------------------
# make_edges stack
# -------------------------------------------------------------------


def _make_edges_with_path(
    edges,
    path,
    make_line_partial,
    min_length,
) -> None:
    '''

    :param path: the path with which we try to make an edge.

    :param make_line_partial: the make_line_partial, wrapping make_line
        with preconfigured settings for clip, snap_x, snap_y, page_height,
        page_number and doctop_basis.

    :param min_length: the minimum length for a path to be taken into
        consideration.
    '''
    items = path["items"]  # items in this path

    # if 'closePath', add a line from last to first point
    if path["closePath"] and items[0][0] == "l" and items[-1][0] == "l":
        items.append(("l", items[-1][2], items[0][1]))

    for i in items:
        if i[0] not in ("l", "re", "qu"):
            continue  # ignore anything else

        if i[0] == "l":  # a line
            p1, p2 = i[1:]
            line_dict = make_line_partial(path, p1, p2)
            if line_dict:
                edges.append(line_to_edge(line_dict))

        elif i[0] == "re":
            # A rectangle: decompose into 4 lines, but filter out
            # the ones that simulate a line
            rect = i[1].normalize()  # normalize the rectangle

            if (
                rect.width <= min_length and rect.width < rect.height
            ):  # simulates a vertical line
                x = abs(rect.x1 + rect.x0) / 2  # take middle value for x
                p1 = Point(x, rect.y0)
                p2 = Point(x, rect.y1)
                line_dict = make_line_partial(path, p1, p2)
                if line_dict:
                    edges.append(line_to_edge(line_dict))
                continue

            if (
                rect.height <= min_length and rect.height < rect.width
            ):  # simulates a horizontal line
                y = abs(rect.y1 + rect.y0) / 2  # take middle value for y
                p1 = Point(rect.x0, y)
                p2 = Point(rect.x1, y)
                line_dict = make_line_partial(path, p1, p2)
                if line_dict:
                    edges.append(line_to_edge(line_dict))
                continue

            line_dict = make_line_partial(path, rect.tl, rect.bl)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, rect.bl, rect.br)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, rect.br, rect.tr)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, rect.tr, rect.tl)
            if line_dict:
                edges.append(line_to_edge(line_dict))

        else:  # must be a quad
            # we convert it into (up to) 4 lines
            ul, ur, ll, lr = i[1]

            line_dict = make_line_partial(path, ul, ll)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, ll, lr)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, lr, ur)
            if line_dict:
                edges.append(line_to_edge(line_dict))

            line_dict = make_line_partial(path, ur, ul)
            if line_dict:
                edges.append(line_to_edge(line_dict))


def _make_edges_with_bbox(
    edges,
    make_line_partial_preconfd_path,
    bbox,
) -> None:
    '''

    :param make_line_partial: the make_line_partial, wrapping make_line
        with preconfigured settings for clip, snap_x, snap_y, page_height,
        page_number and doctop_basis.

    :param bbox: the bbox with which we are going to try and make some edges.
    '''
    line_dict = make_line_partial_preconfd_path(p1=bbox.tl, p2=bbox.tr)
    if line_dict:
        edges.append(line_to_edge(line_dict))

    line_dict = make_line_partial_preconfd_path(p1=bbox.bl, p2=bbox.br)
    if line_dict:
        edges.append(line_to_edge(line_dict))

    line_dict = make_line_partial_preconfd_path(p1=bbox.tl, p2=bbox.bl)
    if line_dict:
        edges.append(line_to_edge(line_dict))

    line_dict = make_line_partial_preconfd_path(p1=bbox.tr, p2=bbox.br)
    if line_dict:
        edges.append(line_to_edge(line_dict))


# from pdf_struct.mo_utils.timer import count_and_avg_timer


# @count_and_avg_timer(name='prep - make_edges')
def make_edges(
    page: Page,
    clean_graphics_partial: partial,
    clip: Rect | None = None,
    tset: TableSettings | None = None,
    add_lines: list[tuple[Point, Point]] | None = None,
) -> list[dict]:
    '''
    Detects edges for the columns, rows and borders of tables.

    Only applicable in strategies 'lines' and 'lines_strict'.

    At the end of the parsing, the edges shall comprise:
    - the detected edges for the column and row edges
    - the detected edges for the table borders
    - the lines passed-in as argument to parameter 'add_lines'

    :returns: a list of edges dict.

    :param page: the current page.
    :param clip=None: any passed-in clip.
    :param tset=None: the TableSettings object.
    :param add_lines=None: a list of tuple of Points, representing
        additional lines hint, passed as argument to `find_tables`.
    '''

    # ---------------------------------------
    # Configure
    # ---------------------------------------
    edges: list[dict] = []

    snap_x: float = tset.snap_x_tolerance  # type: ignore
    snap_y: float = tset.snap_y_tolerance  # type: ignore
    min_length: float = tset.edge_min_length  # type: ignore
    page_height: float = page.rect.height
    doctop_basis: float = page.number * page_height
    page_number: int = page.number + 1
    prect: Rect = page.rect
    if page.rotation in (90, 270):
        w, h = prect.br
        prect = Rect(0, 0, h, w)
    if clip is not None:
        clip = Rect(clip)
    else:
        clip = prect

    # ---------------------------------------
    # Clean graphics
    # ---------------------------------------

    # NOTE: very heavy
    # Timing: 8.980 milliseconds
    # NOTE: `clean_graphics` formerly nested function now living
    # in table_make_edges
    # bboxes, paths = clean_graphics(
    #     page=page,
    #     drawings=drawings,
    #     textpage=textpage,
    #     lines_strict=lines_strict,
    #     snap_x=snap_x,
    #     snap_y=snap_y,
    # )
    bboxes, paths = clean_graphics_partial(
        snap_x=snap_x,
        snap_y=snap_y,
    )
    # We now have bboxes (as Rect) that should represent table bboxes
    # and the filtered paths from which we may induce some columns and
    # rows edges

    # ---------------------------------------
    # Make columns and rows edges
    # ---------------------------------------

    # Make a partial with make_line
    # NOTE: `make_line` used to be a nested function, now living
    # in table_make_edges
    _make_line_partial = partial(
        make_line,
        clip=clip,
        snap_x=snap_x,
        snap_y=snap_y,
        page_height=page_height,
        page_number=page_number,
        doctop_basis=doctop_basis,
    )

    # Walk the paths and try to make column and rows edges
    for p in paths:
        _make_edges_with_path(
            edges=edges,
            path=p,
            make_line_partial=_make_line_partial,
            min_length=min_length,
        )

    # ---------------------------------------
    # Make borders
    # ---------------------------------------

    path = {"color": (0, 0, 0), "fill": None, "width": 1}

    # Make a subpartial for make line with the path that has
    # just been defined
    _make_line_partial_preconfd_path = partial(
        _make_line_partial,
        p=path,
    )

    # Walk the bboxes and make border lines
    for bbox in bboxes:  # add the border lines for all enveloping bboxes
        _make_edges_with_bbox(
            edges=edges,
            make_line_partial_preconfd_path=_make_line_partial_preconfd_path,
            bbox=bbox,
        )

    # ---------------------------------------
    # Take into account any passed-in 'add_lines' arguments
    # ---------------------------------------

    if add_lines is not None:  # add user-specified lines
        assert isinstance(add_lines, (tuple, list))
    else:
        add_lines = []
    for p1, p2 in add_lines:
        p1 = Point(p1)
        p2 = Point(p2)
        line_dict = _make_line_partial_preconfd_path(p1=p1, p2=p2)
        if line_dict:
            edges.append(line_to_edge(line_dict))

    # ---------------------------------------
    # Return the edges
    # ---------------------------------------

    return edges
