# tables_tup_combine.py
'''
Module providing functions to combine tables_tuples when we have
two table_tuples returned by both the TableFinder and stabs.
'''


import pymupdf  # type: ignore

from pdf_structr.tables.table_lib import (
    create_table_info_dict,
)
from pdf_structr.utils.utils import sort_rect_key_by_bottom_y_left_x

#####################
# Combine the tables from NewTableFinder and from clusters
#####################


def _eliminate_smallest_rect(
    rect_one: pymupdf.Rect,
    rect_two: pymupdf.Rect,
    idx_one: int,
    idx_two: int,
    rect_dicts_one: dict[int, pymupdf.Rect],
    rect_dicts_two: dict[int, pymupdf.Rect],
    mdstr_dict_one: dict[int, str | None],
    mdstr_dict_two: dict[int, str | None],
) -> None:
    '''
    Compare rect_one and rect_two areas and eliminate the smallest rectangle
    from its numbered dict.
    '''
    _rect_one_area = rect_one.get_area()
    _rect_two_area = rect_two.get_area()

    if _rect_one_area > _rect_two_area:
        rect_dicts_two[idx_two] = None
        mdstr_dict_two[idx_two] = None
        return

    if _rect_two_area > _rect_one_area:
        rect_dicts_one[idx_one] = None
        mdstr_dict_one[idx_one] = None


def _eliminate_contained_or_smaller_intersects_rect(
    rect_one: pymupdf.Rect,
    rect_two: pymupdf.Rect,
    idx_one: int,
    idx_two: int,
    rect_dict_one: dict[int, pymupdf.Rect | None],
    rect_dict_two: dict[int, pymupdf.Rect | None],
    mdstr_dict_one: dict[int, str | None],
    mdstr_dict_two: dict[int, str | None],
) -> None:
    '''
    Eliminate rectangles contained in other and smaller intersecting
    rectangles.
    '''
    # containment check
    if rect_two.contains(rect_one):
        rect_dict_one[idx_one] = None
        mdstr_dict_one[idx_one] = None
        return

    if rect_one.contains(rect_two):
        rect_dict_two[idx_two] = None
        mdstr_dict_two[idx_two] = None
        return

    # intersection check: the larger wins
    if rect_two.intersects(rect_one):

        _eliminate_smallest_rect(
            rect_one=rect_one,
            rect_two=rect_two,
            idx_one=idx_one,
            idx_two=idx_two,
            rect_dicts_one=rect_dict_one,
            rect_dicts_two=rect_dict_two,
            mdstr_dict_one=mdstr_dict_one,
            mdstr_dict_two=mdstr_dict_two,
        )


def _compare_with_second_rect_list(
    rect_one: pymupdf.Rect,
    idx_one: int,
    rect_dict_one: dict[int, pymupdf.Rect | None],
    rect_dict_two: dict[int, pymupdf.Rect | None],
    mdstr_dict_one: dict[int, str | None],
    mdstr_dict_two: dict[int, str | None],
    idx_rect_tup_list_two: list[tuple[int, pymupdf.Rect]],
):
    # check against second list
    for _idx_two, _rect_two in idx_rect_tup_list_two:

        # continue if dict has already been disqualified
        if rect_dict_two.get(_idx_two) is None:
            continue

        _eliminate_contained_or_smaller_intersects_rect(
            rect_one=rect_one,
            rect_two=_rect_two,
            idx_one=idx_one,
            idx_two=_idx_two,
            rect_dict_one=rect_dict_one,
            rect_dict_two=rect_dict_two,
            mdstr_dict_one=mdstr_dict_one,
            mdstr_dict_two=mdstr_dict_two,
        )


def _build_combined_dict(
    rect_dict: dict[int, pymupdf.Rect],
    md_str_dict: dict[int, str],
    common_rect_dict: dict[int, pymupdf.Rect],
    common_mdstr_dict: dict[int, str],
    common_idx: int,
):
    for _idx, _rect in rect_dict.items():
        if _rect is not None:
            common_rect_dict[common_idx] = _rect
            common_mdstr_dict[common_idx] = md_str_dict[_idx]
            common_idx += 1

    return common_idx


def _make_info_dict(
    _rect: pymupdf.Rect,
    _mdstr: str,
) -> dict[str, tuple[float, float, float, float] | int]:
    ''' '''
    _lr_count: int = _mdstr.count('|\n')
    _row_count: int = _lr_count - 2
    _col_count: int = int((_mdstr.count('|')) / (_lr_count) - 1)

    return create_table_info_dict(
        table_rect=_rect,
        row_count=_row_count,
        col_count=_col_count,
    )


