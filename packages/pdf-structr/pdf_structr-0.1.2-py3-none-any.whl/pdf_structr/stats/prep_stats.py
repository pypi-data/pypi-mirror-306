# prep_stats.py
'''
Module to encapsulate functions that are preparing the table detection
by adding some statistical information to the blocks.
'''


import logging

import numpy as np

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
# Spans count per blocks
#####################


def _count_spans_per_block(
    block: dict[str, int | float | tuple | list]
) -> int:
    '''
    Count the spans' per block and returns the count.

    Provided that the passed-in block has been pre-processed by
    `clean_dicts_augment_spans` in module `augment`, the counted
    spans are the spans cleaned up of any white spans.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.).
    '''
    return sum(
        len(_line['spans'])  # type: ignore
        for _line in block['lines']  # type: ignore
    )


def _add_spans_count_per_block_to_blocks(
    blocks: list[dict[str, int | float | tuple | list]],
) -> None:
    '''
    Computes the spans' count per block and adds it as a new key
    to each block dict.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.).
    '''
    for _block in blocks:
        _block['spans_count'] = _count_spans_per_block(_block)


#####################
# Char count per blocks
#####################


def _add_char_count_per_block_to_blocks(
    blocks: list[dict[str, int | float | tuple | list]],
) -> None:
    '''
    Computes the char count per block and adds it as a new key
    to each block dict.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.).
    '''
    for _block in blocks:
        _block['txt_len'] = sum(
            len(_span['text'])  # type: ignore
            for _line in _block['lines']  # type: ignore
            for _span in _line['spans']  # type: ignore
        )


def compute_avg_char_count_per_block(
    blocks: list[dict[str, int | float | tuple | list]]
) -> float:
    '''
    Compute the arithmetic average charcount per block.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.).
    '''
    return np.mean([_block['txt_len'] for _block in blocks])


#####################
# Average char width
#####################


def compute_page_avg_char_width(
    blocks: list[dict[str, int | float | tuple | list]]
) -> float:
    '''
    Function to compute the basic arithmetic mean of a char in the page.

    NOTE: the computation here is very basic and does not make any distinction
    between spans of various fontsizes.

    :param page: pymupdf.Page: the current page.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.)
    '''
    # 1. compute spans width and char length
    _span_width_span_len_list: list[tuple[float, int]] = [
        (_span['bbox'][2] - _span['bbox'][0], len(_span['text']))
        for _block in blocks
        for _line in _block['lines']  # type: ignore
        for _span in _line['spans']  # type: ignore
    ]

    # 2. Compute average char width
    _sum_spans_width: float = sum(
        _span_width[0]  # type: ignore
        for _span_width in _span_width_span_len_list
    )

    _sum_spans_txt_len: int = sum(
        _span_txt_length[1]  # type: ignore
        for _span_txt_length in _span_width_span_len_list
    )

    # manual calculation of basic arithmetic mean
    return _sum_spans_width / _sum_spans_txt_len

    # # calculation of a list of the arithmetic char widht mean per span
    # list_of_arit_means_per_span: list[float] = [
    #     (_span_width_span_txt_len[0] / _span_width_span_txt_len[1])
    #     for _span_width_span_txt_len in _span_width_span_len_list
    # ]

    # _mean_arit_of_arit_means: float = np.average(
    #     list_of_arit_means_per_span  # type: ignore
    # )

    # # geometric mean
    # _total_span_count: int = len(_span_width_span_len_list)
    # _mean_geom: float = geometric_mean(list_of_arit_means_per_span)

    # # harmonic mean of spans' length
    # _mean_harm: float = harmonic_mean(list_of_arit_means_per_span)

    # # quadratic mean
    # _sum_of_square_of_means = np.sum(
    #     [
    #         np.square(_arit_mean)
    #         for _arit_mean in list_of_arit_means_per_span
    #     ]
    # )
    # _mean_quadra: float = np.sqrt(
    #     np.divide(_sum_of_square_of_means, _total_span_count)
    # )


#####################
# Blocks stats for extraction
#####################


