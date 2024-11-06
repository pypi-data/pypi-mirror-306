# classes.py
'''
'''

import inspect
import itertools
from collections.abc import Sequence
from functools import partial
from operator import itemgetter
from typing import Any, Callable, Generator, Iterator

from pymupdf import (  # type: ignore
    Page,
    TextPage,
    message,
)

from pdf_structr.tables.header import (
    TableHeader,
    new_get_table_header,
)
from pdf_structr.tables.settings import (
    DEFAULT_Y_TOLERANCE,
    TableSettings,
)
from pdf_structr.tables.table_funcs import (
    TextMap,
    WordExtractor,
    WordMap,
    cluster_objects,
)
from pdf_structr.tables.table_lib import (
    extract_table_to_markdown_generic,
)
from pdf_structr.tables.tablefinder_lib import (
    edges_to_intersections,
    get_edges_tf,
    intersections_to_cells,
    new_cells_to_tables,
)


class CellGroup:
    def __init__(self, cells):
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), filter(None, cells))),
            min(map(itemgetter(1), filter(None, cells))),
            max(map(itemgetter(2), filter(None, cells))),
            max(map(itemgetter(3), filter(None, cells))),
        )


class TableRow(CellGroup):
    pass


class NewTable:
    def __init__(self, page: Page, textpage: TextPage, cells, chars, blocks):
        self.page = page
        self.textpage = textpage
        self.chars = chars
        self.cells = cells
        self.header = self._get_header(blocks=blocks)  # PyMuPDF extension

    @property
    def bbox(self):
        c = self.cells
        return (
            min(map(itemgetter(0), c)),
            min(map(itemgetter(1), c)),
            max(map(itemgetter(2), c)),
            max(map(itemgetter(3), c)),
        )

    @property
    def rows(self) -> list:
        _sorted: list[tuple[float, float, float, float]] = sorted(
            self.cells, key=itemgetter(1, 0)
        )
        _xs: list[float] = sorted(set(map(itemgetter(0), self.cells)))
        _rows: list[TableRow] = [
            _compute_table_row(_row_cells, _xs)
            for _, _row_cells in itertools.groupby(_sorted, itemgetter(1))
        ]
        return _rows

    @property
    def row_count(self) -> int:  # PyMuPDF extension
        return len(self.rows)

    @property
    def col_count(self) -> int:  # PyMuPDF extension
        return max([len(_row.cells) for _row in self.rows])

    @property
    def max_col_inner_coords(self) -> list[float]:
        '''
        Returns the inner coordinates of the columns' edges.
        The outer coordinates are the table's borders.
        '''
        for _row in self.rows:
            if all(_cell is not None for _cell in _row.cells):
                break

        return [_cell[2] for _cell in _row.cells][:-1]

    def extract(self, **kwargs) -> list:

        return convert_table_rows_to_list(
            chars=self.chars,
            rows=self.rows,
            kwargs=kwargs,
        )

    def to_markdown(self, clean=True):
        """Output table content as a string in Github-markdown format.

        If clean is true, markdown syntax is removed from cell content."""

        _extract_func = partial(
            convert_table_rows_to_list,
            chars=self.chars,
            rows=self.rows,
        )

        return extract_table_to_markdown(
            header=self.header,
            col_count=self.col_count,
            extract_method=_extract_func,
            clean=clean,
        )

    def to_pandas(self, **kwargs):
        """Return a pandas DataFrame version of the table."""

        _extract_func = partial(
            convert_table_rows_to_list,
            chars=self.chars,
            rows=self.rows,
            kwargs=kwargs,
        )

        return extract_table_to_pandas(
            header=self.header,
            extract_method=_extract_func,
        )

    def _get_header(self, blocks, y_tolerance=3):
        """Identify the table header.

        *** PyMuPDF extension. ***

        Starting from the first line above the table upwards, check if it
        qualifies to be part of the table header.

        Criteria include:
        * A one-line table never has an extra header.
        * Column borders must not intersect any word. If this happens, all
          text of this line and above of it is ignored.
        * No excess inter-line distance: If a line further up has a distance
          of more than 1.5 times of its font size, it will be ignored and
          all lines above of it.
        * Must have same text properties.
        * Starting with the top table line, a bold text property cannot change
          back to non-bold.

        If not all criteria are met (or there is no text above the table),
        the first table row is assumed to be the header.

        :param blocks: list[dict]: the previously extracted blocks.

        """

        return new_get_table_header(
            page=self.page,
            textpage=self.textpage,
            table_rows=self.rows,
            table_cols_inner_coords=self.max_col_inner_coords,
            extract_method=self.extract,
            table_bbox=self.bbox,
            blocks=blocks,
            y_tolerance=y_tolerance,
        )


