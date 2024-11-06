# main_utils.py
'''
Storing the main decorator for the customized pymupdf to markdown
converter.
'''
import functools
import logging
import os
from typing import Any, Callable, Union

import pymupdf  # type: ignore

# from pdf_struct.mo_pymupdf_pp.hdr_clssr import (
#     IdentifyHeaders,
# )
from pdf_structr.header_id.identify_hdr import IdentifyHeaders

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

############################
# Helpers
############################


def _make_doc_layout_for_reflowable_docs(
    doc: pymupdf.Document,
    page_width: float,
    page_height: float,
) -> None:
    '''
    Change doc layout for reflowable documents such HTML and ebooks.
    Sets the layout of reflowable document to:
    - multiple pages of `page_height` if a page_height param has been
    passed in;
    - a single page for documents that are reflowable and do not have a
    page height attribute.

    :returns: None. The function is just setting the properties of the
        passed-in doc which is mutable.

    :param doc: pymupdf.Document: the pymupdf document currently being
        processed.
    :param page_width: float: the page width parameter passed-in by the user.
    :param page_height: float: the page height parameter passed-in by the user.
    '''
    # reflowable documents allow making 1 page for the whole document
    if doc.is_reflowable:
        # check if a user defined page dimension was provided
        if hasattr(page_height, "__float__"):
            # accept user page dimensions
            doc.layout(width=page_width, height=page_height)
        else:
            # no page height limit given: make 1 page for whole document
            doc.layout(width=page_width, height=792)
            # height that covers full document
            height = 792 * doc.page_count
            doc.layout(width=page_width, height=height)


def _validate_margins(
    margins: (
        float
        | tuple[float]
        | tuple[float, float]
        | tuple[float, float, float, float]
    )
) -> tuple[float, float, float, float]:
    '''
    Converts the margins from the user input to a 4-float tuple.

    :returns: a 4-float tuple setting the margins from the sides of the page.
        ex. (0, 50, 0, 50).

    :param margins: (
        float
        | tuple[float]
        | tuple[float, float]
        | tuple[float, float, float, float]
    ): a float, a 1-tuple float, a 2-tuple float or a 4-tuple float
        that sets the requested margins beyond which content shall not be
        considered:
        - single value: margin applicable to all sides
        - 2-tuple float: the top and bottom margins
        - 4-tuple float: left-top-right-bottom margins
        Default to (0, 50, 0, 50) clockwise from left, from the page's
        margin, in the main decorator.

    '''
    # If margin is a float or an int,
    # then this should apply to all the margins
    if isinstance(margins, (float, int)):
        return (margins,) * 4

    if not all(hasattr(margin, "__float__") for margin in margins):
        raise ValueError("margin values must be floats")

    # if margins tuple has only 1 member
    # then this shall be the margin for all 4 sides
    if len(margins) == 1:
        _margin: float = margins[0]
        return (_margin,) * 4

    # if margins has only 2 members,
    # these two members are the horizontal margins
    elif len(margins) == 2:
        return (0, margins[0], 0, margins[1])  # type: ignore

    elif len(margins) != 4:
        raise ValueError(
            "margins must be one float or a "
            "tuple of one, two or four floats"
        )

    else:
        # Else return the margins as is
        return margins  # type: ignore


def _validate_table_strategy(table_strategy: str) -> str:
    '''
    Validates that the passed-in table_strategy is in the list of
    acceptable values for pymupdf and sets it to 'lines_strict' if not.

    :param table_strategy: str: the table strategy defined by the user.
    '''
    if table_strategy not in (['lines', 'lines_strict', 'text']):
        logger.info(
            msg=(
                f"table_strategy '{table_strategy}' not in "
                "['lines', 'lines_strict', 'text']; automatically reset "
                "to 'lines_strict'."
            )
        )
        return 'lines_strict'

    return table_strategy


def _make_header_identifier(
    doc: pymupdf.Document,
    pages: list[int],
    hdr_info: Any | None = None,
) -> Callable:
    '''
    Makes a header identifier Callable, either using the argument
    passed in the hdr_info parameter or creating it from a
    statistical analysis of the passed-in document using
    the font sizes as header level indicators.

    doc: pymupdf.Document: the pymupdf document currently being
        processed.
    pages: list[int]: the list of page numbers to be processed. 0-based.
    hdr_info: Any | None = None: either a Callable, or an object
        having a method get_header_id, or False, or anything else.
    '''
    _get_header_id: Callable

    # if hdr_info is callable, use it
    if callable(hdr_info):
        _get_header_id = hdr_info

    # if hdr_info is an object with a method get_header_id
    elif (
        hdr_info is not None
        and hasattr(hdr_info, "get_header_id")
        and callable(hdr_info.get_header_id)
    ):
        _get_header_id = hdr_info.get_header_id

    # if hdr_info is False, the user does not want to identify
    # header: set get_header_id to a function returning an empty
    # string
    elif hdr_info is False:

        def _get_header_id(*args, **kwargs):
            return ""

    # if hdr_info is anything else, build the header identifier
    # from the IdentifyHeaders class
    else:

        # hdr_info = IdentifyHeaders(source=doc)
        # _get_header_id = hdr_info.get_header_md_mark
        hdr_info = IdentifyHeaders(doc=doc, pages=pages)
        _get_header_id = hdr_info.get_header_id

    return _get_header_id


