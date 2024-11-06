# extract_rects.py
'''
Module that wraps the extraction of rectangles of all types.

'''
from typing import Union

import pymupdf  # type: ignore

from pdf_structr.extract.extract_images import extract_image_info
from pdf_structr.extract.extract_tables import extract_tables
from pdf_structr.extract.extract_vgs import (
    make_lists_and_dict_of_vg_clusters_and_paths,
)

# from pdf_struct.custrag_layout.main import (
#     extract_page_text_layout,
# )
# from pymupdf4llm.helpers.multi_column import column_boxes  # type: ignore
from pdf_structr.multicol.main import (
    column_boxes,
)
from pdf_structr.stats.augment import clean_dicts_augment_spans
from pdf_structr.stats.prep_stats import (
    compute_stats_for_extraction,
)
from pdf_structr.utils.utils import (
    compute_container_bbox_from_list_dicts_bbox_key,
)

# from pdf_structr.custrag_stats.stats_page import (
#     compute_and_store_stats_in_dicts,
# )
# from pdf_struct.mo_utils.timer import count_and_avg_timer


def _define_clip_zone(
    page: pymupdf.Page, margins: tuple[float, float, float, float]
) -> pymupdf.Rect:
    '''
    Define the clip zone from which content shall be extracted.

    :param page: pymupdf.Page: the current page
    :param margins: page margins beyond which content shall not
        be considered.
    '''
    # Apply the margins to a clip rectangle
    left, top, right, bottom = margins

    return page.rect + (left, top, -right, -bottom)


# @count_and_avg_timer(name='prep - extract_elts_from_page')
def extract_elts_from_page(
    page: pymupdf.Page,
    margins: tuple[float, float, float, float],
    textflags: Union[int, int],
    table_strategy: str,
) -> tuple[
    pymupdf.TextPage,  # the textpage
    list[dict],  # the text_blocks as extracted by textpage.extractDICT
    list[pymupdf.IRect],  # the list of text rectangles
    tuple[
        # list of tables bbox, cols and rows
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],  # the numbered dict of tables md strings
        dict[int, pymupdf.Rect],  # a numbered dict of tab_rects
    ],
    list[  # the list of image information
        dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ]
    ],
    list,  # the graphics list (always empty due to bug)
    dict[int, pymupdf.Rect],  # vg_clusters: numbrd dict of vectr graphics
    list[dict[str, int | str | pymupdf.Rect]],  # the outer links list
    dict,  # the layout dict
]:
    '''
    Extracts a textpage, the links on the page, information
    on the images it contains, on the tables, on the vector
    graphics and the text rectangles.

    Returns this information in various formats in a tuple.

    :param page: pymupdf.Page: the current page.

    :param margins: tuple[float, float, float, float]: the margins tuple.

    :param textflags: Union[int, int]: the applicable text flags for the
        TextPages extraction. Union in this context is equivalent to
        adding the values of the respective textflags. Defaults to 192
        as per the main decorator (i.e. TEXT_MEDIABOX_CLIP (64) and
        TEXT_CID_FOR_UNKNOWN_UNICODE (128)).

    :param table_strategy: str: the table detection strategy. Valid values are
        "lines", "lines_strict" and "text". Default is "lines_strict" (ignores
        borderless rectangle vector graphics).
        "lines" uses all vector graphics on the page to detect grid lines.
        "text": text positions are used to generate "virtual" column and / or
        row boundaries
    '''
    ###################
    # Define the clip zone
    ###################

    _clip: pymupdf.Rect = _define_clip_zone(page=page, margins=margins)

    ###################
    # Extract external links on page
    ###################

    _links: list[dict[str, int | str | pymupdf.Rect]] = [
        link for link in page.get_links() if link["kind"] == pymupdf.LINK_URI
    ]

    ###################
    # Make a TextPage for all later extractions
    ###################

    _textpage: pymupdf.TextPage = page.get_textpage(
        flags=textflags, clip=_clip
    )

    ###################
    # Extract image information
    ###################

    _img_info: list[
        dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ]
    ] = extract_image_info(page=page)

    ###################
    # Extract blocks and augment spans
    ###################

    _blocks: list[dict] = _textpage.extractDICT(sort=True)["blocks"]

    # Compute some stats for further steps
    _blocks = clean_dicts_augment_spans(blocks=_blocks)
    compute_stats_for_extraction(_blocks)

    # _blocks, _page_stats = compute_and_store_stats_in_dicts(
    #     page=page,
    #     blocks=_blocks,
    # )

    textpage_bbox: pymupdf.Rect = pymupdf.Rect(
        compute_container_bbox_from_list_dicts_bbox_key(_blocks)
    )

    # extract layout
    _layout_dict: dict = {}
    # _layout_dict: dict[str, dict | list] = extract_page_text_layout(
    #     page=page,
    #     blocks=_blocks,
    #     page_stats=_page_stats,
    # )

    ###################
    # Extract drawings
    ###################

    # NOTE: consider moving this after the filters
    def _pop_useless_keys(drawing):
        del drawing['layer']
        del drawing['even_odd']
        del drawing['fill_opacity']

        del drawing['stroke_opacity']
        del drawing['dashes']
        del drawing['lineJoin']
        del drawing['lineCap']

        # NOTE: consider rounding the bboxes, but
        # needs to access Rect keys and this might be cruelly slow

        return drawing

    _drawings: list[dict] = [
        _pop_useless_keys(drawing) for drawing in page.get_drawings()
    ]

    # Attempt to work with the cdrawings instead
    # Non-conclusive due to some missing keyword args
    # _drawings2: list[dict] = page.get_cdrawings()

    ###################
    # Extract tables information
    ###################

    # _tables_tuple:
    # - _tables (coord): for information purposes
    # - _tab_md_strs: for output
    # - _tab_rects (dict[Rect]): to position the tables on the page
    # - _tab_rects0 (list[Rect]): as exclusion zone
    _tables_tuple: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
        list[pymupdf.Rect],
    ] = extract_tables(
        page=page,
        textpage=_textpage,
        drawings=_drawings,
        blocks=_blocks,
        clip=_clip,
        textpage_bbox=textpage_bbox,
        table_strategy=table_strategy,
    )

    ###################
    # Extract vector graphics information
    ###################

    # BUG: This is never accessed, except return, so always returning
    # an empty list
    _graphics: list = []

    # Make a list and a numbered dict of vg_clusters Rectangles
    # # and a list of actual (relevant) paths
    _vg_clusters0, _vg_clusters, _actual_paths = (
        make_lists_and_dict_of_vg_clusters_and_paths(
            page=page,
            drawings=_drawings,
            tab_rects0=_tables_tuple[3],  # this is the tables rect list
            img_info=_img_info,
        )
    )

    ###################
    # Extract text boxes
    ###################

    # identify text bboxes on page, avoiding tables, images and graphics
    # also extract the text blocks from the page with textpage.extractDICT
    _text_rects: list[pymupdf.Rect | pymupdf.IRect] = column_boxes(
        page=page,
        blocks=_blocks,
        no_image_text=True,
        paths=_actual_paths,  # this is the paths themselves
        # this is a combined list of tables rect and img/vg rectangles
        avoid=_tables_tuple[3] + _vg_clusters0,
    )

    return (
        _textpage,
        _blocks,
        _text_rects,
        # we return only the list of table bbox, cols and rows,
        # the dict of tables md_strs and the dict of table rects
        (
            _tables_tuple[0],
            _tables_tuple[1],
            _tables_tuple[2],
        ),
        _img_info,
        _graphics,
        _vg_clusters,
        _links,
        _layout_dict,
    )
