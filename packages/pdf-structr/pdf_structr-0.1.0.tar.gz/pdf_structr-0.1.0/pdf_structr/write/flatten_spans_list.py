# flatten_spans_list.py
'''
Module encapsulating the flattening of the spans' list
corresponding to a line (and eventually, a paragraph).
'''


import logging

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


###################################
# Spans list cleaning and flattening - shortcut
###################################


def _flatten_and_clean_spans_shortcut(
    formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ],
    prefix: str,
    suffix: str,
):
    '''
    Shortcut to clean the list of spans (a list of tuples at this stage)
    into a list of string chunks when the spans are all bold and italics,
    all bold or all italics.

    :param formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ]: the list of formatted spans' tuples.

    :param prefix: str: a prefix to apply to the line.

    :param suffix: str: a suffix to apply to the line.
    '''
    # Flatten the list, getting rid of all the spans prefixes and suffixes
    # along the way and adding a prefix and a suffix at the beginning and
    # end of the list of string chunks
    _flat_list = (
        [prefix]
        + [
            _str_chk
            for (_fspan, _ws) in formatted_spans_tuples_list
            for _str_chk in (
                '',
                *_fspan[1:-1],
                '',
                _ws * ' ',
            )
        ]
        + [suffix]
    )

    # Fix the end of the list (the last span might have a trailing
    # white space that needs to be extracted out of the formatting)
    _flat_list[-2] = ''
    _flat_list.append(' ')

    return _flat_list


###################################
# Spans list cleaning and flattening - complex with subfunctions
###################################


def _chop_off_prefix_only(
    flat_list: list[str],
    this_span: tuple[tuple[str, str, str, str, str, str, str], int],
) -> None:
    '''
    Chop off the prefix (when the suffix of the previous span was chopped off).

    :param flat_list: list[str]: the flat list of string chunks extracted
        from the list of formatted spans tuples.

    :param this_span: tuple: the current span to be flattened into the
        list of string chunks.

    '''
    flat_list.extend([*this_span[0][1:], this_span[1] * ' '])


def _flatten_span_difft_suf_pref(
    flat_list: list[str],
    prev_suff_chopped_off: bool,
    this_span: tuple[tuple[str, str, str, str, str, str, str], int],
) -> None:
    '''
    Flattens and cleans a span (as a tuple at this stage) that
    DOES NOT SHARE the same suffix-prefix as the following one.

    :param flat_list: list[str]: the flat list of string chunks extracted
        from the list of formatted spans tuples.

    :param prev_suff_chopped_off: bool: a boolean indicating whether the
        previous span was chopped off its suffix because this span
        has the same prefix (and accordingly, whether this span should
        be chopped off its prefix).

    :param this_span: tuple[tuple[str, str, str, str, str, str, str], int]:
        the current span to be flattened into the list of string chunks.

    '''

    # prev span's suffix not chopped off
    if not prev_suff_chopped_off:
        flat_list.extend([*this_span[0], this_span[1] * ' '])

    # prev span's suffix chopped off
    else:
        _chop_off_prefix_only(flat_list, this_span)


def _flatten_span_same_suf_pref(
    flat_list: list[str],
    prev_suff_chopped_off: bool,
    this_span: tuple,
) -> None:
    '''
    Flattens and cleans a span (as a tuple at this stage) that
    DOES SHARE the same suffix-prefix as the following one.

    :param flat_list: list[str]: the flat list of string chunks extracted
        from the list of formatted spans tuples.

    :param prev_suff_chopped_off: bool: a boolean indicating whether the
        previous span was chopped off its suffix because this span
        has the same prefix (and accordingly, whether this span should
        be chopped off its prefix).

    :param this_span: tuple[tuple[str, str, str, str, str, str, str], int]:
        the current span to be flattened into the list of string chunks.

    '''

    # the previons span's suffix has not been chopped off
    # => chop off this span's suffix only, not the prefix
    # and add a whitespace
    if not prev_suff_chopped_off:
        flat_list.extend([*this_span[0][:-1], this_span[1] * ' '])

    # the previons span's suffix has also been chopped off
    # => chop off this span's prefix and suffix and add a whitespace
    else:
        flat_list.extend([*this_span[0][1:-1], this_span[1] * ' '])


