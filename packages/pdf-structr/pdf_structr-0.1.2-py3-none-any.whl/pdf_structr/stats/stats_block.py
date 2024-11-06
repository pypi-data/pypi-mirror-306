# stats_block.py
'''
Module encapsulating the computation of stats at block level.
'''

# import functools
import logging

from pdf_structr.stats.stats_lib import (
    add_mode_median_mean_ftsize_to_txtdict,
    add_stat_keys_to_textdict,
    compute_chars_stats_per_span,
    compute_item_median_and_mean_per_elt_in_collection,
    flatten_txtlen_ftsize_tuples_list,
)
from pdf_structr.stats.stats_line import (
    augment_line_and_spans,
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
# Dict preparation
#####################


def _update_block_dict_keys(textblock: dict) -> dict:
    '''
    Add new keys to compute block level stats as well as new keys for the
    font size median and mode and text length to the passed-in textblock
    dict.

    :return: the passed-in textblock dict as updated with the additional new
        stats keys.

    :param textblock: dict: the current textblock.
    '''
    _line: dict = add_stat_keys_to_textdict(textdict=textblock)

    # Add a span_count key to the blocks dict
    textblock['char_count_per_line_avg'] = 0
    textblock['char_count_per_line_med'] = 0
    textblock['span_count_per_line_avg'] = 0
    textblock['span_count_per_line_med'] = 0
    textblock['span_count'] = 0

    return _line


#####################
# Data collection
#####################


def _collect_and_clean_lines_data(
    textblock: dict,
    page_stats: dict,
) -> None:
    '''
    Update the block's line by making the font size stats computation
    at line's level, deleting white spans and white lines.

    :param textblock: dict: the current textblock dict.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''

    # ----------------------------------------------
    # 1. Iterate and go down into the lines
    # ----------------------------------------------

    # iterate the lines, delete white spans, build lists of txt len - ft
    # size tuples for each span in each line and compute median and mode font
    # size for each line
    textblock['lines'] = [
        augment_line_and_spans(_line, textblock, page_stats)
        for _line in textblock['lines']
    ]

    # ----------------------------------------------
    # 2. Delete white lines
    # ----------------------------------------------

    textblock['lines'] = [
        _line for _line in textblock['lines'] if _line['spans']
    ]


#####################
# Statistics computation
#####################


def _compute_chars_stats_for_block(textblock: dict) -> None:
    '''
    Computes the text length for the block.
    Computes the average and median characters count
    per line included in the block.

    :param textblock: dict: the current textblock dict.
    '''
    _lines_txtlen_list: list[int] = [
        _line['txt_len'] for _line in textblock['lines']
    ]

    # Update the textblock 'txt_len'
    textblock['txt_len'] = sum(_lines_txtlen_list)

    # Update the textblock 'digit_count'
    textblock['digit_count'] = sum(
        _line['digit_count'] for _line in textblock['lines']
    )

    # Compute char stats per spans in the block and add results
    # to keys 'char_count_per_span_avg' and 'char_count_per_span_med'
    compute_chars_stats_per_span(textdict=textblock)

    # Compute char stats per line in the block and add results to keys
    # 'char_count_per_line_avg' and 'char_count_per_line_med'
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=textblock,
        item_list=_lines_txtlen_list,
        coll_elt_name='line',
        item_name='char_count',
    )


def _update_block_span_counts(
    textblock: dict,
    block_span_count_per_line_list: list[int],
):
    '''
    Update the textblock 'span_count' and 'digit_span_count' (i.e. the number
    of spans composed of digit for the block).

    :param textblock: dict: the current textblock dict.
    :param block_span_count_per_line_list: list[int]: a list of int,
        where each int the spans' count in one of the line of the block
    '''
    # Update the textblock 'span_count'
    textblock['span_count'] = sum(block_span_count_per_line_list)

    # Update the line's digit spans count
    textblock['digit_span_count'] = sum(
        _line['digit_span_count'] for _line in textblock['lines']
    )


def _compute_spans_stats_for_block(textblock: dict) -> None:
    '''
    Computes the spans count for the block.

    Computes the average and median spans count per line included in the block.

    :param textblock: dict: the current textblock dict.
    '''
    # Make a list of the spans' length in the block
    _block_span_count_per_line_list = [
        len(_line['spans']) for _line in textblock['lines']
    ]

    # Update the block spans count and digit_span_count (i.e. the number
    # of spans composed of digit for the block)
    _update_block_span_counts(
        textblock=textblock,
        block_span_count_per_line_list=_block_span_count_per_line_list,
    )

    # Update the textblock 'span_count_per_line_avg' and
    # 'span_count_per_line_med'
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=textblock,
        item_list=_block_span_count_per_line_list,
        coll_elt_name='line',
        item_name='span_count',
    )


def _compute_spans_and_chars_stats_for_block(textblock: dict) -> None:
    '''
    Computes char stats for the block (text length and char per line
    median and average).
    Computes the average and median characters count
    per spans included in the block.
    Computes spans stats for the block.

    :param textblock: dict: the current textblock dict.
    '''
    _compute_chars_stats_for_block(textblock)
    _compute_spans_stats_for_block(textblock)


def _compute_stats_on_blocks_subelements(
    textblock: dict,
    page_stats: dict,
) -> dict:
    '''
    Computes stats on text blocks subelements once they have been enriched
    by _collect_and_clean_lines_data.

    :returns: the text block.

    :param textblock: dict: the current textblock dict.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''

    # ----------------------------------------------
    # 1. Flatten the list of (txt len - ft size) tuples
    # ----------------------------------------------

    # Concatenate and flatten the lines' lists of txt len - ft size
    # tuples and store it under the block's "txtlen_ftsize_tuples"
    # key
    textblock['txtlen_ftsize_tuples'] = flatten_txtlen_ftsize_tuples_list(
        source_list_dict=textblock['lines'],
    )

    # ----------------------------------------------
    # 2. Update the page level line count (at this stage, excluding
    # white lines)
    # NOTE: should be done at a later stage
    # ----------------------------------------------

    page_stats['line_count'] += len(textblock['lines'])

    # ----------------------------------------------
    # 3. Compute block level stats on spans and chars
    # ----------------------------------------------

    _compute_spans_and_chars_stats_for_block(textblock)

    # ----------------------------------------------
    # 4. Compute ft_size_med and ft_size_mod for the textblock
    # ----------------------------------------------

    return add_mode_median_mean_ftsize_to_txtdict(txtdict=textblock)


def _compute_stats_blocks_subelements_or_return_white_block(
    textblock: dict,
    page_stats: dict,
) -> dict:
    '''
    Computes stats on text blocks subelements once they have been enriched
    by _collect_and_clean_lines_data or returns the white block.

    :returns: the text block.

    :param textblock: dict: the current textblock dict.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''
    # If there is something in the lines, compute stats on subelements
    # contained in the block
    if textblock['lines']:

        return _compute_stats_on_blocks_subelements(
            textblock=textblock,
            page_stats=page_stats,
        )

    # Else return the white textblock
    return textblock


#####################
# Data collection and statistics computation
#####################


def _collect_lines_txtlen_ftsize_and_compute_block_ftsize_stats(
    textblock: dict,
    page_stats: dict,
) -> dict:
    '''
    Iterates on the lines in a block to get their spans text length and
    font size, compute font size stats at line level, and then compute
    stats at the block level.

    :returns: the textblock, augmented with stats.

    :param textblock: dict: the current textblock dict.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''

    # ----------------------------------------------
    # 1. Compute the stats IN subelements
    # ----------------------------------------------

    _collect_and_clean_lines_data(textblock=textblock, page_stats=page_stats)

    # ----------------------------------------------
    # 2. Compute block level stats ON subelements
    # ----------------------------------------------

    return _compute_stats_blocks_subelements_or_return_white_block(
        textblock=textblock,
        page_stats=page_stats,
    )


#####################
# Main API
#####################


def augment_block_and_subdicts(
    textblock: dict,
    page_stats: dict,
) -> dict:
    '''
    Augment the block with keys for the computation of the
    its textlength and font size median and mode, then iterates
    on the lines of the block and calls _augment_line_and_spans() to make
    the computations.

    If all the lines in the text blocks are empty or white, return with
    adding block level stats.

    :param textblock: dict: the current text block.

    :param page_stats: dict: a dict to collect statistics on the page.
    '''

    # ----------------------------------------------
    # 1. Update some keys and values
    # ----------------------------------------------

    # Update the textblock dict keys for further processing
    _textblock: dict = _update_block_dict_keys(textblock)

    # Update the page's lines count before excluding white lines
    page_stats['line_count_bef_cleaning'] += len(_textblock['lines'])

    # ----------------------------------------------
    # 1. Compute statistics
    # ----------------------------------------------

    return _collect_lines_txtlen_ftsize_and_compute_block_ftsize_stats(
        textblock=_textblock, page_stats=page_stats
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