class NewTableFinder:
    """
    Derived from TableFinder

    Passing chars and edges as parameters and making them attributes.

    Given a PDF page, find plausible table structures.

    Largely borrowed from Anssi Nurminen's master's thesis:
    http://dspace.cc.tut.fi/dpub/bitstream/handle/123456789/21520/Nurminen.pdf?sequence=3

    ... and inspired by Tabula:
    https://github.com/tabulapdf/tabula-extractor/issues/16
    """

    def __init__(self, page, textpage, chars, edges, blocks, settings=None):

        # Make the chars and edges attributes of the instance
        # self.input_edges = edges
        self.edges = edges
        self.chars = chars
        self.textpage = textpage

        # NOTE: the following code is the same as parent TableFinder
        # except for the self.tables at the end
        self.page = page
        # if the TableFinder is called from the `find_tables`
        # function, the function has already applied
        # `TableSettings.resolve(settings)` => no need to do it again
        if hasattr(page, 'table_settings'):
            self.settings = page.table_settings
        else:
            self.settings = TableSettings.resolve(settings)

        # Get the edges of the tables
        self.edges = self.get_edges()

        # Get the intersections between the edge: this is how we identify
        # the tables
        self.intersections = edges_to_intersections(
            self.edges,
            self.settings.intersection_x_tolerance,
            self.settings.intersection_y_tolerance,
        )

        # Convert the intersections to cells
        self.cells = intersections_to_cells(self.intersections)

        # Convert the cells to tables
        # NOTE: a bit heavy
        # Timing: 2.497 milliseconds
        self.tables = [
            # NOTE: in NewTableFinder, we call NewTable instead of Table
            NewTable(
                self.page,
                self.textpage,
                cell_group,
                self.chars,
                blocks,
            )
            for cell_group in new_cells_to_tables(
                self.page, self.textpage, self.cells
            )
        ]

    def get_edges(self) -> list:

        return get_edges_tf(
            page=self.page,
            settings=self.settings,
            chars=self.chars,
            # edges=self.input_edges,
            edges=self.edges,
        )

    def __getitem__(self, i):
        tcount = len(self.tables)
        if i >= tcount:
            raise IndexError("table not on page")
        while i < 0:
            i += tcount
        return self.tables[i]


"""
Start of PyMuPDF interface code.
The following functions are executed when "page.find_tables()" is called.

* make_chars: Fills the CHARS list with text character information extracted
              via "rawdict" text extraction. Items in CHARS are formatted
              as expected by the table code.
* make_edges: Fills the EDGES list with vector graphic information extracted
              via "get_drawings". Items in EDGES are formatted as expected
              by the table code.

The lists CHARS and EDGES are used to replace respective document access
of pdfplumber or, respectively pdfminer.
The table code has been modified to use these lists instead of accessing
page information themselves.
"""

# -------------------------------------------
# Table class support functions
# -------------------------------------------


def _compute_table_row(
    row_cells: Iterator[tuple[float, float, float, float]],
    xs: list[float],
) -> TableRow:
    # make a dict of the cells' bboxes, with x0 as the key
    # the row_cells bbox as value => xdict
    _xdict: dict[float, tuple[float, float, float, float]] = {
        _cell[0]: _cell for _cell in row_cells
    }
    # make a row
    return TableRow([_xdict.get(x) for x in xs])


def to_list(collection) -> list:
    if isinstance(collection, list):
        return collection
    elif isinstance(collection, Sequence):
        return list(collection)
    elif hasattr(collection, "to_dict"):
        res = collection.to_dict("records")  # pragma: nocover
        return res
    else:
        return list(collection)


WORD_EXTRACTOR_KWARGS = inspect.signature(WordExtractor).parameters.keys()
TEXTMAP_KWARGS = inspect.signature(WordMap.to_textmap).parameters.keys()


