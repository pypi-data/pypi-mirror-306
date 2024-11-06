# stats_lib.py
'''
Module encapsulating common functions for the other stats modules
including in particular the core median and mode font size functions.
'''


import itertools
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
# Generic text dict keys updater
#####################


def add_stat_keys_to_textdict(textdict: dict) -> dict:
    '''
    Add a series of stats dict keys to the passed-in textdict (line
    or text block) to store the statistics that are going to be
    computed at line and block levels.

    :param textdict: dict: a line or block dict extracted by pymupdf.
    '''
    textdict['txt_len'] = 0
    textdict['txtlen_ftsize_tuples'] = []
    textdict['ft_size_med'] = 0
    textdict['ft_size_mod'] = 0
    textdict['ft_size_mod_2nd'] = 0
    textdict['ft_sizes_count'] = 0
    textdict['char_count_per_span_avg'] = 0
    textdict['char_count_per_span_med'] = 0
    textdict['digit_count'] = 0
    textdict['digit_span_count'] = 0

    return textdict


#####################
# Generic mode and median font size calculation (for lines and blocks)
#####################


def _compute_median_mean_ftsize_when_several_fntsizes(
    txtdict: dict,
    size_len_list: list[tuple[int, float]],
    half_txtdict_len: float,
) -> dict:
    '''

    Computes the median and mean font size and appends it to the dict.

    :return: the passed-in line, text block or page_stats dict after
        update of its font size modes and median.

    :param txtdict: dict: a line, a text block or a page stats dict.
    :param size_len_list: list[tuple[int, float]]: the font size - text length
        tuples list, compounded and ordered by text length, ascending.
    :param half_txtdict_len: float: half the textdict length (in characters).
    '''
    # Compute the page font size mean
    txtdict['ft_size_mean'] = np.average(
        a=[  # type: ignore
            _ftsize[0] for _ftsize in size_len_list  # type: ignore
        ],
        weights=[  # type: ignore
            _txt_len[1] for _txt_len in size_len_list  # type: ignore
        ],
    )

    # If the sum of the chars at the two most frequent fontsizes exceeds half
    # the line's length, we also have the median
    if (size_len_list[-1][1] + size_len_list[-2][1]) >= half_txtdict_len:
        txtdict['ft_size_med'] = size_len_list[-2][0]
        return txtdict

    # Else:
    # Compute the median font size for the line using numpy
    # Explode values of _size_len_tup_list into 1D np array
    txtdict['ft_size_med'] = np.median(
        np.concatenate(
            [np.repeat(_len, _size) for _size, _len in size_len_list]
        )
    )

    return txtdict


def _compute_median_mean_ftsize_to_txtdict(
    txtdict: dict,
    size_len_list: list[tuple[int, float]],
) -> dict:
    '''
    Computes the median and mean font size and appends it to the dict.

    :return: the passed-in line, text block or page_stats dict after
        update of its font size modes and median.

    :param txtdict: dict: a line, a text block or a page stats dict.
    :param size_len_list: list[tuple[int, float]]: the font size - text length
        tuples list, compounded and ordered by text length, ascending.
    '''
    # Compute half the line's text length
    _half_txtdict_len: float = txtdict['txt_len'] / 2

    # If the count of the chars at the most frequent fontsize
    # exceeds half the line's length, we've got the median
    if size_len_list[-1][1] >= _half_txtdict_len:
        txtdict['ft_size_med'] = size_len_list[-1][0]
        txtdict['ft_size_mean'] = size_len_list[-1][0]
        return txtdict

    # Else if several font sizes in the txtdict
    return _compute_median_mean_ftsize_when_several_fntsizes(
        txtdict=txtdict,
        size_len_list=size_len_list,
        half_txtdict_len=_half_txtdict_len,
    )


def _make_ftsizes_aggregate_txtlen_list(
    txtdict: dict,
) -> list[tuple[int, float]]:
    '''
    Aggregate the text length sharing the same fontsizes and return a
    list of (text length - font size) tuples ordered in ascending
    order of text length.

    :return: list[tuple[int, float]]: a list of (text length - font size)
        tuples ordered in ascending order of text length.

    :param txtdict: dict: a line, a text block or a page stats dict.
    '''
    # Sort the list of "text length - font size" tuples by font sizes
    # in ascending order
    txtdict['txtlen_ftsize_tuples'].sort(key=lambda tup: tup[1])

    # Sum up (text) lengths of the tuples with the same font size
    # into a size_dict
    _size_dict: dict[float, int] = {}
    for _len_size_tup in txtdict['txtlen_ftsize_tuples']:
        _size_dict[_len_size_tup[1]] = (
            _size_dict.get(_len_size_tup[1], 0) + _len_size_tup[0]
        )

    # Sort by length and convert the _size_dict into a list of
    # text length - font size tuples
    return sorted(_size_dict.items(), key=lambda item: item[1])  # type: ignore


