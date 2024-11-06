# settings.py
'''
Encapsulation of some of the subfunctions of the interface
function `find_table`.
'''


from dataclasses import dataclass
from operator import itemgetter

from pymupdf import (  # type: ignore
    TOOLS,
    Matrix,
    Page,
)


class UnsetFloat(float):
    pass


NON_NEGATIVE_SETTINGS = [
    "snap_tolerance",
    "snap_x_tolerance",
    "snap_y_tolerance",
    "join_tolerance",
    "join_x_tolerance",
    "join_y_tolerance",
    "edge_min_length",
    "min_words_vertical",
    "min_words_horizontal",
    "intersection_tolerance",
    "intersection_x_tolerance",
    "intersection_y_tolerance",
]


TABLE_STRATEGIES = ["lines", "lines_strict", "text", "explicit"]
UNSET = UnsetFloat(0)
DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 1
DEFAULT_X_TOLERANCE = 3
DEFAULT_Y_TOLERANCE = 3
DEFAULT_X_DENSITY = 7.25
DEFAULT_Y_DENSITY = 13
bbox_getter = itemgetter("x0", "top", "x1", "bottom")


@dataclass
class TableSettings:
    vertical_strategy: str = "lines"
    horizontal_strategy: str = "lines"
    explicit_vertical_lines: list | None = None
    explicit_horizontal_lines: list | None = None
    snap_tolerance: float = DEFAULT_SNAP_TOLERANCE
    snap_x_tolerance: float = UNSET
    snap_y_tolerance: float = UNSET
    join_tolerance: float = DEFAULT_JOIN_TOLERANCE
    join_x_tolerance: float = UNSET
    join_y_tolerance: float = UNSET
    edge_min_length: float = 3
    min_words_vertical: float = DEFAULT_MIN_WORDS_VERTICAL
    min_words_horizontal: float = DEFAULT_MIN_WORDS_HORIZONTAL
    intersection_tolerance: float = 3
    intersection_x_tolerance: float = UNSET
    intersection_y_tolerance: float = UNSET
    text_settings: dict | None = None

    def __post_init__(self) -> "TableSettings":  # type: ignore
        """Clean up user-provided table settings.

        Validates that the table settings provided consists
        of acceptable values and returns a cleaned up version.
        The cleaned up version fills out the missing
        values with the default values in the provided settings.

        TODO: Can be further used to validate that the values
            are of the correct type. For example, raising
            a value error when a non-boolean input is
            provided for the key ``keep_blank_chars``.

        :param table_settings: User-provided table settings.
        :returns: A cleaned up version of the user-provided table settings.
        :raises ValueError: When an unrecognised key is provided.
        """

        for setting in NON_NEGATIVE_SETTINGS:
            if (getattr(self, setting) or 0) < 0:
                raise ValueError(
                    f"Table setting '{setting}' cannot be negative"
                )

        for orientation in ["horizontal", "vertical"]:
            strategy = getattr(self, orientation + "_strategy")
            if strategy not in TABLE_STRATEGIES:
                raise ValueError(
                    f"{orientation}_strategy must be one of"
                    f'{{{",".join(TABLE_STRATEGIES)}}}'
                )

        if self.text_settings is None:
            self.text_settings = {}

        # This next section is for backwards compatibility
        for attr in ["x_tolerance", "y_tolerance"]:
            if attr not in self.text_settings:
                self.text_settings[attr] = self.text_settings.get(
                    "tolerance", 3
                )

        if "tolerance" in self.text_settings:
            del self.text_settings["tolerance"]
        # End of that section

        for attr, fallback in [
            ("snap_x_tolerance", "snap_tolerance"),
            ("snap_y_tolerance", "snap_tolerance"),
            ("join_x_tolerance", "join_tolerance"),
            ("join_y_tolerance", "join_tolerance"),
            ("intersection_x_tolerance", "intersection_tolerance"),
            ("intersection_y_tolerance", "intersection_tolerance"),
        ]:
            if getattr(self, attr) is UNSET:
                setattr(self, attr, getattr(self, fallback))

        return self

    @classmethod
    def resolve(cls, settings=None):
        if settings is None:
            return cls()
        elif isinstance(settings, cls):
            return settings
        elif isinstance(settings, dict):
            core_settings = {}
            text_settings = {}
            for k, v in settings.items():
                if k[:5] == "text_":
                    text_settings[k[5:]] = v
                else:
                    core_settings[k] = v
            core_settings["text_settings"] = text_settings
            return cls(**core_settings)
        else:
            raise ValueError(f"Cannot resolve settings: {settings}")