def chars_to_textmap(chars: list, **kwargs) -> TextMap:
    kwargs.update({"presorted": True})

    extractor = WordExtractor(
        **{k: kwargs[k] for k in WORD_EXTRACTOR_KWARGS if k in kwargs}
    )
    wordmap = extractor.extract_wordmap(chars)
    textmap = wordmap.to_textmap(
        **{k: kwargs[k] for k in TEXTMAP_KWARGS if k in kwargs}
    )

    return textmap


def extract_text(chars: list[dict], **kwargs) -> str:
    chars = to_list(chars)
    if len(chars) == 0:
        return ""

    if kwargs.get("layout"):
        return chars_to_textmap(chars, **kwargs).as_string
    else:
        y_tolerance = kwargs.get("y_tolerance", DEFAULT_Y_TOLERANCE)
        extractor = WordExtractor(
            **{k: kwargs[k] for k in WORD_EXTRACTOR_KWARGS if k in kwargs}
        )
        words = extractor.extract_words(chars)
        if words:
            rotation = words[0][
                "rotation"
            ]  # rotation cannot change within a cell
        else:
            rotation = 0

        if rotation == 90:
            words.sort(key=lambda w: (w["x1"], -w["top"]))
            lines = " ".join([w["text"] for w in words])
        elif rotation == 270:
            words.sort(key=lambda w: (-w["x1"], w["top"]))
            lines = " ".join([w["text"] for w in words])
        else:
            lines = cluster_objects(  # type: ignore
                words, itemgetter("doctop"), y_tolerance
            )
            lines = "\n".join(
                " ".join(word["text"] for word in line)  # type: ignore
                for line in lines
            )
            if rotation == 180:  # needs extra treatment
                lines = "".join(
                    [(c if c != "\n" else " ") for c in reversed(lines)]
                )

        return lines


# -------------------------------------------
# Table class functions
# -------------------------------------------


def char_in_bbox(
    char: dict,
    bbox_x0: float,
    bbox_top: float,
    bbox_x1: float,
    bbox_bottom: float,
    # bbox: tuple[float, float, float, float]
) -> bool:
    '''
    Test whether a character is in the bbox.

    Formerly nested function in `convert_table_rows_to_list`
    (method `extract()` of `Table` class).

    :param char: dict: a character dict as made out of the page
        characters extracted via function `make_chars` in module
        `table_make_chars`.

    :param bbox_x0: float: the bbox tuple[0]

    :param bbox_top: float: the bbox tuple[1]

    :param bbox_x1: float: the bbox tuple[2]

    :param bbox_bottom: float: the bbox tuple[3]
    '''
    # vertical middle coordinate (y coord) for the char
    v_mid: float = (char["top"] + char["bottom"]) / 2
    # horizontal middle coordinate (x coord) for the char
    h_mid: float = (char["x0"] + char["x1"]) / 2
    # x0, top, x1, bottom = bbox

    return bool(
        # is horizontally in the bbox?
        (h_mid >= bbox_x0)
        and (h_mid < bbox_x1)
        # is vertically in the bbox?
        and (v_mid >= bbox_top)
        and (v_mid < bbox_bottom)
    )


def _get_cell_text_if_not_none(
    cell: tuple[float, float, float, float], row_chars: list[dict], **kwargs
) -> str:
    '''
    For a given cell, extracts text from the `row_chars` list of
    characters dict for the row in which the cell is, if cell is not None.

    :param cell: tuple[float, float, float, float]: a bbox tuple for
        a given cell.

    :param row_chars: list[dict]: a list of characters' dicts, made out of
        the page characters extracted via function `make_chars` in module
        `table_make_chars`, filtered for a given row.

    '''
    # Make a partial for faster access to char_in_bbox
    _char_in_cell_bbox_partial = partial(
        char_in_bbox,
        bbox_x0=cell[0],
        bbox_top=cell[1],
        bbox_x1=cell[2],
        bbox_bottom=cell[3],
    )

    cell_chars: list[dict] = [
        char for char in row_chars if _char_in_cell_bbox_partial(char)
    ]

    if len(cell_chars):
        kwargs["x_shift"] = cell[0]
        kwargs["y_shift"] = cell[1]
        if "layout" in kwargs:
            kwargs["layout_width"] = cell[2] - cell[0]
            kwargs["layout_height"] = cell[3] - cell[1]

        return extract_text(cell_chars, **kwargs)

    return ""