def compute_stats_for_extraction(
    blocks: list[dict[str, int | float | tuple | list]],
) -> None:
    '''
    Adds spans count and char counts to the blocks.
    Returns the average char width in the blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.)

    '''
    _add_spans_count_per_block_to_blocks(blocks)
    _add_char_count_per_block_to_blocks(blocks)

    # NOTE: This is dead code, but let's keep it for the moment
    # _avg_char_count_per_block: float = compute_avg_char_count_per_block(
    #     blocks
    # )
    # compute_avg_char_count_per_block(blocks)
    # compute_page_avg_char_width(blocks)


#####################
# Block or row font size stats
#####################


def compute_ftsize_mode_for_block_or_row(
    main_dict: dict[str, int | float | tuple | list],
    subdict_key: str,
) -> tuple[float, float]:
    '''
    Compute the font size mode and mode relevancy for a given block or row.

    :returns: a 2-float tuple, where the first item is the mode font size
        and the second its relevancy:
        number of char at the font size / total number of chars in the block or
        row.

    :param main_dict: dict[str, int | float | tuple | list]: a row or a block.
        It must have a key equal to subdict_key, which itself contains
        a 'spans' key.

    :param subdict_key: str: the key under which the subdicts are stored
        under the main_dict. May be 'lines' (if the main dicts are blocks)
        or 'cells' (if the main dicts are rows).

    '''
    # Make a tuple of spans text length - font size
    _spans_lens_fss_tl: list[tuple[int, float]] = [
        (
            len(_span['text']),
            round(_span['size'], 1),
        )
        for _sub_dict in main_dict[subdict_key]  # type: ignore
        for _span in _sub_dict['spans']
    ]

    # Get the text length for the main dict
    _text_len_main_dict: int = main_dict.get('txt_len', 0)  # type: ignore
    if _text_len_main_dict == 0:
        _text_len_main_dict = sum(
            _span_len_fss_t[0]  # type: ignore
            for _span_len_fss_t in _spans_lens_fss_tl
        )

    # Convert the tuple to a dict and sum up the chars at a given
    # size
    _sizes_dict: dict[float, int] = {}
    for _len_fs_tup in _spans_lens_fss_tl:
        _sizes_dict[_len_fs_tup[1]] = (
            _sizes_dict.get(_len_fs_tup[1], 0) + _len_fs_tup[0]  # type: ignore
        )

    # If only one font size
    if len(_sizes_dict) == 1:

        # return the font size and a relevancy score set at 1
        return (
            # mode
            next(iter(_sizes_dict)),
            # 100% relevant
            1,
        )

    else:

        # sort the dict by values and convert it to a list of 2-tuples
        # font size - char count at font size sorted by highest
        # char count at font size
        _fss_len_tl: list[tuple[float, int]] = sorted(
            _sizes_dict.items(), key=lambda _fs_len: _fs_len[1]
        )

        return (
            # mode
            _fss_len_tl[-1][0],
            # compute relevancy score of mode:
            # char_count at mode / total char_count
            (_fss_len_tl[-1][1] / _text_len_main_dict),
        )


#####################
# Block or row font bold, italic and color
#####################


def compute_property_mode_and_relevancy(
    property_dict: dict[int | float, int],
    text_len_main_dict: int,
) -> tuple[float, float]:
    '''
    Computes the font size or color mode and the relevancy score of such mode.

    :param property_dict: dict[int, int]: the colors dictionary or font sizes
        dictionary, where the keys are the colors or the font sizes and
        the values, the char count at the corresponding color or font size.

    :param text_len_main_dict: int: the total char count in the block or row.

    '''
    # If only one color or font size
    if len(property_dict) == 1:

        # return the color or font size and a relevancy score set at 1
        return (
            next(iter(property_dict)),  # mode
            1,  # relevancy score: 1 = 100%
        )

    # sort the dict by values (text length) and convert it to a
    # list of 2-tuples color/font size - char count at color/font size
    # sorted in ascending of char counts
    _property_txtlength_tl: list[tuple[int | float, int]] = sorted(
        property_dict.items(), key=lambda _prop_len: _prop_len[1]
    )

    # mode: take the key of the last item in the list
    _property_mode_value: int | float = _property_txtlength_tl[-1][0]

    # relevancy score: char_count at mode / total char_count
    _relevancy_score: float = (
        _property_txtlength_tl[-1][1] / text_len_main_dict
    )

    return (
        _property_mode_value,
        _relevancy_score,
    )