def _flatten_and_clean_first_spans(
    flat_list: list[str],
    prev_suff_chopped_off: bool,
    this_span: tuple[tuple[str, str, str, str, str, str, str], int],
    next_pref: str,
) -> bool:
    '''
    Handle one span at a time. Flattens any span not being the last span
    (i.e. first spans) in the list of formatted spans, getting rid of excess
    formatting suffixes and prefixes.

    Returns True if this span and the next one have the SAME suffix-
    prefix (=> this span's suffix is chopped off) or False if this
    span and the next one have DIFFERENT suffix-prefix (=> this span's
    suffix is not chopped off).

    :param flat_list: list[str]: the flat list of string chunks extracted
        from the list of formatted spans tuples.

    :param prev_suff_chopped_off: bool: a boolean indicating whether the
        previous span was chopped off its suffix because this span
        has the same prefix (and accordingly, whether this span should
        be chopped off its prefix).

    :param this_span: tuple[tuple[str, str, str, str, str, str, str], int]:
        the current span to be flattened into the list of string chunks.

    :param next_pref: str: the next span, to identify whether we need
        to chop off the suffix element from this span.

    '''
    # Difft suffix (this span) - prefix (next span)
    # --------------------------------------------

    if not this_span[0][-1] == next_pref:

        _flatten_span_difft_suf_pref(
            flat_list=flat_list,
            prev_suff_chopped_off=prev_suff_chopped_off,
            this_span=this_span,
        )

        return False

    # Same suffix (this span) - prefix (next span)
    # --------------------------------------------

    _flatten_span_same_suf_pref(
        flat_list=flat_list,
        prev_suff_chopped_off=prev_suff_chopped_off,
        this_span=this_span,
    )

    return True


def _clean_and_add_last_span_to_flat_list(
    flat_list: list[str],
    last_span: tuple,
    prev_suff_chopped_off: bool,
) -> None:
    '''
    Clean and adds the last span in the list. Handled differently
    because there is no following span to be compared with.

    :param flat_list: list[str]: the flat list of string chunks extracted
        from the list of formatted spans tuples.

    :param last_span: tuple[tuple[str, str, str, str, str, str, str], int]:
        the last span being flattened into the list of string chunks.

    :param prev_suff_chopped_off: bool: a boolean indicating whether the
        previous span was chopped off its suffix because this span
        has the same prefix (and accordingly, whether this span should
        be chopped off its prefix).

    '''
    # if the previous suffix was not chopped off
    if not prev_suff_chopped_off:
        flat_list.extend([*last_span[0], last_span[1] * ' '])

    # if the previous suffix was chopped off, chopp off
    # the prefix of this span
    else:
        _chop_off_prefix_only(
            flat_list,
            last_span,
        )


def _complex_flattening(
    formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ],
    span_count: int,
):
    '''
    Flattens the list of formatted spans (a list of tuples at this stage)
    into a list of string chunks when there is complex formatting involved
    (nesting of superscript, inline code, italics or bold).

    :param formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ]: the list of formatted spans' tuples.

    :param span_count: int: a 0-based count of the spans in the
        formatted_spans_tuples_list.

    '''
    _flat_list: list[str] = []
    # the formatted spans list
    _prev_suff_chopped_off: bool = False

    for _idx in range(0, span_count + 1):  # type: ignore

        # first spans
        if _idx < span_count:  # type: ignore
            _prev_suff_chopped_off = _flatten_and_clean_first_spans(
                flat_list=_flat_list,
                prev_suff_chopped_off=_prev_suff_chopped_off,
                this_span=formatted_spans_tuples_list[_idx],
                next_pref=formatted_spans_tuples_list[_idx + 1][0][0],
            )
            continue

        # Last span in the list
        _clean_and_add_last_span_to_flat_list(
            flat_list=_flat_list,
            last_span=formatted_spans_tuples_list[_idx],
            prev_suff_chopped_off=_prev_suff_chopped_off,
        )

    return _flat_list