def _compute_mode_median_mean_ftsize_to_txtdict(txtdict: dict) -> dict:
    '''
    Computes the mode and the median font size for a line or a block
    and returns the corresponding dict.

    :return: the passed-in line, text block or page_stats dict after
        update of its font size modes and median.

    :param txtdict: dict: a line, a text block or a page stats dict.
    '''
    # Aggregate the text length of the subdict sharing the same font sizes
    # into a list of (text length - font size) tuples ordered in ascending
    # order of text length
    _size_len_list: list[tuple[int, float]] = (
        _make_ftsizes_aggregate_txtlen_list(txtdict)
    )

    # Save the count of unique fontsizes in the dict
    txtdict['ft_sizes_count'] = len(_size_len_list)

    # Compute font size modes (1st and 2nd)
    txtdict['ft_size_mod'] = _size_len_list[-1][0]
    if len(_size_len_list) > 1:
        txtdict['ft_size_mod_2nd'] = _size_len_list[-2][0]

    # Compute median and mean font size
    return _compute_median_mean_ftsize_to_txtdict(
        txtdict=txtdict,
        size_len_list=_size_len_list,
    )


def add_mode_median_mean_ftsize_to_txtdict(txtdict: dict) -> dict:
    '''
    Adds the mode, the median and the mean font size for a line or a block
    to the coresponding dict and returns the dict.

    :return: the passed-in line or block after update, as the case may be,
        of its font size mode and median.

    :param txtdict: dict: a line or a block.
    '''
    # -------------------------------------
    # If all the spans have been deleded from the line or all the lines
    # have been deleted from the block, return the line or the block
    # without making any calculation
    if not txtdict['txtlen_ftsize_tuples']:
        return txtdict

    # -------------------------------------
    # Else: we have at least one span in the line or one line in the block
    # Sort the len-size tuples by size
    return _compute_mode_median_mean_ftsize_to_txtdict(txtdict=txtdict)


#####################
# Generic flattener txtlen_ftsize_tuples lists
#####################


def flatten_txtlen_ftsize_tuples_list(
    source_list_dict: list[tuple[int, float]],
) -> list[tuple[int, float]]:
    '''
    Flattens the 'txtlen_ftsize_tuples' lists contained in each
    of the source dict (lines or blocks) and returns a flattened list.

    :return: a faltten

    :param source_list_dict: list[dict]: a list of lines or blocks with
        a 'txtlen_ftsize_tuples' key populated with a list of tuples
        (txt length, font size) corresponding to the underlying spans.
    '''
    return list(
        itertools.chain.from_iterable(  # type: ignore
            _source_dict['txtlen_ftsize_tuples']  # type: ignore
            for _source_dict in source_list_dict
        )
    )


#####################
# Generic median and mean computer
#####################


def compute_item_median_and_mean_per_elt_in_collection(
    textdict: dict,
    item_list: list[int],
    coll_elt_name: str,
    item_name: str,
) -> None:
    '''
    Computes the mean and the median items per the passed-in collection
    elements. Items may be txt length, spans count, lines count,
    blocks count, etc. Collection elements may be spans, lines, blocks,
    pages, etc.

    :param textdict: dict: the dict where the stats computation results
        are going to be stored (line, block or page).
    :param item_list: list[int]: a list of int corresponding to the
        items count (text length, span counts, line counts, block counts,
        etc.) for each of the elements of the collection for which
        the stats are computed (ex. spans, lines, blocks, pages, etc.).
    :param coll_elt_name: str: the name of the elements of the collection
        per which the statistics are computed. Ex. span, line, block, page,
        etc.
    :param item_name: str: the name of the items of the collection
        on which the statistics are computed. Ex. span_count in lines, blocks,
        pages; char_count in spans, lines, blocks, pages, etc.
    '''
    # Items per collection element stats
    # Update the textdict['items_per_line_avg']
    textdict[f'{item_name}_per_{coll_elt_name}_avg'] = np.mean(item_list)
    # Update the textdict['items_per_line_med']
    textdict[f'{item_name}_per_{coll_elt_name}_med'] = np.median(item_list)


#####################
# Generic char count stats in spans for upper levels dict (lines, blocks
# and pages)
#####################


def compute_chars_stats_per_span(textdict: dict) -> None:
    '''
    Computes char per span stats for upper levels dict (line, block or page).

    :param textdict: dict: the upper level dict (line, block or page).
        Must have 'txtlen_ftsize_tuples' key storing a list of
        spans' (text length - ft size) tuples.
    '''
    # Char per spans stats
    spans_txtlen_list: list[int] = [
        txtlen_ftsize_tup[0]
        for txtlen_ftsize_tup in textdict['txtlen_ftsize_tuples']
    ]

    # Call the abstract char per span stats function
    compute_item_median_and_mean_per_elt_in_collection(
        textdict=textdict,
        item_list=spans_txtlen_list,
        coll_elt_name='span',
        item_name='char_count',
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