def _filter_out_empty_tables_tuples(
    tables_tuples: list[
        tuple[
            list[dict[str, tuple[float, float, float, float] | int]],
            dict[int, str],
            dict[int, pymupdf.Rect],
            list[pymupdf.Rect],
        ]
    ],
) -> list[tuple]:
    return [
        _tables_tup
        for _tables_tup in tables_tuples
        # to eliminate empty tuple, we just check the list[dict] stored
        # as element[0] in each _tables_tuple
        if _tables_tup[0]
    ]


#####################
# Old interface
# NOTE: Dead code
# Used to be called by `combine_tables_tuples`
#####################


def _compare_and_eliminate_rects_from_dicts(
    rect_dict_one: dict[int, pymupdf.Rect],
    rect_dict_two: dict[int, pymupdf.Rect],
    mdstr_dict_one: dict[int, str],
    mdstr_dict_two: dict[int, str],
) -> None:
    '''
    Eliminate rectangles contained in other and smaller intersecting
    rectangles from each others dictionaries of Rect.
    '''
    _idx_rect_tup_list_one: list[tuple[int, pymupdf.Rect]] = list(
        rect_dict_one.items()
    )
    _idx_rect_tup_list_two: list[tuple[int, pymupdf.Rect]] = list(
        rect_dict_two.items()
    )

    for _idx_one, _rect_one in _idx_rect_tup_list_one:
        # continue if dict has already been disqualified
        if rect_dict_one.get(_idx_one) is None:
            continue

        _compare_with_second_rect_list(
            rect_one=_rect_one,
            idx_one=_idx_one,
            rect_dict_one=rect_dict_one,
            rect_dict_two=rect_dict_two,
            mdstr_dict_one=mdstr_dict_one,  # type: ignore
            mdstr_dict_two=mdstr_dict_two,  # type: ignore
            idx_rect_tup_list_two=_idx_rect_tup_list_two,
        )


def _build_combined_dicts(
    rect_dict_one,
    mdstr_dict_one,
    rect_dict_two,
    mdstr_dict_two,
) -> tuple[
    dict[int, pymupdf.Rect],
    dict[int, str],
]:
    '''
    Build combined Rectangle and MD string dictionaries.
    '''
    _common_rect_dict: dict[int, pymupdf.Rect] = {}
    _common_mdstr_dict: dict[int, str] = {}

    _common_idx: int = 0

    _common_idx = _build_combined_dict(
        rect_dict=rect_dict_one,
        md_str_dict=mdstr_dict_one,
        common_rect_dict=_common_rect_dict,
        common_mdstr_dict=_common_mdstr_dict,
        common_idx=_common_idx,
    )

    _build_combined_dict(
        rect_dict=rect_dict_two,
        md_str_dict=mdstr_dict_two,
        common_rect_dict=_common_rect_dict,
        common_mdstr_dict=_common_mdstr_dict,
        common_idx=_common_idx,
    )

    return _common_rect_dict, _common_mdstr_dict


def _make_info_list(
    _common_rect_dict: dict[int, pymupdf.Rect],
    _common_mdstr_dict: dict[int, str],
) -> list[dict[str, tuple[float, float, float, float] | int]]:
    '''
    Make the information dict.
    '''
    return [
        _make_info_dict(_rect, _mdstr)
        for _rect, _mdstr in zip(
            _common_rect_dict.values(),
            _common_mdstr_dict.values(),
        )
    ]


def _combine_tables_from_stabs(
    tables_tuples: list[tuple[list, dict, dict, list]],
):
    '''
    Combine tables coming from the NewTableFinder with those extracted
    via the block clusters extractor.

    :param tables_tuples: list[tuple]: tables groups extracted by the
        stabs table extractor.
    '''
    pass


#####################
# Main interface
#####################


