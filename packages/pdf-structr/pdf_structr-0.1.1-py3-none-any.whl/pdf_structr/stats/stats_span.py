# stats_span.py
'''
Module encapsulating spans level data collection and analysis for
page, blocks and lines stats.
'''

# import functools
import logging

from pdf_structr.get_text_lines.make_spans_list import (
    is_white,
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
# Span(s) level computations
#####################


def _extract_span_text_and_length(
    span: dict,
    page_stats: dict,
) -> tuple[str, int]:
    '''
    Returns a span's text and text length and populates its length before
    assessing whether it is a white span into the page_stats dict.

    :param span: the span from which extraction is made.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''
    # Compute the span's text length
    _span_txt: str = span['text']
    _txt_len: int = len(_span_txt)

    # Update the page's charcount before excluding white spans
    page_stats['txt_len_bef_cleaning'] += _txt_len

    return _span_txt, _txt_len


def _count_digits_in_span_text(
    text: str, length: int, page_stats: dict
) -> int:
    '''
    Counts and returns the number of digits in a string.
    '''
    if text.isnumeric():
        page_stats['digit_span_count'] += 1
        return length

    if text.isalpha():
        return 0

    return sum(1 if char.isdigit() else 0 for char in text)


#####################
# Span in a line where there are several spans
#####################


def compute_span_length_ftsize_digitcount(
    span: dict,
    page_stats: dict,
) -> tuple[int, float]:
    '''
    Extract the span's length and font size from the current span,
    extracts the number of digits in the string from the current span,
    add the length and the number of digits as keys to the span's dict
    and returns a tuple _txt_len - font size.

    Mark the span at txt_len == 0 if white span.

    :returns: a tuple font length - font size.

    :param page_stats: dict:
    :param textblock: dict:
    :param line: dict:
    :param span: dict:
    '''
    # Extract the span's text and text length
    _span_txt, _txt_len = _extract_span_text_and_length(
        span=span, page_stats=page_stats
    )

    # Mark white spans
    if is_white(_span_txt) or _txt_len == 0:
        span['txt_len'] = 0
        span['digit_count'] = 0
        return (0, 0)

    # Else (passed-in span is not white)
    span['txt_len'] = _txt_len
    span['digit_count'] = _count_digits_in_span_text(
        span['text'],
        _txt_len,
        page_stats,
    )

    return (_txt_len, span['size'])


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