############################
# Partial decorator
############################


def process_doc_decorator(
    _func: Any | None = None,
    *,
    hdr_info: Any | None = None,
    # NOTE: consider the following (changed in the original pymupdf4llm)
    # textflags: Union[int, int] = pymupdf.TEXT_MEDIABOX_CLIP,
    textflags: Union[int, int] = (
        pymupdf.TEXT_MEDIABOX_CLIP | pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE
    ),
    # image_path: str = "",
    image_path: str = "test_data/images/",
    image_format: str = "png",
    image_size_limit: float = 0.05,
    dpi: int = 150,
    page_width: float = 595,
    page_height: float = 842,
    graphics_limit: int | None = None,
    fontsize_limit: float = 3,
    ignore_code: bool = False,
):
    '''
    Partial decorator for the processing of a document by one of
    the doc_processor.

    Sets the default parameters for the md_converters to avoid having
    them passed as arguments in the functions.

    :param textflags: Union[int, int] = (
        pymupdf.TEXT_MEDIABOX_CLIP
        | pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE
    ): the applicable text flags for the TextPages extraction. Union
        in this context is equivalent to adding the values of
        the respective textflags.
        Defaults to the union of pymupdf.TEXT_MEDIABOX_CLIP
        (64: characters entirely outside the page's mediabox are ignored)
        and pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE (128: use raw character
        codes instead of U+FFFD when encoding information is missing
        or uncertain).

    :param hdr_info: Any | None = None: callable or object having a method
        named 'get_hdr_info' or None or False. If False, no header
        detection method will be enforced. If None, a statistical method
        will be used to build a header identifier.

    :param image_path: str: folder into which images should be stored.

    :param image_format: str: desired image extension. Defaults to
        'png'.

    :param image_size_limit: float = 0.05: thresholds (as a proporition
        of the page's edges beyong which the images shall be ignored
        in the `write_image` module).

    :param dpi: int = 150: desired resolution for generated images.

    :param page_width: float = 595: page width. Default 595
        (A4 portrait).

    :param page_height: float = 842: page height. Default 842
        (A4 portrait)

    :param graphics_limit: int: vector graphics number thresholds
        beyond which a page shall be ignored for having too many
        vector graphics.

    :param fontsize_limit: float = 3: [___]

    :param ignore_code: bool = False: a boolean setting whether
        to mark monosized text as monosized or treat it as
        any other text. Usefull for documents which are all monos,
        such as emails in text format or OCRed faxes.
    '''
    # ######################
    # Set the PARAM dictionary
    # ######################

    IMG_PATH: str = image_path

    PARAM: dict[str, str | int | float | bool | None] = {
        'IMG_PATH': IMG_PATH,
        'IMG_EXTENSION': image_format,
        'DPI': dpi,
        'GRAPHICS_LIMIT': graphics_limit,
        'IGNORE_CODE': ignore_code,
        'image_size_limit': image_size_limit,
        'FONTSIZE_LIMIT': fontsize_limit,
    }

    def process_doc_inner_decorator(
        doc_processor: Callable,
    ) -> Callable:
        '''
        Closure decorator function that passes the passed-in doc_processor
        function to its wrapper function and returns the wrapper function,
        ready to be called.

        :param doc_processor: Callable: doc_processor is one of functions
            in `main` module (for instance, `to_markdown_gen` or
            `to_markdown_list`).
        '''

        @functools.wraps(doc_processor)
        def process_doc_wrapper(
            doc: pymupdf.Document | str,
            pages: list[int] | None = None,
            write_images: bool = False,
            embed_images: bool = False,
            force_text: bool = True,
            margins: (
                float
                | tuple[float]
                | tuple[float, float]
                | tuple[float, float, float, float]
            ) = (0, 50, 0, 50),
            table_strategy: str = "lines_strict",
            # extract_words: bool = False,
            eol_y_thresholds: float = 1.4,
            *args,
            **kwargs,
        ) -> Any | None:
            '''
            This wrapper validates and prepares the extraction parameters
            from the default and passed-in parameters, performs some doc
            level actions then calls the decorated function to process
            the document with these parameters.

            It returns either a single md string for the all the
            processed pages or a list of dict containing the md string
            and additional information for each page depending
            on the decorated function.

            All the parameters are optional, except for the doc.

            :param doc: pymupdf.Document. Only required parameter.

            :param pages: list[int]: list of page numbers to consider
                (0-based).

            :param write_images: bool: whether to save images / drawing as
                files.

            :param embed_images: bool: whether to embed images as base64
                encoded strings.

            :param force_text: bool: whether to output text despite of
                background.

            :param margins: (
                    float
                    | tuple[float]
                    | tuple[float, float]
                    | tuple[float, float, float, float]
                ): page margins beyond which content shall not be considered.
                Defaults to (0, 50, 0, 50) clockwise from left, from the page's
                margin.

            :param table_strategy: str: the table detection strategy. Valid
                values are "lines", "lines_strict" and "text". Default is
                "lines_strict" (ignores borderless rectangle vector graphics).
                "lines" uses all vector graphics on the page to detect grid
                lines.
                "text": text positions are used to generate "virtual" column
                and / or row boundaries

            :param eol_y_thresholds: float = 1.4: when printing out lines,
                lines pertaining to the same block shall not in principle
                be terminated by an eol character ('\n'). However, if the
                current line pertaining to the same block as the previous
                one has a y gap above this thresholds (in proporition of
                the current line's height), an eol character ('\n') shall
                be prepended to the current line.

            '''
            # ######################
            # Validate image parameters
            # ######################
            if embed_images is True:
                write_images = False
                PARAM['IMG_PATH'] = ""

            # Create the image directory in case it does not already exists
            if (
                PARAM['IMG_PATH']
                and write_images is True
                and not os.path.exists(IMG_PATH)
            ):
                os.mkdir(IMG_PATH)

            # ######################
            # Open the doc if doc is a file path
            # After this, doc is necessarily a pymupdf.Document
            # ######################

            if not isinstance(doc, pymupdf.Document):
                doc = pymupdf.open(doc)

            # ######################
            # Handling reflowable documents
            # ######################

            _make_doc_layout_for_reflowable_docs(
                doc=doc, page_width=page_width, page_height=page_height
            )

            # ######################
            # Page selection settings
            # ######################

            if pages is None:  # use all pages if no selection given
                pages = list(range(doc.page_count))

            # ######################
            # Margins settings and validation
            # ######################

            margins = _validate_margins(margins=margins)

            # ######################
            # Tables strategy validation
            # ######################

            table_strategy = _validate_table_strategy(
                table_strategy=table_strategy
            )

            # ######################
            # HDR classifier validation and setting
            # ######################

            # If "hdr_info" is not either a callable, an object with a
            # method "get_header_id" or False, scan the document and use
            # font sizes as header level indicators.

            # Define a get_header_id Callable variable
            _get_header_id: Callable = _make_header_identifier(
                doc=doc, pages=pages, hdr_info=hdr_info
            )

            # ######################
            # Update the PARAM dict with write_images, embed_images
            # and force_text arguments
            # ######################

            PARAM.update(
                {
                    'write_images': write_images,
                    'embed_images': embed_images,
                    'force_text': force_text,
                    'eol_y_thresholds': eol_y_thresholds,
                }
            )

            # ##########################################
            # Actual processing
            # ##########################################

            # doc_processor is one of the function in `main`
            # module
            document_output: Any | None = doc_processor(
                doc=doc,
                pages=pages,
                textflags=textflags,
                get_header_id=_get_header_id,
                margins=margins,
                table_strategy=table_strategy,
                PARAM=PARAM,
            )

            return document_output

        return process_doc_wrapper

    # If called without keyword arguments, the default values
    # apply
    if _func is None:

        return process_doc_inner_decorator

    # If called with keyword arguments, the passed-in keywords
    # arguments apply
    else:

        return process_doc_inner_decorator(doc_processor=_func)


############################
# Document metadata extraction
############################


def get_metadata(doc: pymupdf.Document, pno: int) -> dict:
    '''
    Extracts the metadata from the document and returns it
    as a dict.

    :param doc: pymupdf.Document: the document being processed.
    :param pno: int: number of pages in the document.
    '''
    meta = doc.metadata.copy()
    meta["file_path"] = doc.name
    meta["page_count"] = doc.page_count
    meta["page"] = pno + 1
    return meta
