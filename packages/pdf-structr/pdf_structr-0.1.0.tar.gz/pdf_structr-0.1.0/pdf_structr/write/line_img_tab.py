# line_img_tab.py
'''
Module to store some dataclasses for the paragraphs, lines, images and table
elements extracted from the pdf.
'''

from dataclasses import dataclass
from typing import Generator, Iterable

import pymupdf  # type: ignore

from pdf_structr.tabs.prep_stats import (
    compute_bim_prop,
    compute_fprop_dicts_from_spans_tuples,
    compute_property_mode_and_relevancy,
    make_span_fprop_tuple,
)


@dataclass(slots=True, kw_only=True)
class Line:
    '''
    Class to store the lines.

    :param bbox: pymupdf.Rect: the rectangle containing the text that
        will be stored in the instance.

    :param str_itr: str | Iterable[str]: the string representation
        as an iterable of the text contained in the rectangle.

    :param prefix: str | Iterable[str]: an eventual line prefix.

    :param indent_prefix: str | Iterable[str]: an eventual line indent
        prefix, made of whitespaces.

    :param suffix: str | Iterable[str]: an eventual line suffix.

    :param lr_suffix: int. One or several line returns, to be added
        as suffixes upon concatenation of the line with other lines.

    :param line_type: str = 'regular': 'regular', 'bulleted',
        'bulleted-chunk', 'all-mono', 'header', 'header-chunk'.

    :param raw_line_no: int: the raw line number, upon
        extraction of the raw lines list from the clip (text rectangle or image
        rectangle).

    :param block: int: the block number to which the line pertains.

    :param spans: (
        list[dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]]
    ): the list of spans in the line.

    :param spans_count: int: 0-based number of spans in the paragraph.

    :param italic_span_count: int: 0-based counts of spans formatted as
        italics. -1 means no italic spans.

    :param bold_span_count: int: 0-based counts of spans formatted as
        bold. -1 means no bold spans.

    :param superscript_span_count: int: 0-based counts of spans formatted
        as superscript. -1 means no superscript spans.

    :param il_code_span_count: int: 0-based counts of spans formatted as
        inline code. -1 means no monosized font spans.

    '''

    # the rectangle containing the text
    bbox: pymupdf.Rect

    # String elements
    # the string representation of the text contained in the rectangle
    str_itr: str | Iterable[str]

    # Prefixes
    # an eventual prefix
    prefix: str | Iterable[str]
    # an eventual indent prefix
    indent_prefix: str | Iterable[str]

    # Suffixes
    # an eventual suffix
    suffix: str | Iterable[str]
    # a suffix to store line returns to be appended upon concatenation
    lr_suffix: int

    # Element informations
    line_type: str
    # the raw line number corresponding to the line
    raw_line_no: int
    # the block number to which the element pertains
    block: int

    # Data source: spans
    # spans: the spans in the line
    spans: list[
        dict[str, float | int | str | tuple[float, float] | pymupdf.Rect]
    ]

    # Spans' stats
    spans_count: int
    italic_span_count: int
    bold_span_count: int
    superscript_span_count: int
    il_code_span_count: int