###################################
# Spans list cleaning and flattening - main function
###################################


def flatten_and_clean_str_itr(
    formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ],
    span_count: int,
    bold_span_count: int,
    italics_span_count: int,
) -> list[str]:
    '''
    At this stage, formatted_spans_tuples_list is a list of
    2-tuples, each tuple containing a 7-string tuple and an int.

    The 7-string tuple correspond to the text content of the
    initial span (which is the central element str_tup[3]) and
    the other elements correspond to markdown formatting elements
    ('`' for mono, etc.).

    The int correspond to an optional whitespace that shall be
    added at the end of the string.

    This function extracts each element of each of the 7-string tuple,
    produce an optional white-space string element that it appends
    to the 7 str elements, and adds these 8 string chunks to a
    single list, which whill be returned by the function.

    Accordingly, the returning list is necessarily a multiple of 8.

    The first three elements of the list will be the first span's
    opening formatting elements (bold&italics, superscript, mono, in
    this order), the fourth element will be the first span's text content.

    The last four elements of the list will be the last span markdown closing
    elements (mono, superscrit, bold&italics) and an optional whitespace (in
    this order).

    Every 8-string chunks will represent a span. As soon as the line contains
    more than 1 span, this function and its subfunctions will have cleaned
    the "useless" markdown formatting elements (for instance, if two spans
    with the same bold&italics ('**_', '_**') formatting follow each other,
    the string element corresponding to the closing '_**' for the first span
    will have been deleted and replaced by an empty '' and the opening '**_'
    for the following span will have been deleted, so that the span can be
    concatenated as a single bold and italic element in markdown.

    The corresponding list will be appended to the line's str_iter
    attribute as a list of strings.

    :param formatted_spans_tuples_list: list[
        tuple[tuple[str, str, str, str, str, str, str], int]
    ]: the list of formatted spans' tuples.

    :param span_count: int: a 0-based count of the spans in the
        formatted_spans_tuples_list.

    :param bold_span_count: int: a 0-based count of the spans
        formatted in bold in the formatted_spans_tuples_list.

    :param italics_span_count: int: a 0-based count of the spans
        formatted in italics in the formatted_spans_tuples_list.

    '''

    # Shortcut if there is only one span in the line
    # ----------------------------------------------

    if span_count == 0:

        return [
            *formatted_spans_tuples_list[0][0],
            (formatted_spans_tuples_list[0][1] * ' '),
        ]

    # Shortcut if all the spans are bold and italics
    # ----------------------------------------------

    if all(
        [
            italics_span_count == span_count,
            bold_span_count == span_count,
        ]
    ):

        return _flatten_and_clean_spans_shortcut(
            formatted_spans_tuples_list=formatted_spans_tuples_list,
            prefix='**_',
            suffix='_**',
        )

    # Shortcut if all the spans in the line are italics
    # ----------------------------------------------

    if italics_span_count == span_count:

        return _flatten_and_clean_spans_shortcut(
            formatted_spans_tuples_list=formatted_spans_tuples_list,
            prefix='_',
            suffix='_',
        )

    # Shortcut if all the spans in the line are bold
    # ----------------------------------------------

    if bold_span_count == span_count:

        return _flatten_and_clean_spans_shortcut(
            formatted_spans_tuples_list=formatted_spans_tuples_list,
            prefix='**',
            suffix='**',
        )

    # If no shortcut applied, do a complex flattening
    # ----------------------------------------------

    return _complex_flattening(
        formatted_spans_tuples_list=formatted_spans_tuples_list,
        span_count=span_count,
    )


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