def compute_bim_prop(
    property_dict: dict[int, int],
    text_len_main_dict: int,
    property_no: int,
) -> float:
    '''
    Computes the proportion of bold or italic characters in the block or row.

    :param property_dict: dict[int, int]: the property dict that serves as a
        data source. Either the bold_dict or the italic_dict.

    :param text_len_main_dict: int: the character count in the current
        row or block.

    :param property_no: int: 16 (for bold), 8 (for mono) or 2 (for italic).


    '''
    _proportion: float = 0

    # If only one item in the property dict
    if len(property_dict) == 1:

        # If the only item in the dict has for key the property_no
        if property_dict.get(property_no):

            # The proportion of characters at this proportion is 100%
            _proportion = 1

        # We do not compute the else case, since the else case is
        # no character at the property no => 0
        return _proportion

    # If we have characters both at the property and not at the property,
    # we compute the proportion:
    #  char count at property / total char count
    return property_dict[property_no] / text_len_main_dict


def _feed_in_dicts(
    sizes_dict: dict,
    bold_dict: dict,
    italic_dict: dict,
    mono_dict: dict,
    colors_dict: dict,
    flags_dict: dict,
    fontnames_dict: dict,
    property_tup: tuple[int, float, int, int, int, int, int, str],
) -> None:
    '''
    Feeds the property dicts.

    :param sizes_dict: dict: the dict to store the various font size
        as keys and the corresponding number of chars as values.

    :param bold_dict: dict: the dict to store whether the boldness
        or non-boldness of the chars as keys and the corresponding
        numbers of chars as values.

    :param italic_dict: dict: the dict to store whether the italicness
        or non-italicness of the chars as keys and the corresponding
        numbers of chars as values.

    :param colors_dict: dict: the dict to store whether the color code
        of the chars as keys and the corresponding numbers of chars as values.

    :param flags_dict: dict: the dict to store whether the flags of the
        chars as keys and the corresponding numbers of chars as values.

    :param property_tup: tuple[int, float, int, int, int, int]: the property
        tuple for the span: text length, size, boldness, italicness,
        monosizedness, color, font name.

    '''
    _text_length: int = property_tup[0]

    # feed in the size dict
    sizes_dict[property_tup[1]] = (
        sizes_dict.get(property_tup[1], 0) + _text_length  # type: ignore
    )

    # feed in the bold dict: add the number of characters in the
    # current span to the "bold" or "not bold" value of the bold dict
    bold_dict[property_tup[2]] = (
        bold_dict.get(property_tup[2], 0) + _text_length  # type: ignore
    )

    # feed in the italic dict
    italic_dict[property_tup[3]] = (
        italic_dict.get(property_tup[3], 0) + _text_length  # type: ignore
    )

    # feed in the monosized font dict
    mono_dict[property_tup[4]] = (
        italic_dict.get(property_tup[4], 0) + _text_length  # type: ignore
    )

    # feed in the flags dict
    flags_dict[property_tup[5]] = (
        italic_dict.get(property_tup[5], 0) + _text_length  # type: ignore
    )

    # feed in the colors dict
    colors_dict[property_tup[6]] = (
        colors_dict.get(property_tup[6], 0) + _text_length  # type: ignore
    )

    # feed in the font name dict
    fontnames_dict[property_tup[7]] = (
        colors_dict.get(property_tup[7], 0) + _text_length  # type: ignore
    )


def _compute_text_len_from_spans_prop_tup(
    spans_properties_tl: list[tuple],
) -> int:
    '''
    Compute the text length from the spans' properties tuples and return it.

    :param property_tup: tuple[int, float, int, int, int]: the property
        tuple for the span: text length, size, boldness, italicness, color.

    '''
    return sum(
        _span_property_tup[0]  # type: ignore
        for _span_property_tup in spans_properties_tl
    )