@dataclass(slots=True, kw_only=True)
class Parag:
    '''
    Class to store the paragraphs. A paragraph encompasses several lines.
    It is meant to be an intermediary between a Line and a ParagImgTab.

    :param bbox: pymupdf.Rect: the rectangle containing the text that
        will be stored in the instance.

    :param str_itr: str | Iterable[str]: the string representation
        as an iterable of the text contained in the rectangle.

    :param prefix: str | Iterable[str]: an eventual line prefix.

    :param indent_prefix: str | Iterable[str]: an eventual line indent
        prefix, made of whitespaces.

    :param suffix: str | Iterable[str]: an eventual line suffix.

    :param lr_suffix: int. One or several line returns, to be added
        as suffixes upon concatenation of the line with other lines.

    :param parag_type: str = 'regular': 'regular', 'bulleted', 'all-mono',
        'header'.

    :param block: int: the block number to which the line pertains.

    :param lines: list[Lines]: a list of Line instances pertaining to this
        paragraph.

    :param spans_count: int: 0-based number of spans in the paragraph.

    :param italic_span_count: int: 0-based counts of spans formatted as
        italics. -1 means no italic spans.

    :param bold_span_count: int: 0-based counts of spans formatted as
        bold. -1 means no bold spans.

    :param superscript_span_count: int: 0-based counts of spans formatted
        as superscript. -1 means no superscript spans.

    :param il_code_span_count: int: 0-based counts of spans formatted as
        inline code. -1 means no monosized font spans.

    '''

    # the rectangle containing the text
    bbox: pymupdf.Rect

    # Element informations
    parag_type: str

    # Data source: lines, a list of Lines
    lines: list[Line]

    # Properties
    fs_mode: tuple[float, float] | None
    bold_prop: float | None
    ital_prop: float | None
    mono_prop: float | None
    flags_mode: tuple[float, float] | None
    color_mode: tuple[float, float] | None
    fontname_mode: tuple[str, float] | None

    # ----------------------------------------------------------
    # Methods
    # ----------------------------------------------------------

    @staticmethod
    def _is_span_bold(span: dict) -> bool:
        return (span['flags'] & 2**4) or (
            span['font'].lower().find('bold') != -1
        )

    @staticmethod
    def _is_span_italic(span: dict) -> bool:
        return (span['flags'] & 2**1) or (
            span['font'].lower().find('italic') != -1
        )

    @staticmethod
    def _is_span_mono(span: dict) -> bool:
        return (span['flags'] & 2**3) or (
            span['font'].lower().find('mono') != -1
        )

    def spans(self) -> Generator:
        return (_span for _line in self.lines for _span in _line.spans)

    def _is_span_bold_italic(self, span: dict) -> bool:
        return self._is_span_bold(span) and self._is_span_italic(span)

    # ----------------------------------------------------------
    # Get list of specific text (bold, italic, bold and italic)
    # ----------------------------------------------------------

    def italic_strings(self) -> list[str]:
        return [
            _span['text']  # type: ignore
            for _span in self.spans()
            # span flag or span in the fontname
            if self._is_span_italic(_span)
        ]

    def bold_strings(self) -> list[str]:
        return [
            _span['text']  # type: ignore
            for _span in self.spans()
            # bold flag or bold in the fontname
            if self._is_span_bold(_span)
        ]

    def bold_and_italic_strings(self) -> list[str]:
        return [
            _span['text']  # type: ignore
            for _span in self.spans()
            # bold flag or bold in the fontname
            if self._is_span_bold_italic(_span)  # type: ignore
        ]

    # ----------------------------------------------------------
    # Char counts
    # ----------------------------------------------------------

    def chars_count(self) -> int:
        return sum(
            len(_span['text']) for _span in self.spans()  # type: ignore
        )

    def _font_proprs_len_tups(
        self,
    ) -> list[tuple[int, float, int, int, int, int, int, str]]:
        return [make_span_fprop_tuple(_span) for _span in self.spans()]

    def set_font_properties(self) -> None:
        # Make a tuple of spans text length - font properties
        _spans_lens_font_properties_tl: list[
            tuple[int, float, int, int, int, int, int, str]
        ] = self._font_proprs_len_tups()

        # Get the char count
        _text_len: int = self.chars_count()

        (
            _sizes_dict,
            _bold_dict,
            _italic_dict,
            _mono_dict,
            _flags_dict,
            _colors_dict,
            _fontnames_dict,
        ) = compute_fprop_dicts_from_spans_tuples(
            _spans_lens_font_properties_tl
        )

        # Size
        self.fs_mode = compute_property_mode_and_relevancy(
            _sizes_dict, _text_len
        )
        # _size_prop: tuple[float, float] = (
        #     compute_property_mode_and_relevancy(
        #         _sizes_dict, _text_len
        #     )
        # )

        # Boldness
        self.bold_prop = compute_bim_prop(_bold_dict, _text_len, 16)
        # _bold_prop: float = compute_bim_prop(
        #     _bold_dict, _text_len, 16
        # )

        # Italic
        self.ital_prop = compute_bim_prop(_italic_dict, _text_len, 2)
        # _ital_prop: float = compute_bim_prop(
        #     _italic_dict, _text_len, 2
        # )

        # Mono
        self.mono_prop = compute_bim_prop(_mono_dict, _text_len, 8)
        # _mono_prop: float = compute_bim_prop(
        #     _mono_dict, _text_len, 8
        # )

        # Flags
        self.flags_mode = compute_property_mode_and_relevancy(
            _flags_dict, _text_len
        )

        # Color
        self.color_mode = compute_property_mode_and_relevancy(
            _colors_dict, _text_len  # type: ignore
        )
        # _color_mode_tup: tuple[float, float] = (
        #     compute_property_mode_and_relevancy(
        #         _colors_dict, _text_len_main_dict  # type: ignore
        #     )
        # )

        # Color
        self.fontname_mode = compute_property_mode_and_relevancy(
            _fontnames_dict, _text_len  # type: ignore
        )

    # ----------------------------------------------------------
    # Spans' counts
    # ----------------------------------------------------------

    def spans_count(self) -> int:
        return sum(1 for _span in self.spans())

    def italic_spans_count(self) -> int:
        return sum(
            1
            for _span in self.spans()
            # span flag or span in the fontname
            if self._is_span_italic(_span)
        )

    def bold_spans_count(self) -> int:
        return sum(
            1
            for _span in self.spans()
            # span flag or span in the fontname
            if self._is_span_bold(_span)
        )

    def bold_italic_spans_count(self) -> int:
        return sum(
            1
            for _span in self.spans()
            # span flag or span in the fontname
            if self._is_span_bold_italic(_span)
        )

    def mono_spans_count(self) -> int:
        return sum(
            1
            for _span in self.spans()
            # span flag or span in the fontname
            if self._is_span_mono(_span)
        )

    # ----------------------------------------------------------
    # Testing font property
    # ----------------------------------------------------------

    def is_all_italic(self) -> bool:
        if (self.italic_spans_count() / self.spans_count()) >= 0.8:
            return True

        return False

    def is_all_bold(self) -> bool:
        if (self.bold_spans_count() / self.spans_count()) >= 0.8:
            return True

        return False

    def is_all_mono(self) -> bool:
        if (self.mono_spans_count() / self.spans_count()) >= 0.8:
            return True

        return False

    # ----------------------------------------------------------
    # Printing text out as raw text or as md string
    # ----------------------------------------------------------

    def to_text(self) -> str:
        return ' '.join(
            _span['text'] for _span in self.spans()  # type: ignore
        )

    def to_md(self) -> str:
        return ''.join(
            _md_str_elt
            for _line in self.lines
            for _md_str_elt in _line.str_itr
        )

    def to_dict(self) -> dict:
        return {
            'block_left_x': self.bbox.x0,
            'block_top_y': self.bbox.y0,
            'block_right_x': self.bbox.x1,
            'block_bottom_y': self.bbox.y1,
            'line_left_x': self.bbox.x0,
            'line_top_y': self.bbox.y0,
            'line_right_x': self.bbox.x1,
            'line_bottom_y': self.bbox.y1,
            'font_size': self.fs_mode[0] if self.fs_mode else -1,
            'flags': self.flags_mode[0] if self.flags_mode else -1,
            'font_name': self.fontname_mode[0] if self.fontname_mode else '',
            'color': self.color_mode[0] if self.color_mode else -1,
            'text': self.to_text(),
            'span_left_x': self.bbox.x0,
            'span_top_y': self.bbox.y0,
            'span_right_x': self.bbox.x1,
            'span_bottom_y': self.bbox.y1,
        }


