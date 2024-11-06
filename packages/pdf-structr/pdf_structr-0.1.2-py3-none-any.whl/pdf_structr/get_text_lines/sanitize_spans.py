# sanitize_spans.py
'''
Module to store the spans sanitizer that intervenes once the spans
have been grouped into lines.
'''


import logging

from pymupdf import Rect  # type: ignore

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


###############################
# Common helper function
###############################


def _are_duplicates(
    current_span_text: str,
    previous_span_text: str,
    current_span_bbox: Rect,
    previous_span_bbox: Rect,
) -> bool:
    '''
    Test whether two spans are duplicate.
    '''
    return (
        previous_span_text == current_span_text
        and previous_span_bbox == current_span_bbox
    )


#####################
# Elaborate join spans and delete duplicates
# NOTE: does not work as expected because of the way the _x_delta
# is being computed (as a proportion of the size of the current span).
# Merges spans that should stay separate. The determination of the
# x_delta shall be made in consideration of the average char width
# at the font size or sthing similar.
#####################


def _need_to_be_joined(
    current_span: dict,
    current_span_x0: float,
    previous_span_x1: float,
) -> bool:
    '''
    Test whether two spans need to be joined.

    :returns: bool: True if they need to be joined and False otherwise.

    :param current_span: float: the current span (i.e. comes after
    previous_span; we're iterating back to front).

    :param current_span_x0: float: x0 of the current span.

    :param previous_span_x1: float: x1 of the previous span.

    '''
    # Compute the x_delta (float): x_gap below which two spans shall
    # be joined.
    _x_delta = current_span["size"] * 0.1
    return (current_span_x0 - previous_span_x1) < _x_delta


def _join_non_duplicate_close_spans(
    current_span: dict[str, int | float | str | tuple[float, float] | Rect],
    previous_span: dict[str, int | float | str | tuple[float, float] | Rect],
) -> dict[str, int | float | str | tuple[float, float] | Rect]:
    '''
    If two spans are closer than the x_gap and are not duplicate,
    joins them.

    :param current_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the current span in the loop of _sanitize_spans.

    :param previous_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the previous span in the loop of _sanitize_spans.
    '''
    # On occasion, spans may also be duplicated.
    # Let's check it
    if not _are_duplicates(
        current_span_text=current_span["text"],  # type: ignore
        previous_span_text=previous_span["text"],  # type: ignore
        current_span_bbox=current_span["bbox"],  # type: ignore
        previous_span_bbox=previous_span["bbox"],  # type: ignore
    ):
        # spans are not duplicate => concatenate the text
        previous_span["text"] += current_span["text"]  # type: ignore

    # join bboxes Rectangles
    previous_span["bbox"] |= current_span["bbox"]  # type: ignore

    return previous_span


def _join_spans_delete_duplicates_acmb(
    line_spans: list[
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ],
    idx: int,
    current_span: dict[str, int | float | str | tuple[float, float] | Rect],
    previous_span: dict[str, int | float | str | tuple[float, float] | Rect],
) -> None:
    '''
    Check if the spans need to be concatenated (spans separated by less than
    the x_delta). If so, concatenates and extend the bbox, then updates the
    list.

    To be called from within a loop:

    ```python

    # sort the spans in the line ascending horizontally
    line_spans.sort(key=lambda span: span["bbox"].x0)  # type:ignore

    # join spans, delete duplicates
    # iterate back to front
    for _idx in range(len(line_spans) - 1, 0, -1):

        _join_spans_delete_duplicates_acmb(
            line_spans=line_spans,
            idx=_idx,
            current_span=line_spans[_idx],
            previous_span=line_spans[_idx - 1],
            # 10% of the fontsize
            x_delta=line_spans[_idx]["size"] * 0.1,  # type: ignore
        )

    return line_spans

    ```

    :returns: None because it is working straight on the list of spans.

    :param line_spans: list[
        dict[
            str,
            int
            | float
            | str
            | tuple[float, float]
            | Rect,
        ]
    ]: the list of spans.

    :param idx: int: the index number in the iteration.

    :param current_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the current span in the loop of _sanitize_spans.

    :param previous_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the previous span in the loop of _sanitize_spans.
    '''
    # if the x gap between two spans is below the x_delta, we
    # need to join the spans
    if _need_to_be_joined(
        current_span=current_span,
        current_span_x0=current_span["bbox"].x0,  # type: ignore
        previous_span_x1=previous_span["bbox"].x1,  # type: ignore
    ):

        # join the spans in the previous span
        line_spans[idx - 1] = _join_non_duplicate_close_spans(
            current_span=current_span,
            previous_span=previous_span,
        )

        # and delete the current_span
        # NOTE: deleting in the middle of a list
        del line_spans[idx]


#####################
# Simple delete duplicates
#####################


def _delete_duplicates(
    line_spans: list[
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ],
    idx: int,
    current_span: dict[str, int | float | str | tuple[float, float] | Rect],
    previous_span: dict[str, int | float | str | tuple[float, float] | Rect],
) -> None:
    '''
    Delete duplicates.

    :returns: None because it is working straight on the list of spans.

    :param line_spans: list[
        dict[
            str,
            int
            | float
            | str
            | tuple[float, float]
            | Rect,
        ]
    ]: the list of spans.

    :param idx: int: the index number in the iteration.

    :param current_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the current span in the loop of _sanitize_spans

    :param previous_span: dict[
        str, int | float | str | tuple[float, float] | Rect
    ]: the previous span in the loop of _sanitize_spans
    '''
    if _are_duplicates(
        current_span_text=current_span["text"],  # type: ignore
        previous_span_text=previous_span["text"],  # type: ignore
        current_span_bbox=current_span["bbox"],  # type: ignore
        previous_span_bbox=previous_span["bbox"],  # type: ignore
    ):

        # NOTE: deleting in the middle of a list...
        del line_spans[idx]


#####################
# Main API
#####################


def sanitize_spans(
    line_spans: list[
        # span
        dict[
            str,
            # flags and color
            int
            # size (fontsize), ascender and descender
            | float
            # font (fontname) and text
            | str
            # origin
            | tuple[float, float]
            # bbox
            | Rect,
        ]
    ],
):
    """
    Sort and join the spans in a re-synthesized line.

    The PDF may contain "broken" text with words cut into pieces.
    This function joins spans representing the particles and sorts them
    left to right.

    :returns: a list of sorted, and potentially cleaned-up spans.

    :param line_spans: list[
        dict[
            str,
            int
            | float
            | str
            | tuple[float, float]
            | Rect,
        ]
    ]: the list of spans in the current line.
    """
    # sort the spans in the line ascending horizontally
    line_spans.sort(key=lambda _span: _span["bbox"].x0)  # type:ignore

    # delete duplicates
    # iterate back to front so that we can delete spans
    for _idx in range(len(line_spans) - 1, 0, -1):

        # NOTE: not is use; needs to be though over
        # and probably refactored.
        # _join_spans_delete_duplicates_acmb(
        #     line_spans=line_spans,
        #     idx=_idx,
        #     current_span=line_spans[_idx],
        #     previous_span=line_spans[_idx - 1],
        # )
        _delete_duplicates(
            line_spans=line_spans,
            idx=_idx,
            current_span=line_spans[_idx],
            previous_span=line_spans[_idx - 1],
        )

    # Add a `span_no_in_line_x0` key to each span
    for _idx, _span in enumerate(line_spans):
        _span['span_no_in_line_x0'] = _idx

    # NOTE: This is where we should compute statistics at line level
    # and even clip level

    return line_spans
