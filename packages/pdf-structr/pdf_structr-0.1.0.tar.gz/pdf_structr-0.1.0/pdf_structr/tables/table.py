"""
Copyright (C) 2023 Artifex Software, Inc.

This file is part of PyMuPDF.

PyMuPDF is free software: you can redistribute it and/or modify it under the
terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

PyMuPDF is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License
along with MuPDF. If not, see <https://www.gnu.org/licenses/agpl-3.0.en.html>

Alternative licensing terms are available from the licensor.
For commercial licensing, see <https://www.artifex.com/> or contact
Artifex Software, Inc., 39 Mesa Street, Suite 108A, San Francisco,
CA 94129, USA, for further information.

---------------------------------------------------------------------
Portions of this code have been ported from pdfplumber, see
https://pypi.org/project/pdfplumber/.

The ported code is under the following MIT license:

---------------------------------------------------------------------
The MIT License (MIT)

Copyright (c) 2015, Jeremy Singer-Vine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---------------------------------------------------------------------
Also see here: https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt
---------------------------------------------------------------------

The porting mainly pertains to files "table.py" and relevant parts of
"utils/text.py" within pdfplumber's repository on Github.
With respect to "text.py", we have removed functions or features that are not
used by table processing. Examples are:

* the text search function
* simple text extraction
* text extraction by lines

Original pdfplumber code does neither detect, nor identify table headers.
This PyMuPDF port adds respective code to the 'Table' class as method
'_get_header'.
This is implemented as new class TableHeader with the properties:
* bbox: A tuple for the header's bbox
* cells: A tuple for each bbox of a column header
* names: A list of strings with column header text
* external: A bool indicating whether the header is outside the table cells.

"""

# import itertools
from functools import partial, wraps

# from operator import itemgetter
from typing import Any, Callable

# -------------------------------------------------------------------
# Start of PyMuPDF interface code
# -------------------------------------------------------------------
from pymupdf import (  # type: ignore
    TOOLS,
    Page,
    TextPage,
)