@dataclass(slots=True, kw_only=True)
class ParagImgTab:
    '''
    Class to store the either:
    - a list of Parag
    - the string representation and/or references to an image
    - the md-string representation of a table

    :param bbox: pymupdf.Rect: the rectangle containing the text that
        will be stored in the instance.

    :param str_itr: str | Iterable[str] = '': the string representation
        as an iterable of the text contained in the rectangle or as a
        string (only when the stored element is an image or a table).

    :param prefix: str | Iterable[str] = '': an eventual prefix.

    :param indent_prefix: str | Iterable[str] = '': an eventual indent
        prefix, made of whitespaces.

    :param suffix: str | Iterable[str] = '': an eventual suffix.

    :param lr_suffix: int: 0. one or several line returns, to be added
        as suffixes upon concatenation.

    :param elt_type: str = 'text': the type of element: 'text',
        'embd-text', 'table' or 'image_vg'.

    :param parags: list[Parag]: a list of Parag instances pertaining to this
        rectangle. May be an empty list if this is a 'table' or 'image_vg'.

    :param spans_count: int : the number of spans in the rectangle.
        May be -1 if the elt_type is 'table' or 'image_vg'.

    :param italic_span_count: int: 0-based counts of spans formatted as
        italics. -1 means no italic spans.

    :param bold_span_count: int: 0-based counts of spans formatted as
        bold. -1 means no bold spans.

    :param superscript_span_count: int: 0-based counts of spans formatted
        as superscript. -1 means no superscript spans.

    :param il_code_span_count: int: 0-based counts of spans formatted as
        inline code. -1 means no monosized font spans.
    '''

    # the rectangle containing the text
    bbox: pymupdf.Rect

    # String elements
    # the string representation of the text contained in the rectangle
    str_itr: str | Iterable[str] = ''

    # Prefixes
    # an eventual prefix
    prefix: str | Iterable[str] = ''
    # an eventual indent prefix
    indent_prefix: str | Iterable[str] = ''

    # Suffixes
    # an eventual suffix
    suffix: str | Iterable[str] = ''
    # a suffix to store line returns to be appended upon concatenation
    lr_suffix: int = 0

    # Element informations
    elt_type: str = ''

    # Data source: a list of Parag elements
    parags: list[Parag]

    # Spans' stats
    spans_count: int = -1
    italic_span_count: int = -1
    bold_span_count: int = -1
    superscript_span_count: int = -1
    il_code_span_count: int = -1
