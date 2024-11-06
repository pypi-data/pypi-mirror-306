# extract_images.py
'''
Module to extract image information from a page.
'''


import pymupdf  # type: ignore


def extract_image_info(page: pymupdf.Page) -> list[
    dict[
        str,
        str
        | int
        | float
        | tuple[float, float, float, float]
        | tuple[float, float, float, float, float, float],
    ]
]:
    '''
    Extract image information such as bbox, transform matrix, width,
    height, size, etc. for all the images in a given page, sort them
    from large to small, exclude information on smaller images
    contained in larger information and return the sorted and reduced
    list of images information.

    This list is then used to create the vector graphic list. It is also
    returned to the user when the param text_chunk of the to_markdown()
    function is set to True.

    :param page: pymupdf.Page: the current page.

    Returns: a list of image information, sorted from larger to smaller
    image and excluding the smaller images.
    '''
    # extract images on page
    _img_info: list[
        dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ]
    ] = page.get_image_info()[:]

    # sort by descending image area size
    _img_info.sort(
        key=lambda img_dict: abs(pymupdf.Rect(img_dict["bbox"])),
        reverse=True,
    )

    # ignore images contained in another one (simplified mechanism)
    #
    # run from back to front (= small to large)
    # to identify images contained in other images
    # and exclude the smallest ones
    for i in range(len(_img_info) - 1, 0, -1):

        # second image: after in the list -> smaller
        img1: dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ] = _img_info[i]

        # first image: before in the list -> larger
        img0: dict[
            str,
            str
            | int
            | float
            | tuple[float, float, float, float]
            | tuple[float, float, float, float, float, float],
        ] = _img_info[i - 1]

        # if the second image (smaller one) is contained in the first image
        # (larger one), exclude the smaller one
        if (
            pymupdf.Rect(img1["bbox"]) & page.rect
            in pymupdf.Rect(img0["bbox"]) & page.rect
        ):
            del _img_info[i]  # contained in some larger image

    return _img_info