from pdf_structr.tables.classes import NewTableFinder
from pdf_structr.tables.clean_graphics import clean_graphics
from pdf_structr.tables.make_chars import make_chars
from pdf_structr.tables.make_edges import (
    make_edges,
)
from pdf_structr.tables.settings import (
    DEFAULT_JOIN_TOLERANCE,
    DEFAULT_MIN_WORDS_HORIZONTAL,
    DEFAULT_MIN_WORDS_VERTICAL,
    DEFAULT_SNAP_TOLERANCE,
    # TableSettings,
    configure_find_tables,
    page_rotation_reset,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer


# -----------------------------------------------------------------------------
# Extract all page characters to fill the CHARS list
# -----------------------------------------------------------------------------

# def make_chars():
#     pass
# NOTE: `make_chars()` refactored now living in `table_make_chars` module.


# ------------------------------------------------------------------------
# Extract all page vector graphics to fill the EDGES list.
# We are ignoring Bézier curves completely and are converting everything
# else to lines.
# ------------------------------------------------------------------------

# def make_edges():
#     pass
# NOTE: `make_edges()` refactored now living in `table_make_edges` module.


def find_tables_decorator(
    find_tables_func: Callable, return_table_only: bool = True
) -> Callable:
    '''
    High order function that takes in the find_tables function
    and makes it return either the TableFinder only or the
    TableFinder and the chars and edges lists.

    Not strictly speaking a decorator, as it takes more than one
    single function as argument.

    This is actually more of a cache than a decorator.

    :param find_tables_func: Callable: the `find_tables` function.

    :param return_table_only: bool = True: whether we want the
        `find_tables` function to return the TableFinder only
        or the chars and edges list also in a tuple.
    '''

    @wraps(find_tables_func)
    def find_tables_wrapper(*args, **kwargs) -> Any:

        # Update the _prev_pno attribute
        _current_pno: int = kwargs.get('page').number  # type: ignore

        # If it is None, we're on a new page
        # -------------------------------------------
        if find_tables_wrapper._prev_pno is None:  # type: ignore

            find_tables_wrapper._prev_pno = _current_pno  # type: ignore

        # Else we're on the same page as the previous call
        # -------------------------------------------
        elif find_tables_wrapper._prev_pno == _current_pno:  # type: ignore

            # If we are on the same page as the previous call
            # we should pass the _prev_chars and _prev_edges
            # to find table
            kwargs['chars'] = find_tables_wrapper._prev_chars  # type: ignore
            kwargs['edges'] = find_tables_wrapper._prev_edges  # type: ignore
            kwargs['textpage'] = find_tables_wrapper._textpage  # type: ignore
            kwargs['drawings'] = find_tables_wrapper._drawings  # type: ignore

        # Call the find tables function
        _tabs, _chars, _edges, _textpage = find_tables_func(*args, **kwargs)

        # Update the previous stateful parameters
        find_tables_wrapper._prev_pno = _current_pno  # type: ignore
        find_tables_wrapper._prev_clip = kwargs.get('clip')  # type: ignore
        find_tables_wrapper._prev_chars = _chars  # type: ignore
        find_tables_wrapper._prev_edges = _edges  # type: ignore
        find_tables_wrapper._textpage = _textpage  # type: ignore
        find_tables_wrapper._drawings = kwargs['drawings']  # type: ignore

        # Return the TableFinder or the TableFinder - chars - edges tuple
        if return_table_only:

            return _tabs

        return _tabs, _chars, _edges

        # ----------- end of wrapper func -----------

    # Define the find_tables_wrapper attributes
    find_tables_wrapper._prev_pno = None  # type: ignore
    find_tables_wrapper._prev_clip = None  # type: ignore
    find_tables_wrapper._prev_chars = None  # type: ignore
    find_tables_wrapper._prev_edges = None  # type: ignore
    find_tables_wrapper._textpage = None  # type: ignore
    find_tables_wrapper._drawings = None  # type: ignore

    return find_tables_wrapper


# @count_and_avg_timer(name='prep - find_tables')
@find_tables_decorator
def find_tables(
    page: Page,
    textpage: TextPage,
    drawings: list[dict],
    clip=None,
    vertical_strategy: str = "lines",
    horizontal_strategy: str = "lines",
    vertical_lines: list | None = None,
    horizontal_lines: list | None = None,
    snap_tolerance: float = DEFAULT_SNAP_TOLERANCE,
    snap_x_tolerance: float | None = None,
    snap_y_tolerance: float | None = None,
    join_tolerance: float = DEFAULT_JOIN_TOLERANCE,
    join_x_tolerance: float | None = None,
    join_y_tolerance: float | None = None,
    edge_min_length: float = 3,
    min_words_vertical: float = DEFAULT_MIN_WORDS_VERTICAL,
    min_words_horizontal: float = DEFAULT_MIN_WORDS_HORIZONTAL,
    intersection_tolerance: float = 3,
    intersection_x_tolerance: float | None = None,
    intersection_y_tolerance: float | None = None,
    text_tolerance: float = 3,
    text_x_tolerance: float = 3,
    text_y_tolerance: float = 3,
    strategy: str | None = None,  # offer abbreviation
    add_lines=None,  # optional user-specified lines
    blocks: list[dict] | None = None,
    chars: list[dict] | None = None,
    edges: list[dict] | None = None,
) -> tuple[
    NewTableFinder,
    list[dict[Any, Any]],
    list[dict[Any, Any]] | None,
    TextPage | None,
]:
    '''
    Customized version of the find_tables function in pymupdf
    `table` module.
    '''
    # -----------------------------------
    # Configure settings
    # -----------------------------------

    page, tset, old_small, old_xref, old_rot, old_mediabox = (
        configure_find_tables(
            page=page,
            vertical_strategy=vertical_strategy,
            horizontal_strategy=horizontal_strategy,
            vertical_lines=vertical_lines,
            horizontal_lines=horizontal_lines,
            snap_tolerance=snap_tolerance,
            snap_x_tolerance=snap_x_tolerance,
            snap_y_tolerance=snap_y_tolerance,
            join_tolerance=join_tolerance,
            join_x_tolerance=join_x_tolerance,
            join_y_tolerance=join_y_tolerance,
            edge_min_length=edge_min_length,
            min_words_vertical=min_words_vertical,
            min_words_horizontal=min_words_horizontal,
            intersection_tolerance=intersection_tolerance,
            intersection_x_tolerance=intersection_x_tolerance,
            intersection_y_tolerance=intersection_y_tolerance,
            text_tolerance=text_tolerance,
            text_x_tolerance=text_x_tolerance,
            text_y_tolerance=text_y_tolerance,
            strategy=strategy,
        )
    )

    # -----------------------------------
    # Make the CHARS list
    # -----------------------------------

    # create list of characters for page
    if chars is None:
        chars = []
        # chars += make_chars(page, textpage=TEXTPAGE)
        chars += make_chars(page, textpage=textpage)

    # -----------------------------------
    # Find the edges
    # -----------------------------------

    # We only need to try and detect edges if the table detection
    # strategy is of type 'lines' or 'lines_strict'
    # In strategy 'text', the tables will be detected based on text
    # position.
    # In strategy 'explicit', the tables will detected based on
    # the passed-in vertical_lines and horizontal_lines.
    if (
        (vertical_strategy in ['lines', 'lines_strict'])
        or (horizontal_strategy in ['lines', 'lines_strict'])
    ) and edges is None:

        # Make a partial to pre-configure `clean_graphics`
        _clean_graphics_partial: partial = partial(
            clean_graphics,
            page=page,
            textpage=textpage,
            drawings=drawings,
            lines_strict=(
                tset.vertical_strategy == "lines_strict"  # type: ignore
                or tset.horizontal_strategy == "lines_strict"  # type: ignore
            ),
        )

        edges = make_edges(
            page,
            _clean_graphics_partial,
            clip=clip,
            tset=tset,
            add_lines=add_lines,
        )  # create lines and curves

    # -----------------------------------
    # Make the tables
    # -----------------------------------

    # tables = TableFinder(page)
    tables = NewTableFinder(
        page=page,
        textpage=textpage,
        edges=edges,
        blocks=blocks,
        chars=chars,
    )

    # -----------------------------------
    # Restore settings
    # -----------------------------------

    TOOLS.set_small_glyph_heights(old_small)

    if old_xref is not None:
        page = page_rotation_reset(page, old_xref, old_rot, old_mediabox)

    # -----------------------------------
    # Return the loaded TableFinder
    # -----------------------------------

    return tables, chars, edges, textpage
