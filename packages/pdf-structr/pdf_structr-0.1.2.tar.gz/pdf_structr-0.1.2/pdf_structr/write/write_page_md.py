# write_page_md.py
'''
Stores the high-level functions that write the markdown for a page.

'''

import logging
from typing import Iterable

from pdf_structr.write.classes import Line, Parag, ParagImgTab

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
# Turn ParagImgTab and Line elements into a markdown string
#####################


def _extract_str_elts(str_container: ParagImgTab | Line) -> Iterable[str]:
    '''
    Extract string elements from a ParagImgTab | Line.

    :param str_container: ParagImgTab | Line: a ParagImgTab or one of the
        Lines contained in its Parag elements.
    '''
    return (
        *str_container.prefix,
        *str_container.indent_prefix,
        *str_container.str_itr,  # type: ignore
        *str_container.suffix,
        (str_container.lr_suffix * '\n'),
    )


def _extract_str_elts_from_parag(parag: Parag) -> Iterable[str]:
    '''
    Extract string elements from a Parag.

    :param parag: Parag: a Parag element from wich we want to extract
        the line's strings elements (prefix, suffix, str_irt, etc.).
    '''
    return [
        _line_it
        for _line in parag.lines
        for _line_it in _extract_str_elts(str_container=_line)
    ]


def _extract_str_elts_wrapper(parag_img_tab: ParagImgTab) -> Iterable[str]:
    '''
    Extract the string elements from the ParagImgTab element or its
    sub-elements (Parags -> Lines).

    :param parag_img_tab: ParagImgTab: the current ParagImgTab, storing
        either (i) a group of Parag, (ii) the string representation or
        references to an image or (iii) the md-string representation of
        a table.
    '''
    _elt_type: str = parag_img_tab.elt_type

    # If it is a table or image vg element
    if _elt_type == 'table' or _elt_type == 'image_vg':

        return _extract_str_elts(str_container=parag_img_tab)

    # Else it is a text element: the text is nested inside
    # the lines
    return [
        _it
        # Extract each paragraph
        for _parag in parag_img_tab.parags
        # Extract each parag's prefix, suffix, etc. and respectively
        # for each of its lines
        for _it in _extract_str_elts_from_parag(parag=_parag)
        # at the end of the extraction of each parag_img_tab, we add
        # a line return to close the ParagImgTab
    ] + [parag_img_tab.lr_suffix * '\n']


def _clean_page_string(page_md_string: str) -> str:
    '''
    Make some string cleaning before returning.
    '''
    return (
        page_md_string.replace(" ,", ",")
        .replace("\n\n\n", "\n\n")
        .replace("  ", " ")
        .replace(" \n", "\n")
        # superscript square brackets handling
        .replace("] .", "].")
        .replace("] ,", "],")
        .replace("] )", "])")
        .replace("( [", "([")
        # strip any leading `\n`
        .lstrip('\n')
        # only usefull without pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE
        .replace(chr(0), chr(0xFFFD))
    )

    # while md_string.startswith("\n"):
    #     md_string = md_string[1:]


def make_md_string(parag_img_tabs: list[ParagImgTab]) -> str:
    '''
    Turn the parag_img_tabs list into a markdown string.

    :param parag_img_tabs: list[ParagImgTab]: the list of ParagImgTab
        collected for the current page.
    '''
    # Page separator
    _page_sep_str: str = "----\n\n"

    # Flatten the prefix, str_itr and suffix elts of the dicts
    # listed in parag_img_tabs into a single list
    # and join them into a string
    _page_md_string: str = (
        ''.join(
            _subit
            for _parag_img_tab in parag_img_tabs
            for _it in _extract_str_elts_wrapper(_parag_img_tab)
            for _subit in _it
        )
        + _page_sep_str
    )

    # cleaning
    return _clean_page_string(_page_md_string)


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
