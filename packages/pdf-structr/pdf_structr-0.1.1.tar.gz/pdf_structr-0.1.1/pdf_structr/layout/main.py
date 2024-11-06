# main.py
'''
Extracts the text layout from the page.
'''


import logging

import pymupdf  # type: ignore

from pdf_structr.layout.compute_zone_rects import (
    compute_horizontal_zones_rects,
    compute_vertical_zones_rects,
)
from pdf_structr.layout.extract_blocks_compnd_bb import (
    compute_page_blocks_compound_bbxes,
)
from pdf_structr.layout.extract_zones import (
    compute_horizontal_text_intertext_zones,
    compute_vertical_text_intertext_zones_within_text_zones,
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
# Adjust textblock bboxes to their real size
#####################


def adjust_textblocks_bboxes(
    textblocks: list[dict],
):
    '''
    Adjust the textblocks bboxes to the real size of the lines they contain.

    :param blocks: list[dict]: the list of blocks for the page.
    '''
    for _txtblock in textblocks:
        _block_bbox: list[float] = list(_txtblock['lines'][0]['bbox'])

        for _line in _txtblock['lines'][1:]:
            _line_bbox: list[float] = list(_line['spans'][0]['bbox'])

            # adjust the line's bboxes to the spans' bboxes
            for _span in _line['spans'][1:]:
                _span_bbox: tuple = _span['bbox']

                for _i in (
                    0,
                    1,
                ):
                    _line_bbox[_i] = min(_line_bbox[_i], _span_bbox[_i])
                for _i in (
                    2,
                    3,
                ):
                    _line_bbox[_i] = max(_line_bbox[_i], _span_bbox[_i])

                _line['bbox'] = tuple(_line_bbox)

            # adjust the block's bboxes to the lines' bboxes
            for _i in (
                0,
                1,
            ):
                _block_bbox[_i] = min(_block_bbox[_i], _line_bbox[_i])
            for _i in (
                2,
                3,
            ):
                _block_bbox[_i] = max(_block_bbox[_i], _line_bbox[_i])

            _txtblock['bbox'] = tuple(_block_bbox)


#####################
# Main
#####################


def extract_page_text_layout(
    page: pymupdf.Page,
    blocks: list[dict],
    page_stats: dict,
) -> dict[str, dict | list]:
    '''
    Returns a layout dict, composed of a dict (the page's mediabox)
    and five lists, detailling:
    - the outer limits of the compound blocks, text blocks and image blocks;
    - the horizontal text and intertext zones;
    - the vertical text and intertext zones;
    - the rectangles corresponding to the horizontal zones;
    - the rectangles corresponding to the vertical zones.

    :param page: pymupdf.Page: the current page.
    :param blocks: list[dict]: the list of blocks for the page.
    :param page_stats: dict: the page's stats dict.
    '''
    _layout_dict: dict = {}

    _layout_dict['page'] = {'bbox': page.mediabox}

    # Reduce the _textblocks to their real size since some lines and
    # spans have been deleted
    _textblocks: list[dict] = adjust_textblocks_bboxes(textblocks=blocks)

    # Compute page level bboxes for:
    # - all the blocks compounded
    # - only the text blocks compounded
    # - only the image blocks compounded
    # The corresponding bboxes are stored in the _stats_dict
    # Get the page's textblocks as a return value
    _textblocks = compute_page_blocks_compound_bbxes(
        _layout_dict,
        blocks,
    )

    # compute horizontal text and intertext zones
    _layout_dict['horizontal_zones'] = compute_horizontal_text_intertext_zones(
        textblocks=_textblocks,
        layout_dict=_layout_dict,
    )

    # compute vertical zones within horizontal zones
    _layout_dict['vertical_zones'] = (
        compute_vertical_text_intertext_zones_within_text_zones(
            textblocks=_textblocks,
            layout_dict=_layout_dict,
        )
    )

    # compute horizontal rects out of horizontal zones
    _layout_dict['horizontal_rects'] = compute_horizontal_zones_rects(
        layout_dict=_layout_dict,
    )

    # compute vertical rects out of vertical zones
    _layout_dict['vertical_rects'] = compute_vertical_zones_rects(
        layout_dict=_layout_dict,
    )

    return _layout_dict


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
