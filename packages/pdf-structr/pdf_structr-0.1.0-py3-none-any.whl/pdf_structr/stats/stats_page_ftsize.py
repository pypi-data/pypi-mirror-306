# stats_page_ftsize.py
'''
Module to compute stats on the page's font sizes and length at the
spans, lines and blocks levels and add them to the corresponding
dicts.
'''

# import functools
import logging

from pdf_structr.stats.stats_lib import (
    add_mode_median_mean_ftsize_to_txtdict,
    compute_chars_stats_per_span,
    compute_item_median_and_mean_per_elt_in_collection,
    flatten_txtlen_ftsize_tuples_list,
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
# Page level stats computation
#####################


def _compute_proportion_elts_at_mode_ftsize(page_stats: dict) -> None:
    '''
    Compute proportion of blocks, lines, spans and chars at the font size
    mode at page level.

    :param page_stats: dict: a dict to collect statistics on the page.
    '''

    page_stats['prop_blocks_at_mode'] = (
        page_stats['blocks_at_mode']
        / page_stats['block_count']  # type: ignore
    )

    page_stats['prop_lines_at_mode'] = (
        page_stats['lines_at_mode'] / page_stats['line_count']  # type: ignore
    )

    page_stats['prop_spans_at_mode'] = (
        page_stats['spans_at_mode'] / page_stats['span_count']  # type: ignore
    )

    page_stats['prop_chars_at_mode'] = (
        page_stats['chars_at_mode'] / page_stats['txt_len']  # type: ignore
    )


def _count_elts_at_ftsize_mode(page_stats: dict, textblocks: list[dict]):
    '''
    Count the number of blocks, lines, spans and chars at the font size
    mode at page level.

    :param page_stats: dict: a dict to collect statistics on the page.
    :param textblocks: list[dict]: the list of non-white and non-empty
        text block dicts.
    '''

    page_stats['blocks_at_mode'] = len(
        [
            _block
            for _block in textblocks
            if (
                _block['ft_size_mod']  # type: ignore
                == page_stats['ft_size_mod']
            )
        ]
    )

    page_stats['lines_at_mode'] = len(
        [
            _line
            for _block in textblocks
            for _line in _block['lines']  # type: ignore
            if (
                _line['ft_size_mod']  # type: ignore
                == page_stats['ft_size_mod']
            )
        ]
    )

    page_stats['spans_at_mode'] = len(
        [
            _span
            for _block in textblocks
            for _line in _block['lines']  # type: ignore
            for _span in _line['spans']
            if (_span['size'] == page_stats['ft_size_mod'])  # type: ignore
        ]
    )

    page_stats['chars_at_mode'] = sum(
        [
            _span['txt_len']
            for _block in textblocks
            for _line in _block['lines']  # type: ignore
            for _span in _line['spans']
            if (_span['size'] == page_stats['ft_size_mod'])  # type: ignore
        ]
    )


def _compute_additional_page_level_stats(
    page_stats: dict, textblocks: list[dict]
) -> None:
    '''
    Compute additional page level stats.

    :param page_stats: dict: a dict to collect statistics on the page.
    :param textblocks: list[dict]: the list of non-white and non-empty
        text block dicts.
    '''

    # Compute and save the non-white text blocks count for the page
    page_stats['block_count'] = len(textblocks)

    # Count elements (blocks, lines, spans and chars) at page level
    # font size mode
    _count_elts_at_ftsize_mode(page_stats=page_stats, textblocks=textblocks)

    # Compute proportion of each elements at page level font size mode
    _compute_proportion_elts_at_mode_ftsize(page_stats=page_stats)


def compute_page_level_ftsize_stats(
    page_stats: dict, textblocks: list[dict]
) -> None:
    '''
    Compute page level stats after computing lower levels (spans,
    lines and blocks) stats.

    :param page_stats: dict: a dict to collect statistics on the page.
    :param textblocks: list[dict]: the list of non-white and non-empty
        text block dicts.
    '''

    # Build a page's 'txtlen_ftsize_tuples' list
    # Required to compute other synthetic statistical indicators
    # (font size median, mode and mean)
    page_stats['txtlen_ftsize_tuples'] = flatten_txtlen_ftsize_tuples_list(
        source_list_dict=textblocks,  # type: ignore
    )

    # Compute the page's 'txt_len' after cleaning out white spans
    page_stats['txt_len'] = sum(
        _block['txt_len'] for _block in textblocks  # type: ignore
    )

    # Compute the page's 'digit_count'
    page_stats['digit_count'] = sum(
        _block['digit_count'] for _block in textblocks  # type: ignore
    )

    # Per span stats

    # Compute char stats per spans in the page and add results
    # to keys 'char_count_per_span_avg' and 'char_count_per_span_med'
    compute_chars_stats_per_span(textdict=page_stats)

    # Per line stats

    # Compute char stats per line at page level
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=page_stats,
        item_list=[
            _line['txt_len']
            for _textblock in textblocks
            for _line in _textblock['lines']
        ],
        coll_elt_name='line',
        item_name='char_count',
    )

    # Compute spans stats per line at page level
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=page_stats,
        item_list=[
            len(_line['spans'])
            for _textblock in textblocks
            for _line in _textblock['lines']
        ],
        coll_elt_name='line',
        item_name='span_count',
    )

    # Per block stats

    # Compute char stats per block at page level
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=page_stats,
        item_list=[_textblock['txt_len'] for _textblock in textblocks],
        coll_elt_name='block',
        item_name='char_count',
    )

    # Compute spans stats per blocks at page level
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=page_stats,
        item_list=[_textblock['span_count'] for _textblock in textblocks],
        coll_elt_name='block',
        item_name='span_count',
    )

    # Compute lines stats per blocks at page level
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=page_stats,
        item_list=[len(_textblock['lines']) for _textblock in textblocks],
        coll_elt_name='block',
        item_name='line_count',
    )

    # Compute the median and mode font size for the page
    add_mode_median_mean_ftsize_to_txtdict(txtdict=page_stats)

    # Compute additional page level stats
    _compute_additional_page_level_stats(
        page_stats=page_stats,
        textblocks=textblocks,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
