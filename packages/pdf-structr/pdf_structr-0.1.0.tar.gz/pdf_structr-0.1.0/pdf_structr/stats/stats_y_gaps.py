# stats_y_gaps.py
'''
Module to compute y_gaps stats on a page.
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


#####################
# y gaps stats
#####################


def _compute_and_append_line_y_gap_up(
    previous_text_line: dict[str, int | float | tuple | list],
    current_text_line: dict[str, int | float | tuple | list],
) -> dict:
    '''
    Compute the y gap between the top of the current span and the bottom
    of the previous one (y_gap_up). This y_gap_up is generally negative
    in a top-left space. However, if the current line overlaps with the
    previous one (or if the lines have not been ordered by x0), it may be
    positive.

    :returns: the current_text_line augmented with its y_gap_up to previous
        line.

    :param previous_text_line: dict: the previous line in the list of lines.
    :param current_text_line: dict: the current line in the list of lines.
    :param y_gaps_down: list: the list of y_gaps.
    '''
    # Compute the y gap between the current text line and the previous one
    _y_gap_up: int = round(
        previous_text_line['bbox'][3]  # type: ignore
        - current_text_line['bbox'][1]  # type: ignore
    )

    # Append it under key y_gap_up to the line's dict
    current_text_line['y_gap_up'] = _y_gap_up

    # return the current
    return current_text_line


def compute_and_append_lines_gap_up(
    textlines: list[dict[str, int | float | tuple | list]]
):
    '''
    Sort the lines then, for each line, computes the y_gap between the
    y gap between the top of the current span and the bottom
    of the previous one (y_gap_up). This y_gap_up is generally negative
    in a top-left space. However, if the current line overlaps with the
    previous one (or if the lines have not been ordered by x0), it may be
    positive.

    :param textlines: list[dict[str, int | float | tuple | list]]: a list
        of lines to which the 'block_no' has been added.
    '''
    # compute the lines y_gaps up and save them to the lines
    # -----------------------------------------------------
    # sort the lines by block number, y0 and x0
    textlines.sort(
        key=lambda _line: (_line['block_no'], _line['y0'], _line['x0'])
    )
    # Declare a new line's dict
    _textlines: list[dict[str, int | float | tuple | list]] = []
    # Initialize it with the first line
    _textlines.append(textlines[0])
    # initialize the first line (y_gap_up is `-y0``)
    _textlines[0]['y_gap_up'] = -_textlines[0]['bbox'][1]  # type: ignore
    # iterate the remaining textlines and append them the y_gap_up
    _textlines.extend(
        _compute_and_append_line_y_gap_up(
            previous_text_line=_textlines[_idx - 1],
            current_text_line=_textline,
        )
        for _idx, _textline in enumerate(_textlines[1:], 1)
    )

    return _textlines


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
