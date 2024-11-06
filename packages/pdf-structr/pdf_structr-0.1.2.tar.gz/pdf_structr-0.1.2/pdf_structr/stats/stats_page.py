# stats_page.py
'''
Module to compute stats on the page's font sizes and length at the
spans, lines and blocks levels and add them to the corresponding
dicts.
'''

# import functools
import logging

import pymupdf  # type: ignore

from pdf_structr.stats.stats_block import (
    augment_block_and_subdicts,
)
from pdf_structr.stats.stats_page_ftsize import (
    compute_page_level_ftsize_stats,
)
from pdf_structr.stats.stats_x import (
    compute_page_level_coord_stats,
)

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
# Blocks
#####################


def _compute_stats_in_blocks_and_lower_level_dicts(
    page_stats: dict,
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[dict[str, int | float | tuple | list]]:
    '''
    Computes stats in blocks and lower level dicts.

    :return: a "cleaned up" list of blocks (only non-white text blocks)
        where each block and subdicts (lines and spans) has been
        augmented with stats about what it contains.

    :param page_stats: dict: a dict to collect statistics on the page.
    :param blocks: list[dict]: the page's blocks.
    '''
    # Iterate on the blocks by index, filtering out the non-text blocks
    # and compute stats at span, line and block levels
    _textblocks: list[dict[str, int | float | tuple | list]] = [
        augment_block_and_subdicts(
            textblock=_textblock,
            page_stats=page_stats,
        )
        for _textblock in blocks
        # only text block, no image block
        if _textblock['type'] == 0
    ]

    # Get rid of white blocks
    return [
        _textblock
        for _textblock in _textblocks
        if _textblock['txtlen_ftsize_tuples']
    ]


#####################
# Heavy API
#####################


def compute_and_store_stats_in_dicts(
    page: pymupdf.Page,
    blocks: list[dict[str, int | float | tuple | list]],
) -> tuple[list[dict[str, int | float | tuple | list]], dict]:
    '''
    Iretate on the textblocks and call _augment_block_and_subdicts which will
    compute text length and font size mode and median for
    the current block and its lines.

    We keep the lines in the order they are returned by
    textpage.extractDICT(sort=True).

    :returns: a blocks list where white blocks have been excluded and the
        _page_stats dict.

    :param blocks: list[dict]: the page's blocks.
    '''
    # Declare a _page_stats dict that will store the page statistiques
    _page_stats: dict[str, int | float | list] = {
        'page_number': page.number,
        'txt_len_bef_cleaning': 0,
        'span_count_bef_cleaning': 0,
        'line_count_bef_cleaning': 0,
        'block_count_bef_cleaning': len(blocks),
        'txt_len': 0,
        'txtlen_ftsize_tuples': [],
        'ft_size_mean': 0,
        'ft_size_med': 0,
        'ft_size_mod': 0,
        'ft_size_mod_2nd': 0,
        'ft_sizes_count': 0,
        'char_count_per_span_avg': 0,
        'char_count_per_span_med': 0,
        'char_count_per_line_avg': 0,
        'char_count_per_line_med': 0,
        'span_count_per_line_avg': 0,
        'span_count_per_line_med': 0,
        'span_count': 0,
        'line_count': 0,
        'block_count': 0,
        'digit_count': 0,
        'digit_span_count': 0,  # spans which text content is numeric only
        'chars_at_mode': 0,
        'spans_at_mode': 0,
        'lines_at_mode': 0,
        'blocks_at_mode': 0,
        'prop_chars_at_mode': 0,
        'prop_spans_at_mode': 0,
        'prop_lines_at_mode': 0,
        'prop_blocks_at_mode': 0,
    }

    # Iterate on the blocks by index, filtering out the non-text blocks
    # and compute stats at span, line and block levels
    _textblocks: list[dict[str, int | float | tuple | list]] = (
        _compute_stats_in_blocks_and_lower_level_dicts(
            page_stats=_page_stats,
            blocks=blocks,
        )
    )

    # Compute and save page level font size stats
    compute_page_level_ftsize_stats(
        page_stats=_page_stats, textblocks=_textblocks
    )

    # Compute and save page level x0 stats
    compute_page_level_coord_stats(
        page_stats=_page_stats, textblocks=_textblocks
    )

    return _textblocks, _page_stats


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
