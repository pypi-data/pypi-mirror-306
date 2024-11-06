# extract_blocks_compnd_bb.py
'''
Extracts the page compound blocks bboxes.
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
# Page compound blocks bounding boxes
#####################


def _compute_page_blocks_compound_bb_core(
    blocks: list[dict],
) -> dict[str, float]:
    '''
    Compute the compound blocks bounding box, i.e. the smallest rectangle
    containing all the blocks in the passed-in blocks list.

    :returns: dict[str, float]: a dict with the coordinates of the
        corresponding bbox.

    :param blocks: list[dict]: the list of blocks for which to compute
        the compound bbox.
    '''
    return {
        'x0': (min(blocks, key=lambda _block: _block['bbox'][0]))['bbox'][0],
        'y0': (min(blocks, key=lambda _block: _block['bbox'][1]))['bbox'][1],
        'x1': (max(blocks, key=lambda _block: _block['bbox'][2]))['bbox'][2],
        'y1': (max(blocks, key=lambda _block: _block['bbox'][3]))['bbox'][3],
    }


def compute_page_blocks_compound_bbxes(
    stats_dict: dict,
    blocks: list[dict],
) -> list[dict]:
    '''
    Computes the page compound blocks bounding box, the page compound
    textblocks bounding box and the page compound image block bounding
    box.

    :returns: the text blocks (no image block).

    :param stats_dict: dict: the dict where we store the computed statistics.
    :param blocks: list[dict]: the page blocks.
    '''
    # all (txt and image) blocks bounding box
    # ---------------------------------------
    stats_dict['page']['blocks_bbox'] = _compute_page_blocks_compound_bb_core(
        blocks=blocks
    )

    # text blocks bounding box
    # ---------------------------------------
    # Filter the blocks to get the text blocks only
    _textblocks = [_block for _block in blocks if _block['type'] == 0]

    # Compute the page's compound bbox for the textblocks
    if _textblocks:
        stats_dict['page']['text_blocks_bbox'] = (
            _compute_page_blocks_compound_bb_core(
                blocks=_textblocks,
            )
        )
    else:
        stats_dict['page']['text_blocks_bbox'] = None

    # image blocks bounding box
    # ---------------------------------------
    # Filter the blocks to get the image blocks only
    _imgblocks = [_block for _block in blocks if _block['type'] == 1]

    # Compute the page's compound bbox for the image blocks
    if _imgblocks:
        stats_dict['page']['img_blocks_bbox'] = (
            _compute_page_blocks_compound_bb_core(
                blocks=_imgblocks,
            )
        )
    else:
        stats_dict['page']['img_blocks_bbox'] = None

    return _textblocks


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