def _compute_text_len_for_block_or_row_from_spans_prop_tup(
    main_dict: dict[str, int | float | tuple | list],
    spans_properties_tl: list[tuple],
) -> int:
    '''
    Compute the text length for the main dict (block or row) and returns it.

    :param main_dict: dict[str, int | float | tuple | list]: a row or a block.
        It must have a key equal to subdict_key, which itself contains
        a 'spans' key.

    :param property_tup: tuple[int, float, int, int, int]: the property
        tuple for the span: text length, size, boldness, italicness, color.

    '''
    # Check if we've got a 'txt_len' property
    _text_len_main_dict: int = main_dict.get('txt_len', 0)  # type: ignore

    # If the main dict does not have a 'txt_len' property, compute it
    if _text_len_main_dict == 0:

        _text_len_main_dict = _compute_text_len_from_spans_prop_tup(
            spans_properties_tl
        )

    return _text_len_main_dict


def make_span_fprop_tuple(
    span: dict,
) -> tuple[int, float, int, int, int, int, int, str]:
    '''
    Make a font property tuple for a span. This font property tuple returns
    also the char count in the span, so that we can assess the proportion
    of chars in a multispan container.

    :param span: dict: a span's dictionary.
    '''
    _flags: int = span['flags']
    return (
        len(span['text']),
        round(span['size'], 1),
        _flags & 2**4,  # bold
        _flags & 2**1,  # italic
        _flags & 2**3,  # mono
        _flags,
        span['color'],
        span['font'],  # font name
    )


def _make_spans_fprop_tuples(
    main_dict: dict[str, int | float | tuple | list],
    subdict_key: str,
) -> list[tuple[int, float, int, int, int, int, int, str]]:
    '''
    Returns a list of tuple with the properties of the fonts of each
    span and the text length for each span.

    :param main_dict: dict[str, int | float | tuple | list]: a row or a block.
        It must have a key equal to subdict_key, which itself contains
        a 'spans' key.

    :param subdict_key: str: the key under which the subdicts are stored
        under the main_dict. May be 'lines' (if the main dicts are blocks)
        or 'cells' (if the main dicts are rows).

    '''
    return [
        make_span_fprop_tuple(_span)
        for _sub_dict in main_dict[subdict_key]  # type: ignore
        for _span in _sub_dict['spans']
    ]


def compute_fprop_dicts_from_spans_tuples(
    spans_lens_font_properties_tl: list[
        tuple[int, float, int, int, int, int, int, str]
    ],
) -> tuple[dict, dict, dict, dict, dict, dict, dict]:
    '''
    Compute the dicts required to compute the following font properties
    for a passed-in spans font properties list of tuples:
    - the font size mode and its relevancy score
    - the proportion of bold and italic characters
    - the color mode and its relevancy score.

    :returns: a 5-tuple, with, 5 dict:
        - the font sizes dict, with a char count for each font size
        - the bold fonts dict with the bold char count
        - the italic fonts dict with the italic char count
        - the mono fonts dict with the mono char count
        - the flag applicable to the spans, with a char count for each flags
        - the font colors dict, with a char count for each color
        - the font name dict, with a char count for each font name

    :param spans_lens_font_properties_tl: list[
        tuple[int, float, int, int, int, int, int, str]
    ]: the property tuple for the span: text length, size, boldness,
        italicness, monosizedness, flags, color, font name.

    '''
    # Convert the tuples to dicts and sum up the chars at a given property
    _sizes_dict: dict[float, int] = {}
    _bold_dict: dict[int, int] = {}
    _italic_dict: dict[int, int] = {}
    _mono_dict: dict[int, int] = {}
    _flags_dict: dict[int, int] = {}
    _colors_dict: dict[int, int] = {}
    _fontnames_dict: dict[str, int] = {}

    # walk the tuples and feed in the bold and italic dict
    for _span_property_tup in spans_lens_font_properties_tl:

        _feed_in_dicts(
            sizes_dict=_sizes_dict,
            bold_dict=_bold_dict,
            italic_dict=_italic_dict,
            mono_dict=_mono_dict,
            flags_dict=_flags_dict,
            colors_dict=_colors_dict,
            fontnames_dict=_fontnames_dict,
            property_tup=_span_property_tup,
        )

    return (
        _sizes_dict,
        _bold_dict,
        _italic_dict,
        _mono_dict,
        _flags_dict,
        _colors_dict,
        _fontnames_dict,
    )


