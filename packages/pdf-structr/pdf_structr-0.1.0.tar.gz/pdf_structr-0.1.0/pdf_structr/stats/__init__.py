# __init__.py
'''
Package encapsulating the statistical functions of custrag.

Entry point:

`pdf_struct.custrag_stats`

-> stats_page, compute_and_store_stats_in_dicts()
    -> _compute_stats_in_blocks_and_lower_level_dicts():

-> stats_block, augment_block_and_subdicts()
    -> _collect_lines_txtlen_ftsize_and_compute_block_ftsize_stats()
        -> _compute_block_lines_stats()
        -> _compute_spans_and_chars_stats_for_block()
            -> _compute_spans_stats_for_block()
            -> _compute_chars_stats_for_block()

-> stats_line,
'''
