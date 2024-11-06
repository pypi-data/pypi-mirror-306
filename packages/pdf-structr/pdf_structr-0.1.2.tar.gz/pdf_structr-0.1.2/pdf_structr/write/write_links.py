# write_links.py
'''
Storing links related functions
'''

import pymupdf  # type: ignore


def resolve_links(
    links: list[dict[str, int | str | pymupdf.Rect]] | None,
    span: dict[str, float | int | str | tuple[float, float] | pymupdf.Rect],
) -> str | None:
    '''
    Accept a span and return a markdown link string if the spans and one of the
    links overlap by more than 70%.

    :param links: list[pymupdf.Link]: a list of links
        as returned by page.get_links().

    :param span: dict[
        str, float | int | str | tuple[float, float] | pymupdf.Rect
    ]: a span dictionary as returned by page.get_text("dict")

    Returns:
        None or a string representing the link in MD format.
    '''
    if links is None:
        return None

    _span_bbox: pymupdf.Rect = span["bbox"]
    # top_y_thresholds: float = _span_bbox.y0 - _span_bbox.height
    # bottom_y_thresholds: float = _span_bbox.y1 + _span_bbox.height

    _pot_links_list: list[str] = [
        f'[{str(span["text"]).strip()}]({_pot_link["uri"]})'
        for _pot_link in links
        if (
            # pot_link['from'].y0 <= top_y_thresholds  # type: ignore
            # and pot_link['from'].y1 >= bottom_y_thresholds  # type: ignore
            # If the link overlaps at least 70% of the span
            (_pot_link["from"].tl + _pot_link["from"].br) / 2  # type: ignore
            in _span_bbox
        )
    ]

    if _pot_links_list:
        return _pot_links_list[0]

    return None