def _compute_fprop_block_or_row_dicts(
    main_dict: dict[str, int | float | tuple | list],
    subdict_key: str,
) -> tuple[int, dict, dict, dict, dict, dict, dict, dict]:
    '''
    Compute the dicts required to compute the following font properties
    for a given block or row:
    - the font size mode and its relevancy score
    - the proportion of bold and italic characters
    - the color mode and its relevancy score.

    :returns: a 5-tuple, with, for the main dict:
        - the char count
        - a tuple font size mode - fs mode relevancy
        - the bold char proportion
        - the italic char proportion
        - the mono char proportion
        - the flag mode - flag mode relevancy
        - a tuple char color mode - color mode relevancy
        - a font name mode - font name mode relevancy

    :param main_dict: dict[str, int | float | tuple | list]: a row or a block.
        It must have a key equal to subdict_key, which itself contains
        a 'spans' key.

    :param subdict_key: str: the key under which the subdicts are stored
        under the main_dict. May be 'lines' (if the main dicts are blocks)
        or 'cells' (if the main dicts are rows).

    '''

    # Make a tuple of spans text length - properties
    _spans_lens_font_properties_tl: list[
        tuple[int, float, int, int, int, int, int, str]
    ] = _make_spans_fprop_tuples(main_dict, subdict_key)

    # Get the text length for the main dict
    _text_len_main_dict: int = (
        _compute_text_len_for_block_or_row_from_spans_prop_tup(
            main_dict=main_dict,
            spans_properties_tl=_spans_lens_font_properties_tl,
        )
    )

    # Convert the tuples to dicts and sum up the chars at a given property
    return (
        _text_len_main_dict,
        *compute_fprop_dicts_from_spans_tuples(
            spans_lens_font_properties_tl=_spans_lens_font_properties_tl,
        ),
    )


def compute_fprop_block_or_row(
    main_dict: dict[str, int | float | tuple | list],
    subdict_key: str,
) -> tuple[int, tuple[float, float], float, float, float, tuple[float, float]]:
    '''
    Compute the following properties for a given block or row:
    - the font size mode and its relevancy score
    - the proportion of bold and italic characters
    - the color mode and its relevancy score.

    :returns: a 5-tuple, with, for the main dict:
        - the char count
        - a tuple font size mode - fs mode relevancy
        - the bold char proportion
        - the italic char proportion
        - a tuple char color mode - color relevancy

    :param main_dict: dict[str, int | float | tuple | list]: a row or a block.
        It must have a key equal to subdict_key, which itself contains
        a 'spans' key.

    :param subdict_key: str: the key under which the subdicts are stored
        under the main_dict. May be 'lines' (if the main dicts are blocks)
        or 'cells' (if the main dicts are rows).

    '''
    (
        _text_len_main_dict,
        _sizes_dict,
        _bold_dict,
        _italic_dict,
        _mono_dict,
        _,
        _colors_dict,
        _,
    ) = _compute_fprop_block_or_row_dicts(main_dict, subdict_key)

    # Size
    _size_prop: tuple[float, float] = compute_property_mode_and_relevancy(
        _sizes_dict, _text_len_main_dict
    )

    # Boldness
    _bold_prop: float = compute_bim_prop(_bold_dict, _text_len_main_dict, 16)

    # Italic
    _ital_prop: float = compute_bim_prop(_italic_dict, _text_len_main_dict, 2)

    # Mono
    _mono_prop: float = compute_bim_prop(_mono_dict, _text_len_main_dict, 8)

    # Color
    _color_mode_tup: tuple[float, float] = compute_property_mode_and_relevancy(
        _colors_dict, _text_len_main_dict  # type: ignore
    )

    return (
        _text_len_main_dict,
        _size_prop,
        _bold_prop,
        _ital_prop,
        _mono_prop,
        _color_mode_tup,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