def page_rotation_set0(page):
    """Nullify page rotation.

    To correctly detect tables, page rotation must be zero.
    This function performs the necessary adjustments and returns information
    for reverting this changes.
    """
    mediabox = page.mediabox
    rot = page.rotation  # contains normalized rotation value
    # need to derotate the page's content
    mb = page.mediabox  # current mediabox

    if rot == 90:
        # before derotation, shift content horizontally
        mat0 = Matrix(1, 0, 0, 1, mb.y1 - mb.x1 - mb.x0 - mb.y0, 0)
    elif rot == 270:
        # before derotation, shift content vertically
        mat0 = Matrix(1, 0, 0, 1, 0, mb.x1 - mb.y1 - mb.y0 - mb.x0)
    else:
        mat0 = Matrix(1, 0, 0, 1, -2 * mb.x0, -2 * mb.y0)

    # prefix with derotation matrix
    mat = mat0 * page.derotation_matrix
    cmd = b"%g %g %g %g %g %g cm " % tuple(mat)
    xref = TOOLS._insert_contents(page, cmd, 0)

    # swap x- and y-coordinates
    if rot in (90, 270):
        x0, y0, x1, y1 = mb
        mb.x0 = y0
        mb.y0 = x0
        mb.x1 = y1
        mb.y1 = x1
        page.set_mediabox(mb)

    page.set_rotation(0)

    # refresh the page to apply these changes
    doc = page.parent
    pno = page.number
    page = doc[pno]
    return page, xref, rot, mediabox


def page_rotation_reset(page, xref, rot, mediabox):
    """Reset page rotation to original values.

    To be used before we return tables."""
    doc = page.parent  # document of the page
    doc.update_stream(xref, b" ")  # remove de-rotation matrix
    page.set_mediabox(mediabox)  # set mediabox to old value
    page.set_rotation(rot)  # set rotation to old value
    pno = page.number
    page = doc[pno]  # update page info
    return page


def configure_find_tables(
    page: Page,
    vertical_strategy: str,
    horizontal_strategy: str,
    vertical_lines: list | None,
    horizontal_lines: list | None,
    snap_tolerance: float,
    snap_x_tolerance: float | None,
    snap_y_tolerance: float | None,
    join_tolerance: float,
    join_x_tolerance: float | None,
    join_y_tolerance: float | None,
    edge_min_length: float,
    min_words_vertical: float,
    min_words_horizontal: float,
    intersection_tolerance: float,
    intersection_x_tolerance: float | None,
    intersection_y_tolerance: float | None,
    text_tolerance=3,
    text_x_tolerance=3,
    text_y_tolerance=3,
    strategy=None,  # offer abbreviation
):
    '''
    Function encapsulating the configuration steps when calling find_tables.
    '''
    old_small = bool(TOOLS.set_small_glyph_heights())  # save old value
    TOOLS.set_small_glyph_heights(True)  # we need minimum bboxes
    if page.rotation != 0:
        page, old_xref, old_rot, old_mediabox = page_rotation_set0(page)
    else:
        old_xref, old_rot, old_mediabox = None, None, None

    if snap_x_tolerance is None:
        snap_x_tolerance = UNSET
    if snap_y_tolerance is None:
        snap_y_tolerance = UNSET
    if join_x_tolerance is None:
        join_x_tolerance = UNSET
    if join_y_tolerance is None:
        join_y_tolerance = UNSET
    if intersection_x_tolerance is None:
        intersection_x_tolerance = UNSET
    if intersection_y_tolerance is None:
        intersection_y_tolerance = UNSET
    if strategy is not None:
        vertical_strategy = strategy
        horizontal_strategy = strategy

    settings = {
        "vertical_strategy": vertical_strategy,
        "horizontal_strategy": horizontal_strategy,
        "explicit_vertical_lines": vertical_lines,
        "explicit_horizontal_lines": horizontal_lines,
        "snap_tolerance": snap_tolerance,
        "snap_x_tolerance": snap_x_tolerance,
        "snap_y_tolerance": snap_y_tolerance,
        "join_tolerance": join_tolerance,
        "join_x_tolerance": join_x_tolerance,
        "join_y_tolerance": join_y_tolerance,
        "edge_min_length": edge_min_length,
        "min_words_vertical": min_words_vertical,
        "min_words_horizontal": min_words_horizontal,
        "intersection_tolerance": intersection_tolerance,
        "intersection_x_tolerance": intersection_x_tolerance,
        "intersection_y_tolerance": intersection_y_tolerance,
        "text_tolerance": text_tolerance,
        "text_x_tolerance": text_x_tolerance,
        "text_y_tolerance": text_y_tolerance,
    }
    tset = TableSettings.resolve(settings=settings)
    page.table_settings = tset

    return page, tset, old_small, old_xref, old_rot, old_mediabox
