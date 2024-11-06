# clustc_ho_trows.py
'''
Module encapsulating a high-order stack used by
the rlb and the clb stacks to group blocks
or rows of blocks by clusters of table rows.

ho: high-order
trows: table rows

'''


import logging
from typing import Any, Callable

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
# Create clusters of blocks or rows forming a table
#####################


def _create_cluster_acmb(
    clusters: list[list],
    curr_item: Any,
    next_item: Any,
    same_cluster: bool,
    are_items_likely_rows_in_same_table_fn: Callable,
):
    '''
    Create a new rows or blocks cluster if needed. Returns True if has
    and False if it did not.

    :param clusters: list[list]: the list of items' clusters currently
        being built (rows or blocks).

    :param curr_item: Any: the current item to be appended as a cluster
        or passed.

    :param next_item: Any: the current item for comparison purposes with
        curr_item.

    :param same_cluster: bool: a boolean, that will be reset in the current
        function for the next item in the list and indicating whether
        the current item shall be added to the current cluster.

    :param are_items_likely_rows_in_same_table_fn: Callable: the function that
        will test whether two consecutive items shall form part of the same
        cluster or not.
    '''
    # test whether the next item belongs to the same cluster as this item
    if are_items_likely_rows_in_same_table_fn(
        curr_item,
        next_item,
    ):
        # if so, and if the same_cluster sentinel is False, the current
        # item has not yet been added to any cluster
        # => we need to create a new cluster and add this item to the
        # new cluster
        if same_cluster is False:
            clusters.append([curr_item])

        # Turn same_cluster to True so that the next item
        # be automatically appended to the same cluster
        return True

    # Turn _same_cluster to False; next item will have
    # to be compared against its follower to eventually
    # make a new cluster
    return False


def _add_item_as_cluster_or_to_clusters_or_pass(
    clusters: list[list],
    items: list,
    idx: int,
    same_cluster: bool,
    are_items_likely_rows_in_same_table_fn: Callable,
):
    '''
    Appends an item to the last cluster in the list of clusters, create a new
    cluster starting with the current item or pass.

    :param clusters: list[list]: the list of items' clusters currently
        being built.

    :param items: list: a list of items from which two consecutive items
        will be extracted and tested against each other to determine
        whether they are likely rows of the same table and appended as
        such to a cluster or as a new cluster or passed if not matching
        the criteria.

    :param idx: int: the index number in the iteration on the blocks list.

    :param same_cluster: bool: a boolean, that will be reset in the current
        function for the next block in the list and indicating whether
        the current block shall be added to the current cluster (i.e. has
        the same spans' count and is consecutive to the previous cluster).

    :param are_items_likely_rows_in_same_table_fn: Callable: the function that
        will test whether two consecutive items shall form part of the same
        cluster or not.
    '''

    # if it has been determined that the current item belongs to the
    # same cluster as the previous item, append it to the last cluster
    if same_cluster is True:
        clusters[-1].append(items[idx])

    # Test whether the next item belongs to the same cluster
    # as this one. If so and if same_cluster is False, create a new items
    # cluster.
    # Reset the value of same_cluster to True if a new cluster
    # has been creaed => at next iteration, the next item will
    # be automatically appending to the last cluster.
    same_cluster = _create_cluster_acmb(
        clusters=clusters,
        curr_item=items[idx],
        next_item=items[idx + 1],
        same_cluster=same_cluster,
        are_items_likely_rows_in_same_table_fn=(
            are_items_likely_rows_in_same_table_fn
        ),
    )

    # return the sentinel
    return same_cluster


def group_items_by_clusters_of_consecutive_items_with_same_coll_count(
    items: list[Any],
    are_items_likely_rows_in_same_table_fn: Callable,
) -> list[list[Any]]:
    '''
    Group a list of items into clusters of consecutive items with the
    same cols count. Items may be text blocks (in which case
    `are_items_likely_rows_in_same_table_fn` will rely on an analysis
    of its lines and/or spans to figure out whether they are likely
    rows in a table) or rows of text blocks (in which case
    `are_items_likely_rows_in_same_table_fn` will rely on an analysis
    of the contained blocks to figure out whether they are likely
    rows in a table).

    May be passed as items either rows or blocks.

    :param items: list: a list of items from which two consecutive items
        will be extracted and tested against each other to determine
        whether they are likely rows of the same table and appended as
        such to a cluster or as a new cluster or passed if not matching
        the criteria.

    :param are_items_likely_rows_in_same_table_fn: Callable: the function that
        will test whether two consecutive items shall form part of the same
        cluster or not.

    '''

    # declare a clusters list of list where each sublist will be a cluster
    _clusters: list[list] = []
    # declare a sentinel to be set to True or False within the loop to indicate
    # whether the next item shall be appended to the same cluster as the
    # current item within the iteration
    _same_cluster: bool = False

    # walk the items and group them by clusters
    for _idx in range(0, len(items) - 1):

        _same_cluster = _add_item_as_cluster_or_to_clusters_or_pass(
            clusters=_clusters,
            items=items,
            idx=_idx,
            same_cluster=_same_cluster,
            are_items_likely_rows_in_same_table_fn=(
                are_items_likely_rows_in_same_table_fn
            ),
        )

    # hande the last item in the list
    # at this point, if the _same_cluster sentinel has been turned to True,
    # this means that the last block in the list of filtered_blocks
    # has been selected to be added to the last block_cluster
    if _same_cluster is True:
        # so just do it
        _clusters[-1] += [items[-1]]  # type: ignore

    return _clusters


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
