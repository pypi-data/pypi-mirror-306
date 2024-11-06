# clust_rlb.py
'''
Module encapsulating functions making clusters of blocks
that appear to be 'row like block' (rlb).

A series of blocks appears to be row like when each block
contains more than one span, successive blocks contain
the same number of spans separated by a significant whitespace
and all the lines in the blocks appears to be on the same geometrical
line.
'''


import logging

from pdf_structr.tabs_clust.clustc_ho_trows import (
    group_items_by_clusters_of_consecutive_items_with_same_coll_count,
)
from pdf_structr.tabs_clust.rlb_lib import (
    are_blocks_likely_rows_in_same_table,
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
# Filter blocks
#####################


def _filter_blocks_by_spans_count(
    blocks: list[dict[str, int | float | tuple | list]],
    no_of_spans: int,
) -> list[dict[str, int | float | tuple | list]]:
    '''
    Function to filter blocks that contain more than a certain number of spans.

    NOTE: this is adequate on page 26 of the STIFF document where each block
    usually contains one single line which itself contains one single span.
    This filtering might however not be so adequate in document that are
    mainly composed of text paragraph text and where a single block may
    contain several lines, and each line several spans.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.)

    :param no_of_spans: int: number of spans that the blocks shall have to
        be retained.

    :param avg_char_width: float: the average char width on the page. NOTE:
        this average is average everything, including chars of different
        font sizes and names. Might be excessive, but gives a starting point
        to make proportional computation.
    '''

    # add a _bno index number to each block to keep track of their
    # sorting order
    for _idx, _block in enumerate(blocks):
        _block['_bno'] = _idx

    # filter blocks that are more than no_of_spans long
    return [
        _block
        for _block in blocks
        if _block['spans_count'] > no_of_spans  # type: ignore
    ]


#####################
# Make clusters
#####################


def make_rlb_clusters(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[list[dict[str, int | float | tuple | list]]]:
    '''
    Filters the blocks to keep only blocks that contain more than 2 spans
    and then try to group them into clusters of consecutive blocks with
    the same spans count (assuming that two blocks that contains the
    same number of spans might be a table).

    Returns a list of clusters, where each cluster is a group of blocks.

    :param blocks: list[dict[str, int | float | tuple | list]]:
        the list of text blocks as returned by `clean_dicts_augment_spans`
        and as augmented by the preliminary steps in `detect_tables`
        (i.e with white spans filtered out and spans' dicts augmented
        with digit_count, punct_count, etc.; blocks' dicts augmented
        with 'spans_count').

    '''

    # Keep only blocks that have more than 2 spans
    # NOTE: we might want to reduce it to more than 1 span
    _blocks_sup_2_spans: list[dict[str, int | float | tuple | list]] = (
        _filter_blocks_by_spans_count(
            blocks=blocks,
            no_of_spans=2,
        )
    )

    # Group the blocks by clusters of consecutive blocks with the same
    # spans' count.
    # Each cluster will be deemed a probable table.
    _blocks_clusters: list[list[dict[str, int | float | tuple | list]]] = (
        group_items_by_clusters_of_consecutive_items_with_same_coll_count(
            items=_blocks_sup_2_spans,
            are_items_likely_rows_in_same_table_fn=(
                are_blocks_likely_rows_in_same_table
            ),
        )
    )

    return _blocks_clusters


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
