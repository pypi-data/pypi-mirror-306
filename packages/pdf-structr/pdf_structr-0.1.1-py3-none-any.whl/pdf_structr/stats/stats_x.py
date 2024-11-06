# stats_x.py
'''
Compute stats on x coordinates of elements in page.
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
# Playground
#####################


def _append_to_dict(
    x0_dict: dict[float, int], txtdict: dict[str, tuple]
) -> None:
    '''
    Appends or increments a key counting the x0 coordinate of the txtdict
    in the x0_dict.

    :param x0_dict: dict[float, int]:
    :param txtdict: dict[str, tuple]:
    '''
    _x0_coord: float = round(txtdict['bbox'][0], 2)
    x0_dict[_x0_coord] = x0_dict.get(_x0_coord, 0) + 1


def _compute_x0_stats(textblocks: list[dict], page_stats: dict) -> None:
    '''
    Compute page level spans x0 stats and stores the results in the
    page_stats dict.

    :param textblocks: list[dict]: the list of non-white and non-empty
        text block dicts.
    :param page_stats: dict: a dict to collect statistics on the page.
    '''
    # Sum up blocks which share the same x0 into a x0_dict
    _blocks_x0_dict: dict[float, int] = {}
    _lines_x0_dict: dict[float, int] = {}
    _spans_x0_dict: dict[float, int] = {}

    for _txtblock in textblocks:
        _append_to_dict(
            x0_dict=_blocks_x0_dict,
            txtdict=_txtblock,
        )
        for _line in _txtblock['lines']:
            _append_to_dict(
                x0_dict=_lines_x0_dict,
                txtdict=_line,
            )
            for _span in _line['spans']:
                _append_to_dict(
                    x0_dict=_spans_x0_dict,
                    txtdict=_span,
                )

    page_stats['blocks_x0s_dict'] = dict(sorted(_blocks_x0_dict.items()))
    page_stats['lines_x0s_dict'] = dict(sorted(_lines_x0_dict.items()))
    page_stats['spans_x0s_dict'] = dict(sorted(_spans_x0_dict.items()))


def compute_page_level_coord_stats(
    page_stats: dict, textblocks: list[dict]
) -> None:
    '''
    Compute page level elements' coordinates stats.

    :param page_stats: dict: a dict to collect statistics on the page.
    :param textblocks: list[dict]: the list of non-white and non-empty
        text block dicts.
    '''
    _compute_x0_stats(textblocks=textblocks, page_stats=page_stats)


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
