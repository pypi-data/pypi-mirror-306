# main.py
'''
This is the new version of the md producer proposed by PyMuPDF
under the new name `pymupdf4llm`, extracted out of the library for refactoring.

This module is called `pymupdf_rag` in `pymupdf4llm`.

Credits to the pymupdf team for their awesome work.

Below is the description provided in the original module.

------------
This script accepts a PDF document filename and converts it to a text file
in Markdown format, compatible with the GitHub standard.

It must be invoked with the filename like this:

python pymupdf_rag.py input.pdf [-pages PAGES]

The "PAGES" parameter is a string (containing no spaces) of comma-separated
page numbers to consider. Each item is either a single page number or a
number range "m-n". Use "N" to address the document's last page number.
Example: "-pages 2-15,40,43-N"

It will produce a markdown text file called "input.md".

Text will be sorted in Western reading order. Any table will be included in
the text in markdwn format as well.

Dependencies
-------------
PyMuPDF v1.24.2 or later

Copyright and License
----------------------
Copyright 2024 Artifex Software, Inc.
License GNU Affero GPL 3.0
Cédric Lor

Additional docstring for the refactored version:
----------------------

This module stores the high-level entry point API functions to access
the refactored pymupdf4llm, called here custrag.

To the difference of the original module, it may not be invoked
from the command line.

As the original one, it may return either:
- an md-string
- a list of dict for each page, containing the md-string and additional
information on the images, tables, etc.

In addition, to_paragimgtabs_list returns a list of ParagImgTab objects,
a class specially designed to store the various elements that may be
returned from the parsing of the pages.

ParagImgTab having a type 'text' or 'embed-text' contain a
list of text paragraphs which contain unstructured data cleanly
separated in paragraphs to be provided as input to a RAG.

ParagImgTab having a type 'table' contain an md-string of the parsed
table.

When using these functions in code, precautions have to be taken to
provide all the parameters that do not have default values in the
decorator wrapper function.

Luckily, the only parameter that does not have default argument is
the `doc` parameter, which may be a string or a pymupdf.Doc.

However, for optimal results, it is better to check out the parameters
of the decorator.
'''

from typing import Callable, Generator, Union

# try:
#     import pymupdf as pymupdf  # available with v1.24.3
# except ImportError:
#     import pymupdf
import pymupdf  # type: ignore

from pdf_structr.extract.extract import process_page_decorator
from pdf_structr.main_utils import (
    get_metadata,
    process_doc_decorator,
)
from pdf_structr.write.extract_pits import (
    extract_paragimgtabs_for_page,
)
from pdf_structr.write.classes import ParagImgTab
from pdf_structr.write.main import get_md_string_for_page

# if pymupdf.pymupdf_version_tuple < (1, 24, 2):
#     raise NotImplementedError("PyMuPDF version 1.24.2 or later is needed.")


@process_doc_decorator
def to_paragimgtabs_list(
    doc: pymupdf.Document,
    *,
    pages: list[int],
    textflags: Union[int, int],
    get_header_id: Callable,
    margins: tuple[float, float, float, float],
    table_strategy: str,
    PARAM: dict[str, str | int | bool | None],
) -> Generator[list[ParagImgTab], None, None]:
    '''
    Process the document and return the ParagImgTabs built from the elements
    on the selected pages as a generator.

    Each element yielded by the Generator is a list of ParagImgTabs
    representing a page in the document.

    :param doc: pymupdf.Document.

    :param pages: list[int]: list of page numbers to consider (0-based).

    :param textflags: Union[int, int]: the applicable text flags for the
        TextPages extraction. Union in this context is equivalent to
        adding the values of the respective textflags. Defaults to 192
        as per the main decorator (i.e. TEXT_MEDIABOX_CLIP (64) and
        TEXT_CID_FOR_UNKNOWN_UNICODE (128)).

    :param get_header_id: Callable: the headers identifier callable.

    :param margins: (
        float
        | tuple[float]
        | tuple[float, float]
        | tuple[float, float, float, float]
        | None
    ) = None: a float, a 1-tuple float, a 2-tuple float or a 4-tuple float
        that sets the requested margins beyond which content shall not be
        considered:
        - single value: margin applicable to all sides
        - 2-tuple float: the top and bottom margins
        - 4-tuple float: left-top-right-bottom margins

    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text' and 'IGNORE_CODE'.
    '''
    return (
        process_page_decorator(extract_paragimgtabs_for_page)(
            page=doc[pno],
            margins=margins,
            table_strategy=table_strategy,
            textflags=textflags,
            get_header_id=get_header_id,
            PARAM=PARAM,
        )[0]
        # Walk the pages
        for pno in pages
    )


