# stats_line.py
'''
Module encapsulating lines level data collection and analysis for
page, blocks and lines stats.
'''

# import functools
import logging

from pdf_structr.stats.stats_lib import (
    add_mode_median_mean_ftsize_to_txtdict,
    add_stat_keys_to_textdict,
    compute_chars_stats_per_span,
)
from pdf_structr.stats.stats_span import (
    compute_span_length_ftsize_digitcount,
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
# Line level computations
#####################


def _update_line_dict_keys(line: dict, textblock: dict) -> dict:
    '''
    Add the block number (key and value) as well as new keys for the
    font size median and mode and text length to the passed-in line dict.

    :return: the passed-in line dict as updated with the additional new
        stats keys.

    :param line: dict: the current line in the textblock.
    :param textblock: dict: the current textblock.
    '''
    # Add the block_no to the line
    line['block_no'] = textblock['number']

    _line: dict = add_stat_keys_to_textdict(textdict=line)

    return _line


def _clean_up_empty_spans(line: dict) -> dict:
    '''
    Deletes the empty spans from the spans list and the len-size tuples
    and returns the line.

    :param line: dict: the current line dict.
    '''
    # Delete white spans from both the lists of txt len - ft size tuples
    # and the list of spans
    line['txtlen_ftsize_tuples'] = [
        _len_ftsize_tup
        for _len_ftsize_tup in line['txtlen_ftsize_tuples']
        if _len_ftsize_tup[0] != 0
    ]
    line['spans'] = [_span for _span in line['spans'] if _span['txt_len'] != 0]

    return line


# NOTE: This is the key re-usable function to compute stats at line level
# in the write package.
# Needs to be refactored.
def _compute_line_spans_stats(line: dict, page_stats: dict) -> dict:
    '''
    Iterates on the spans in a line to update the txt_len keys in the spans
    and in the line's dicts and creates a list of tuples txt length - font size
    per spans that it appends to the line's "txtlen_ftsize_tuples" list.

    Deletes the white spans, compute the line's txt_len and the font size
    median and mode.

    Returns the modified line dict.

    :param line: dict: the current line dict.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''
    # Create text length - font size tuple for each span in the line and store
    # them in a list
    line['txtlen_ftsize_tuples'] = [
        compute_span_length_ftsize_digitcount(
            span=_span,
            page_stats=page_stats,
        )
        for _span in line['spans']
    ]

    # Delete white spans from both the lists of txt len - ft size tuples
    # and the list of spans
    _line: dict = _clean_up_empty_spans(line=line)

    if _line['spans']:
        # Update the line's txt_len
        _line['txt_len'] = sum(_span['txt_len'] for _span in line['spans'])

        # Update the line's digits length
        _line['digit_count'] = sum(
            _span['digit_count'] for _span in line['spans']
        )

        # Update the line's digit spans count
        _line['digit_span_count'] = sum(
            1
            for _span in line['spans']
            if _span['digit_count'] == _span['txt_len']
        )

        # Update the span_count excluding white spans
        page_stats['span_count'] += len(_line['spans'])

        # Compute chars stats per spans in the line and add results
        # to keys 'char_count_per_span_avg' and 'char_count_per_span_med'
        compute_chars_stats_per_span(textdict=_line)

        # Compute the line median and mode font size
        return add_mode_median_mean_ftsize_to_txtdict(txtdict=_line)

    else:
        return _line


def augment_line_and_spans(
    line: dict,
    textblock: dict,
    page_stats: dict,
) -> dict:
    '''
    Adds the block number (key and value) to the passed-in line dict
    as well as new keys to the line dict to store the font size median
    and mode and the line's text length.

    Then calls _compute_line_spans_stats() to compute the corresponding
    the corresponding values in the spans of the passed-in line.

    :param line: dict: the current line.
    :param textblock: dict: the current textblock.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''
    _line: dict = _update_line_dict_keys(line=line, textblock=textblock)

    # Update the page's spans count before excluding white lines
    page_stats['span_count_bef_cleaning'] += len(_line['spans'])

    # Iterate the spans and amend the dicts
    return _compute_line_spans_stats(line=_line, page_stats=page_stats)


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
