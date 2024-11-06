# augment.py
'''
Module encapsulating:
- the white spans, lines and blocks filtering;
- the augmentation of the spans with data about their content.
'''


import logging
import string

from pdf_structr.utils.utils import (
    compute_container_bbx_from_contained_dict_bbxs,
)

# from pdf_struct.mo_utils.timer import count_and_avg_timer

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
# Helper
#####################


def _filter_white_subdicts_out(
    main_list: list[dict],
    container_list_key: str,
) -> list[dict]:
    '''
    Filters out containers (lines or blocks) which list of subdicts
    is empty out of a list of containers.

    :param main_list: list[dict]: the main list to be filtered (ex.
        a list of blocks or a list of lines in a block).

    :param container_list_key: str: the keys to get the list to
        assess (ex. 'spans' to filter out lines which do not contain
        any spans and 'lines' to filter out blocks which do not contain
        any lines).

    '''
    return [
        # ex. line
        _container
        # ex. for _line in textblock['lines']
        for _container in main_list
        # ex. if _line['spans'] => if the line contains spans
        if _container[container_list_key]
    ]


#####################
# Spans
#####################


def _count_digits_in_span_text(text: str, length: int) -> int:
    '''
    Counts and returns the number of digits in a string.
    '''
    if text.isnumeric():
        return length

    if text.isalpha():
        return 0

    return sum(1 for char in text if char.isdigit())


def _punct_count(text: str) -> int:
    '''
    Count the punctuations in a text.
    '''
    _punct_set: set = set(string.punctuation)
    return sum(1 for char in text if char in _punct_set)


def _augment_span(span: dict) -> dict:
    '''
    Adds some statistics to the span
    '''
    # text non stripped
    _span_text: str = span['text']
    _span_len: int = len(_span_text)

    # text stripped
    _span_text_stripped: str = _span_text.strip()
    _span_length_stripped: int = len(_span_text_stripped)

    # text right stripped
    _span_text_right_stripped: str = _span_text.rstrip()
    _span_length_right_stripped: int = len(_span_text_right_stripped)

    # Update the span
    span['txt_len'] = _span_len
    span['trail_ws'] = _span_len - _span_length_right_stripped
    span['inner_ws'] = sum(not c.isspace() for c in _span_text_stripped)
    span['punct_count'] = _punct_count(_span_text_stripped)
    span['digit_count'] = _count_digits_in_span_text(
        text=_span_text_stripped,
        length=_span_length_stripped,
    )

    # NOTE: need to round the drawings also
    # This might cause some trouble ahead if rounding not
    # made at drawings level
    span['bbox'] = tuple((round(_coord, 3) for _coord in span['bbox']))

    return span


def _iterate_augment_and_clean_spans(
    line: dict[str, int | float | tuple | list],
) -> dict[str, int | float | tuple | list]:
    '''
    Iterates the lines in the textblock, augment the spans in the line
    and filter out white spans (i.e. spans containing no char or only
    white space spans).

    :param line: dict[str, int | float | tuple | list]: a text
        block in the list of blocks.
    '''

    # ----------------------------------------------
    # 1. Iterate and go down into the spans
    # ----------------------------------------------

    # iterate the spans, delete white spans, add keys to the spans
    # dict with information on their content (white space, punct, digits, etc.)
    line['spans'] = [
        _augment_span(span=_span)
        for _span in line['spans']  # type: ignore
        if not _span['text'].isspace()
    ]

    line['txt_len'] = sum(
        _span['txt_len'] for _span in line['spans']  # type: ignore
    )

    return line


#####################
# Lines
#####################


def _iterate_lines_filter_white_lines(
    textblock: dict[str, int | float | tuple | list],
) -> dict[str, int | float | tuple | list]:
    '''
    Iterates the lines in the textblock, augment and cleans the spans
    in the line and filter out white lines (i.e. lines containing no
    spans).

    :param textblock: dict[str, int | float | tuple | list]: a text
        block in the list of blocks.
    '''

    # ----------------------------------------------
    # 1. Iterate and go down into the lines
    # ----------------------------------------------

    # iterate the lines, delete white spans, add keys to the spans
    # dict with information on their content (white space, punct, digits, etc.)
    textblock['lines'] = [
        _iterate_augment_and_clean_spans(line=_line)
        for _line in textblock['lines']  # type: ignore
    ]

    # ----------------------------------------------
    # 2. Delete white lines from the block 'lines' list
    # ----------------------------------------------

    textblock['lines'] = _filter_white_subdicts_out(
        main_list=textblock['lines'],  # type: ignore
        container_list_key='spans',
    )

    # ----------------------------------------------
    # 3. Adjust the line's bbox to the size of the remaining spans
    # ----------------------------------------------

    if textblock['lines']:
        textblock['lines'] = _reduce_containers_bbxs_to_contained_bbxs(
            containers=textblock['lines'],  # type: ignore
            subdict_key='spans',
        )

    return textblock


#####################
# Blocks
#####################


def _iterate_blocks_filter_img_blocks_out(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[dict[str, int | float | tuple | list]]:
    '''
    Iterate the blocks, filtering image blocks out, and iterate further down.

    :param blocks: list[dict[str, int | float | tuple | list]]: the list of
        blocks extracted from the page.
    '''
    return [
        _iterate_lines_filter_white_lines(
            textblock=_textblock,
        )
        for _textblock in blocks
        # only text block, no image block
        if _textblock['type'] == 0
    ]


def _reduce_containers_bbxs_to_contained_bbxs(
    containers: list[dict[str, int | float | tuple | list]],
    subdict_key: str,
) -> list[dict[str, int | float | tuple | list]]:
    '''
    Adjust the size of each container bbox to the size of its subelements.

    :param containers: list[dict[str, int | float | tuple | list]]: a list
        of blocks or lines.

    :param subdict_key: str: 'lines', if a list of blocks is passed or 'spans'
        if a list of lines is passed.

    '''
    for _container in containers:
        if _container[subdict_key]:
            _container['bbox'] = (
                compute_container_bbx_from_contained_dict_bbxs(
                    container=_container,
                    subdict_key=subdict_key,
                )
            )

    return containers


# @count_and_avg_timer(name='prep - clean_dicts_augment_spans')
def clean_dicts_augment_spans(
    blocks: list[dict[str, int | float | tuple | list]],
) -> list[dict[str, int | float | tuple | list]]:
    '''
    Cleans the dicts (blocks, lines and spans) by getting rid of
    image blocks as well as white blocks, lines and spans.

    Augments the spans with counts of their elements by type (digits,
    punctuation, white spaces, etc.).

    :param blocks: list[dict[str, int | float | tuple | list]]: the list of
        blocks extracted from the page.
    '''

    # Iterate on the blocks, filtering out the non-text blocks
    # and enrich the spans with data
    _textblocks: list[dict[str, int | float | tuple | list]] = (
        _iterate_blocks_filter_img_blocks_out(blocks=blocks)
    )

    # Get rid of white blocks
    _textblocks = _filter_white_subdicts_out(
        main_list=_textblocks,  # type: ignore
        container_list_key='lines',
    )

    # Reduce size of blocks for which white lines have been removed
    _textblocks = _reduce_containers_bbxs_to_contained_bbxs(
        containers=_textblocks,
        subdict_key='lines',
    )

    return _textblocks


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