@process_doc_decorator
def to_markdown_gen(
    doc: pymupdf.Document,
    *,
    pages: list[int],
    textflags: Union[int, int],
    get_header_id: Callable,
    margins: tuple[float, float, float, float],
    table_strategy: str,
    PARAM: dict[str, str | int | bool | None],
) -> Generator[str, None, None]:
    '''
    Process the document and return the text of the selected pages as
    a generator.

    Each element yielded by the Generator is a string representing a page
    in the document.

    :param doc: pymupdf.Document.

    :param pages: list[int]: list of page numbers to consider (0-based).

    :param textflags: Union[int, int]: the applicable text flags for the
        TextPages extraction. Union in this context is equivalent to
        adding the values of the respective textflags. Defaults to 192
        as per the main decorator (i.e. TEXT_MEDIABOX_CLIP (64) and
        TEXT_CID_FOR_UNKNOWN_UNICODE (128)).

    :param get_header_id: Callable: the headers identifier callable.

    :param margins: (
        float
        | tuple[float]
        | tuple[float, float]
        | tuple[float, float, float, float]
        | None
    ) = None: a float, a 1-tuple float, a 2-tuple float or a 4-tuple float
        that sets the requested margins beyond which content shall not be
        considered:
        - single value: margin applicable to all sides
        - 2-tuple float: the top and bottom margins
        - 4-tuple float: left-top-right-bottom margins

    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries.

    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text' and 'IGNORE_CODE'.
    '''
    return (
        get_md_string_for_page(
            page=doc[pno],
            margins=margins,
            table_strategy=table_strategy,
            textflags=textflags,
            get_header_id=get_header_id,
            PARAM=PARAM,
        )[0]
        # Walk the pages
        for pno in pages
    )


@process_doc_decorator
def to_markdown_list(
    doc: pymupdf.Document,
    *,
    pages: list[int],
    textflags: Union[int, int],
    get_header_id: Callable,
    margins: tuple[float, float, float, float],
    table_strategy: str,
    PARAM: dict[str, str | int | bool | None],
) -> list[dict]:
    """
    Process the document and return the text of the selected pages.

    :return: a list of dict, with one dict per page, providing informations
    on the metadata, the page_tocs, the page images, the page tables, the
    page graphics and the text output.

    :param doc: pymupdf.Document.
    :param pages: list[int]: list of page numbers to consider (0-based).
    :param textflags: Union[int, int]: the applicable text flags for the
        TextPages extraction. Union in this context is equivalent to
        adding the values of the respective textflags. Defaults to 192
        as per the main decorator (i.e. TEXT_MEDIABOX_CLIP (64) and
        TEXT_CID_FOR_UNKNOWN_UNICODE (128)).
    :param get_header_id: Callable: the headers identifier callable.
    :param margins: (
        float
        | tuple[float]
        | tuple[float, float]
        | tuple[float, float, float, float]
        | None
    ) = None: a float, a 1-tuple float, a 2-tuple float or a 4-tuple float
        that sets the requested margins beyond which content shall not be
        considered:
        - single value: margin applicable to all sides
        - 2-tuple float: the top and bottom margins
        - 4-tuple float: left-top-right-bottom margins
    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries.
    :param PARAM: dict[str, str | int | bool | None]: a dict containing
        constant parameters including 'IMG_PATH', 'IMG_EXTENSION', 'DPI',
        'GRAPHICS_LIMIT', 'write_images', 'force_text' and 'IGNORE_CODE'.
    """
    document_output: list = []

    # read the Table of Contents
    toc: list = doc.get_toc()

    # Walk the pages
    for pno in pages:
        page_output, images, tables, graphics = get_md_string_for_page(
            page=doc[pno],
            margins=margins,
            table_strategy=table_strategy,
            textflags=textflags,
            get_header_id=get_header_id,
            PARAM=PARAM,
        )

        # build subet of TOC for this page
        page_tocs = [t for t in toc if t[-1] == pno + 1]

        metadata = get_metadata(doc, pno)

        # Append
        document_output.append(
            {
                "metadata": metadata,
                "toc_items": page_tocs,
                "tables": tables,
                "images": images,
                "graphics": graphics,
                "text": page_output,
            }
        )

    return document_output


if __name__ == "__main__":
    pass