def combine_tables_tuples(
    tables_tuple_from_NewTableFinder: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
        list[pymupdf.Rect],
    ],
    tables_tuples_from_stabs: list[
        tuple[
            list[dict[str, tuple[float, float, float, float] | int]],
            dict[int, str],
            dict[int, pymupdf.Rect],
            list[pymupdf.Rect],
        ]
    ],
):
    '''
    Combine tables coming from the NewTableFinder with those extracted
    via the block clusters extractor.

    :param tables_tuple_from_NewTableFinder: tuple[
        list[dict[str, tuple[float, float, float, float] | int]],
        dict[int, str],
        dict[int, pymupdf.Rect],
        list[pymupdf.Rect],
    ]: the tables extracted by the NewTableFinder.

    :param tables_tuples_from_stabs: list[
        tuple[
            list[dict[str, tuple[float, float, float, float] | int]],
            dict[int, str],
            dict[int, pymupdf.Rect],
            list[pymupdf.Rect],
        ]
    ]: the tables extracted by stabs.
    '''
    # if not tables_tuple_from_NewTableFinder[0]:
    #     _combine_tables_from_stabs(tables_tuples_from_stabs)

    # 0. Filter out table_tuples containing no tables
    _filtered_stabs_tuple_list: list[
        tuple[
            list[dict[str, tuple[float, float, float, float] | int]],
            dict[int, str],
            dict[int, pymupdf.Rect],
            list[pymupdf.Rect],
        ]
    ] = _filter_out_empty_tables_tuples(tables_tuples_from_stabs)

    # There is no table returned by the NewTableFinder
    if not tables_tuple_from_NewTableFinder[0]:
        # 1. If there is no table at all, return a table of empty containers
        if not _filtered_stabs_tuple_list:
            return ([], {}, {}, [])

        # 2. If there is only one tables_tuples in the tables_tuples returned
        # by stabs, return it
        if len(_filtered_stabs_tuple_list) == 1:
            return _filtered_stabs_tuple_list[0]

    # At this stage, there is a tables_tuple returned by the NewTableFinder
    #
    # ... and if no tables_tuples have been returned by stabs, return
    # the tables_tuple returned by NewTableFinder
    if not _filtered_stabs_tuple_list:
        return tables_tuple_from_NewTableFinder

    # Now, there are:
    # - a tables_tuple returned by the NewTableFinder and
    # - one or more tables_tuple returned by stabs.

    # NOTE: We need to combine, but we do no longer have to make containement
    # and intersections checks since (i) each tables_tuple covers a given area
    # and, (ii) inside a given tables_tuples, by conception, tables never
    # overlap.

    # append the tables_tup returned by the NewTableFinder to the list of
    # tables_tup
    _filtered_stabs_tuple_list.append(tables_tuple_from_NewTableFinder)

    # declare two returns dict for Rect and md strings
    _common_rect_dict: dict[tuple[int, int], pymupdf.Rect] = {}
    _common_mdstr_dict: dict[tuple[int, int], str] = {}

    # Walk the tables_tuples and rebuild the tables dicts
    for _idx, _tables_tup in enumerate(_filtered_stabs_tuple_list):
        _rect_dict: dict[int, pymupdf.Rect] = _tables_tup[2]
        _mdstr_dict: dict[int, pymupdf.Rect] = _tables_tup[1]

        for _rect_idx, _rect in _rect_dict.items():
            _common_rect_dict[(_idx, _rect_idx)] = _rect
            _common_mdstr_dict[(_idx, _rect_idx)] = _mdstr_dict[_rect_idx]

    # # a. Eliminate any table that is fully inside another one or that
    # # intersects another and is smaller
    # _rect_dict_one: dict[int, pymupdf.Rect] = tables_tuples[0][2]
    # _rect_dict_two: dict[int, pymupdf.Rect] = tables_tuples[1][2]

    # _mdstr_dict_one: dict[int, str] = tables_tuples[0][1]
    # _mdstr_dict_two: dict[int, str] = tables_tuples[1][1]

    # _compare_and_eliminate_rects_from_dicts(
    #     rect_dict_one=_rect_dict_one,
    #     rect_dict_two=_rect_dict_two,
    #     mdstr_dict_one=_mdstr_dict_one,
    #     mdstr_dict_two=_mdstr_dict_two,
    # )

    # # b. Build the common dicts and lists
    # _common_rect_dict, _common_mdstr_dict = _build_combined_dicts(
    #     rect_dict_one=_rect_dict_one,
    #     mdstr_dict_one=_mdstr_dict_one,
    #     rect_dict_two=_rect_dict_two,
    #     mdstr_dict_two=_mdstr_dict_two,
    # )

    # c. Sort the rect dict

    sorted_rect_list: list[pymupdf.Rect] = list(_common_rect_dict.values())
    sorted_rect_list.sort(key=sort_rect_key_by_bottom_y_left_x)

    # d. make the info list
    # _table_info_list: list[
    #     dict[str, tuple[float, float, float, float] | int]
    # ] = _make_info_list(
    #     _common_rect_dict,
    #     _common_mdstr_dict,
    # )

    return (
        [],
        _common_mdstr_dict,
        _common_rect_dict,
        sorted_rect_list,
    )
