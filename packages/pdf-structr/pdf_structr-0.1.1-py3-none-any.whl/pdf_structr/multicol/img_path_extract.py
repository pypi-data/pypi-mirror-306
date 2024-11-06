# img_path_extract.py
'''
Stores functions that extracts the bbox rectangles of the paths and images
in the a given page.
'''


import logging

from pymupdf import Page, Rect  # type: ignore

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


def _make_path_rect(p: dict) -> Rect:
    '''
    Makes a Rect for a given path.

    :param p: dict: a pymupdf Path.
    '''
    # Get the path's rectangle
    prect: Rect = p["rect"]

    # give empty path rectangles some small width or height
    lwidth = 0.5 if (_ := p["width"]) is None else _ * 0.5
    if prect.width == 0:
        prect.x0 -= lwidth
        prect.x1 += lwidth
    if prect.height == 0:
        prect.y0 -= lwidth
        prect.y1 += lwidth

    return prect


def get_path_bboxes_list(
    paths: list[dict],
) -> list[Rect]:
    '''
    Create a bbox Rectangle list of the paths on the current page.

    :param page: Page: the current page.
    :param paths: list[dict]: a list of paths previously extracted.
    '''
    # extract vector graphics rectangles
    _path_rects: list[Rect] = [_make_path_rect(p) for p in paths]

    # sort path bboxes by ascending top, then left coordinates
    _path_rects.sort(key=lambda b: (b.y0, b.x0))

    return _path_rects


# def get_img_bboxes_list(
def make_avoid_bboxes_list(
    page: Page,
    avoid: list[Rect] | None,
    no_image_text: bool,
) -> list[Rect]:
    '''
    Returns a list of bboxes to avoid, comprising the identified
    table Rectangles, the vg clusters as well as the image blocks.

    Populates the passed-in img_bboxes with the passed-in `avoid`
    `Rectangle` `list` and the images extracted from this page by
    `page.get_image_rects()`.

    :returns: list[Rect]: the list of images' bbox Rectangles of the
        current page populated by this function.

    :param page: Page: the page being currently parsed for columns.

    :param avoid: list[Rect]: this is a list of Rect-likes, which have
        been extracted previously and covering vector graphic clusters
        and tables.

    :param no_image_text: bool: a boolean indicating whether we want to ignore
        text inside image bboxes. True = ignore. False = do not ignore.
    '''
    # Declare a list of bboxes of zones to be avoided if no_image_text is True
    _avoid_bboxes: list[Rect] = []
    # # Declare a list of image bboxes
    # _img_bboxes: list[Rect] = []

    # If the user has provided a list of already extracted
    # image Rectangles in the `avoid` parameter of the main function,
    # add the corresponding Rectangles to _img_bboxes
    if avoid is not None and no_image_text is True:
        _avoid_bboxes = avoid
    # if avoid is not None:
    #     _img_bboxes.extend(avoid)

    # If the user has requested to ignore the text contained in images'
    if no_image_text is True:

        # # Extract the image bbox Rectangles from the page
        # # and append them to the list of _img_bboxes
        # _img_bboxes.extend(
        # Extract the image bbox Rectangles from the page
        # and append them to the list of _avoid_bboxes
        _avoid_bboxes.extend(
            # get the corresponding image rectangles
            page.get_image_rects(_image_xref[0])
            # get the page's image xrefs
            for _image_xref in page.get_images()
        )

    # return _img_bboxes
    return _avoid_bboxes


#####################
# Main and ifnamemain block
#####################


def main():
    pass


if __name__ == '__main__':
    main()