def _get_cell_text(
    cell: tuple[float, float, float, float] | None,
    row_chars: list[dict],
    **kwargs,
) -> str | None:
    '''
    For a given cell, extracts text from the `row_chars` list of
    characters dict for the row in which the cell is.

    :param cell: tuple[float, float, float, float] | None: a bbox tuple for
        a given cell or None.

    :param row_chars: list[dict]: a list of characters' dicts, made out of
        the page characters extracted via function `make_chars` in module
        `table_make_chars`, filtered for a given row.

    '''
    if cell is None:

        return None

    return _get_cell_text_if_not_none(
        cell=cell,
        row_chars=row_chars,
        kwargs=kwargs,
    )


def _get_row_list_of_str(
    row: TableRow,
    chars: list[dict],
    **kwargs,
) -> Generator[str | None, Any, Any]:
    '''
    For each row, make a list of string, where each string is the text of
    one of its cells.

    :param chars: list[dict]: the list of characters' dict, made out of
        the page characters extracted via function `make_chars` in module
        `table_make_chars`.

    :param row: TableRow: a TableRow from a pymupdf.Table instance.

    '''
    # Make a partial for faster access to char_in_bbox
    _char_in_row_bbox_partial = partial(
        char_in_bbox,
        bbox_x0=row.bbox[0],
        bbox_top=row.bbox[1],
        bbox_x1=row.bbox[2],
        bbox_bottom=row.bbox[3],
    )

    # Filter the character dicts that are within the row's bbox
    row_chars: list[dict] = [
        char for char in chars if _char_in_row_bbox_partial(char)
    ]

    # make a list of string, where each string is the text
    # of one of the cell in the row
    return (
        _get_cell_text(
            cell=cell,
            row_chars=row_chars,
            kwargs=kwargs,
        )
        # cell is a bbox tuple
        for cell in row.cells
    )


def convert_table_rows_to_list(
    chars: list[dict], rows: list[TableRow], **kwargs
) -> list[Generator[str | None, Any, Any]]:
    '''
    Function that converts the rows of a Table and the page's CHARS list
    into a list of list of string.

    Adapted from the code of method `extract()` of `Table` class of pymupdf.

    :param chars: list[dict]: the list of characters' dict, made out of
        the page characters extracted via function `make_chars` in module
        `table_make_chars`.

    :param rows: list[TableRow]: the list of TableRows from a NewTable
        instance.

    NOTE: determine when a **kwargs may be passed and what may be
    in there.
    '''
    _get_row_list_of_str_partial: partial = partial(
        _get_row_list_of_str,
        chars=chars,
        kwargs=kwargs,
    )

    return [_get_row_list_of_str_partial(row) for row in rows]


def extract_table_to_markdown(
    header: TableHeader,
    col_count: int,
    extract_method: Callable,
    clean: bool,
) -> str:
    """
    Output table content as a string in Github-markdown format.

    :param header: TableHeader: a pymupdf.Table header instance.

    :param col_count: int: the number of columns in the table.

    :param extract_method: Callable: a callable that extract the table
        to a list of list of strings.

    :param clean: bool:  If clean is true, markdown syntax is removed
        from cell content.
    """
    return extract_table_to_markdown_generic(
        header_names=header.names,
        header_external_print_first_row=header.external,
        table_rows=extract_method(),
        col_count=col_count,
        clean=clean,
    )


def extract_table_to_pandas(
    header,
    extract_method,
    # **kwargs
):
    """Return a pandas DataFrame version of the table."""
    try:
        import pandas as pd
    except ModuleNotFoundError:
        message("Package 'pandas' is not installed")
        raise

    pd_dict = {}
    extract = extract_method()
    hdr = header
    names = header.names
    hdr_len = len(names)
    # ensure uniqueness of column names
    for i in range(hdr_len):
        name = names[i]
        if not name:
            names[i] = f"Col{i}"
    if hdr_len != len(set(names)):
        for i in range(hdr_len):
            name = names[i]
            if name != f"Col{i}":
                names[i] = f"{i}-{name}"

    if not hdr.external:  # header is part of 'extract'
        extract = extract[1:]

    for i in range(hdr_len):
        key = names[i]
        value = []
        for j in range(len(extract)):
            value.append(extract[j][i])
        pd_dict[key] = value

    return pd.DataFrame(pd_dict)
