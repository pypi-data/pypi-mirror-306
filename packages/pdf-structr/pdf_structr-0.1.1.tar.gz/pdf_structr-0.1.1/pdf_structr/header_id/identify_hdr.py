# identify_hdr.py
'''
Storing the identify header class from pymupdf4llm
'''

import pymupdf  # type: ignore

from pdf_structr.get_text_lines.make_spans_list import (
    is_white,
)


def _feed_fontsize_dict(span: dict, fontsizes: dict) -> None:
    fontsz: int = round(span["size"])
    count = fontsizes.get(fontsz, 0) + len(span["text"].strip())
    fontsizes[fontsz] = count


def _load_page_blocks(mydoc: pymupdf.Document, pno: int) -> list[dict]:
    page: pymupdf.Page = mydoc.load_page(page_id=pno)
    return page.get_text("dict", flags=pymupdf.TEXTFLAGS_TEXT)["blocks"]


def _load_page_blocks_wrapper(
    mydoc: pymupdf.Document, pages: list[int]
) -> list[list[dict]]:
    return [_load_page_blocks(mydoc, _pno) for _pno in pages]


class IdentifyHeaders:
    """
    Compute data for identifying header text.

    All non-white text from all selected pages is extracted and its font size
    noted as a rounded value.
    The most frequent font size (and all smaller ones) is taken as body text
    font size.
    Larger font sizes are mapped to strings of multiples of '#', the header
    tag in Markdown, which in turn is Markdown's representation of HTML's
    header tags <h1> to <h6>.
    Larger font sizes than body text but smaller than the <h6> font size are
    represented as <h6>.
    """

    def __init__(
        self,
        doc: str | pymupdf.Document,
        pages: list[int],
        body_limit: float = 12,
    ):
        """Read all text and make a dictionary of fontsizes.

        Args:
            pages: optional list of pages to consider
            body_limit: consider text with larger font size as some header
        """
        mydoc: pymupdf.Document
        if isinstance(doc, pymupdf.Document):
            mydoc = doc
        else:
            mydoc = pymupdf.open(doc)

        if pages is None:  # use all pages if omitted
            pages = range(mydoc.page_count)

        fontsizes: dict[int, int] = {}
        # look at all non-empty horizontal spans
        [
            _feed_fontsize_dict(span, fontsizes)  # type: ignore
            for _page_blocks in _load_page_blocks_wrapper(mydoc, pages)
            for block in _page_blocks
            for line in block["lines"]
            for span in line["spans"]
            if not is_white(span["text"])
        ]

        if mydoc != doc:
            # if opened here, close it now
            mydoc.close()

        # maps a fontsize to a string of multiple # header tag characters
        self.header_id = {}

        # If not provided, choose the most frequent font size as body text.
        # If no text at all on all pages, just use 12.
        # In any case all fonts not exceeding
        temp = sorted(
            fontsizes.items(),
            key=lambda i: i[1],
            reverse=True,
        )
        if temp:
            self.body_limit = max(body_limit, temp[0][0])
        else:
            self.body_limit = body_limit

        # identify up to 6 font sizes as header candidates
        sizes = sorted(
            [f for f in fontsizes.keys() if f > self.body_limit],
            reverse=True,
        )[:6]

        # make the header tag dictionary
        for i, size in enumerate(sizes):
            self.header_id[size] = "#" * (i + 1) + " "

    def get_header_id(self, span: dict, page=None) -> str:
        """Return appropriate markdown header prefix.

        Given a text span from a "dict"/"rawdict" extraction, determine the
        markdown header prefix string of 0 to n concatenated '#' characters.
        """
        fontsize: int = round(span["size"])  # compute fontsize
        if fontsize <= self.body_limit:  # shortcut for body text
            return ""
        hdr_id: str = self.header_id.get(fontsize, "")
        # If no header but larger than body text, assign <h6>.
        if not hdr_id and fontsize > self.body_limit:
            hdr_id = "###### "
        return hdr_id
