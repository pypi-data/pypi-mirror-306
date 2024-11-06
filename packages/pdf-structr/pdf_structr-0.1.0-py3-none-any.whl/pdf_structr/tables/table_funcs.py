# table_funcs.py
'''
Modules encapsulating a set of subfunctions and classes for the table module.

Classes:
- TextMap
- WordMap
- WordExtractor

Functions:
- white_spaces              exported
- line_to_edge              exported
- cluster_list
- make_cluster_dict
- cluster_objects           exported
- merge_bboxes
- objects_to_bbox           exported
'''

import itertools
import string
from operator import itemgetter

from pdf_structr.tables.settings import (
    DEFAULT_X_DENSITY,
    DEFAULT_X_TOLERANCE,
    DEFAULT_Y_DENSITY,
    DEFAULT_Y_TOLERANCE,
    bbox_getter,
)

# -------------------------------
# Global variables
# -------------------------------


white_spaces = set(string.whitespace)  # for checking white space only cells


# -------------------------------------------------------------------
# End of PyMuPDF interface code
# -------------------------------------------------------------------


LIGATURES = {
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬆ": "st",
    "ﬅ": "st",
}


############################################################################
# Classes
############################################################################


class TextMap:
    """
    A TextMap maps each unicode character in the text to an individual `char`
    object (or, in the case of layout-implied whitespace, `None`).
    """

    def __init__(self, tuples=None) -> None:
        self.tuples = tuples
        self.as_string = "".join(map(itemgetter(0), tuples))

    def match_to_dict(
        self,
        m,
        main_group: int = 0,
        return_groups: bool = True,
        return_chars: bool = True,
    ) -> dict:
        start = m.start(main_group)
        end = m.end(main_group)
        subset = self.tuples[start:end]
        chars = [c for (text, c) in subset if c is not None]
        x0, top, x1, bottom = objects_to_bbox(chars)

        result = {
            "text": m.group(main_group),
            "x0": x0,
            "top": top,
            "x1": x1,
            "bottom": bottom,
        }

        if return_groups:
            result["groups"] = m.groups()

        if return_chars:
            result["chars"] = chars

        return result


class WordMap:
    """
    A WordMap maps words->chars.
    """

    def __init__(self, tuples) -> None:
        self.tuples = tuples

    def to_textmap(
        self,
        layout: bool = False,
        layout_width=0,
        layout_height=0,
        layout_width_chars: int = 0,
        layout_height_chars: int = 0,
        x_density=DEFAULT_X_DENSITY,
        y_density=DEFAULT_Y_DENSITY,
        x_shift=0,
        y_shift=0,
        y_tolerance=DEFAULT_Y_TOLERANCE,
        use_text_flow: bool = False,
        presorted: bool = False,
        expand_ligatures: bool = True,
    ) -> TextMap:
        """
        Given a list of (word, chars) tuples (i.e., a WordMap), return a list
        of (char-text, char) tuples (i.e., a TextMap) that can be used
        to mimic the structural layout of the text on the page(s), using
        the following approach:

        - Sort the words by (doctop, x0) if not already sorted.

        - Calculate the initial doctop for the starting page.

        - Cluster the words by doctop (taking `y_tolerance` into account), and
          iterate through them.

        - For each cluster, calculate the distance between that doctop and the
          initial doctop, in points, minus `y_shift`. Divide that distance by
          `y_density` to calculate the minimum number of newlines that
          should come before this cluster. Append that number of newlines
          *minus* the number of newlines already appended, with a minimum
          of one.

        - Then for each cluster, iterate through each word in it. Divide each
          word's x0, minus `x_shift`, by `x_density` to calculate the minimum
          number of characters that should come before this cluster. Append
          that number of spaces *minus* the number of characters and spaces
          already appended, with a minimum of one. Then append the word's text.

        - At the termination of each line, add more spaces if necessary to
          mimic `layout_width`.

        - Finally, add newlines to the end if necessary to mimic to
          `layout_height`.

        Note: This approach currently works best for horizontal, left-to-right
        text, but will display all words regardless of orientation. There is
        room for improvement in better supporting right-to-left text, as well
        as vertical text.
        """
        _textmap: list = []

        if not len(self.tuples):
            return TextMap(_textmap)

        expansions = LIGATURES if expand_ligatures else {}

        if layout:
            if layout_width_chars:
                if layout_width:
                    raise ValueError(
                        "`layout_width` and `layout_width_chars`"
                        " cannot both be set."
                    )
            else:
                layout_width_chars = int(round(layout_width / x_density))

            if layout_height_chars:
                if layout_height:
                    raise ValueError(
                        "`layout_height` and `layout_height_chars` "
                        "cannot both be set."
                    )
            else:
                layout_height_chars = int(round(layout_height / y_density))

            blank_line = [(" ", None)] * layout_width_chars
        else:
            blank_line = []

        num_newlines = 0

        words_sorted_doctop = (
            self.tuples
            if presorted or use_text_flow
            else sorted(self.tuples, key=lambda x: float(x[0]["doctop"]))
        )

        first_word = words_sorted_doctop[0][0]
        doctop_start = first_word["doctop"] - first_word["top"]

        for i, ws in enumerate(
            cluster_objects(
                words_sorted_doctop,
                lambda x: float(x[0]["doctop"]),
                y_tolerance,
            )
        ):
            y_dist = (
                (ws[0][0]["doctop"] - (doctop_start + y_shift)) / y_density
                if layout
                else 0
            )
            num_newlines_prepend = max(
                # At least one newline, unless this iis the first line
                int(i > 0),
                # ... or as many as needed to get the imputed "distance"
                # from the top
                round(y_dist) - num_newlines,
            )

            for _ in range(num_newlines_prepend):
                if not len(_textmap) or _textmap[-1][0] == "\n":
                    _textmap += blank_line
                _textmap.append(("\n", None))

            num_newlines += num_newlines_prepend

            line_len = 0

            line_words_sorted_x0 = (
                ws
                if presorted or use_text_flow
                else sorted(ws, key=lambda x: float(x[0]["x0"]))
            )

            for word, chars in line_words_sorted_x0:
                x_dist = (word["x0"] - x_shift) / x_density if layout else 0
                num_spaces_prepend = max(
                    min(1, line_len), round(x_dist) - line_len
                )
                _textmap += [(" ", None)] * num_spaces_prepend
                line_len += num_spaces_prepend

                for c in chars:
                    letters = expansions.get(c["text"], c["text"])
                    for letter in letters:
                        _textmap.append((letter, c))
                        line_len += 1

            # Append spaces at end of line
            if layout:
                _textmap += [(" ", None)] * (layout_width_chars - line_len)

        # Append blank lines at end of text
        if layout:
            num_newlines_append = layout_height_chars - (num_newlines + 1)
            for i in range(num_newlines_append):
                if i > 0:
                    _textmap += blank_line
                _textmap.append(("\n", None))

            # Remove terminal newline
            if _textmap[-1] == ("\n", None):
                _textmap = _textmap[:-1]

        return TextMap(_textmap)


class WordExtractor:
    def __init__(
        self,
        x_tolerance=DEFAULT_X_TOLERANCE,
        y_tolerance=DEFAULT_Y_TOLERANCE,
        keep_blank_chars: bool = False,
        use_text_flow=False,
        horizontal_ltr=True,  # Should words be read left-to-right?
        vertical_ttb=False,  # Should vertical words be read top-to-bottom?
        extra_attrs=None,
        split_at_punctuation=False,
        expand_ligatures=True,
    ):
        self.x_tolerance = x_tolerance
        self.y_tolerance = y_tolerance
        self.keep_blank_chars = keep_blank_chars
        self.use_text_flow = use_text_flow
        self.horizontal_ltr = horizontal_ltr
        self.vertical_ttb = vertical_ttb
        self.extra_attrs = [] if extra_attrs is None else extra_attrs

        # Note: string.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.split_at_punctuation = (
            string.punctuation
            if split_at_punctuation is True
            else (split_at_punctuation or "")
        )

        self.expansions = LIGATURES if expand_ligatures else {}

    def merge_chars(self, ordered_chars):
        x0, top, x1, bottom = objects_to_bbox(ordered_chars)
        doctop_adj = ordered_chars[0]["doctop"] - ordered_chars[0]["top"]
        upright = ordered_chars[0]["upright"]
        direction = (
            1
            if (self.horizontal_ltr if upright else self.vertical_ttb)
            else -1
        )

        matrix = ordered_chars[0]["matrix"]

        rotation = 0
        if not upright and matrix[1] < 0:
            ordered_chars = reversed(ordered_chars)
            rotation = 270

        if matrix[0] < 0 and matrix[3] < 0:
            rotation = 180
        elif matrix[1] > 0:
            rotation = 90

        word = {
            "text": "".join(
                self.expansions.get(c["text"], c["text"])
                for c in ordered_chars
            ),
            "x0": x0,
            "x1": x1,
            "top": top,
            "doctop": top + doctop_adj,
            "bottom": bottom,
            "upright": upright,
            "direction": direction,
            "rotation": rotation,
        }

        for key in self.extra_attrs:
            word[key] = ordered_chars[0][key]

        return word

    def char_begins_new_word(
        self,
        prev_char,
        curr_char,
    ) -> bool:
        """This method takes several factors into account to determine if
        `curr_char` represents the beginning of a new word:

        - Whether the text is "upright" (i.e., non-rotated)
        - Whether the user has specified that horizontal text runs
          left-to-right (default) or right-to-left, as represented by
          self.horizontal_ltr
        - Whether the user has specified that vertical text the text runs
          top-to-bottom (default) or bottom-to-top, as represented by
          self.vertical_ttb
        - The x0, top, x1, and bottom attributes of prev_char and
          curr_char
        - The self.x_tolerance and self.y_tolerance settings. Note: In
          this case, x/y refer to those directions for non-rotated text.
          For vertical text, they are flipped. A more accurate terminology
          might be "*intra*line character distance tolerance" and
          "*inter*line character distance tolerance"

        An important note: The *intra*line distance is measured from the
        *end* of the previous character to the *beginning* of the current
        character, while the *inter*line distance is measured from the
        *top* of the previous character to the *top* of the next
        character. The reasons for this are partly repository-historical,
        and partly logical, as successive text lines' bounding boxes often
        overlap slightly (and we don't want that overlap to be interpreted
        as the two lines being the same line).

        The upright-ness of the character determines the attributes to
        compare, while horizontal_ltr/vertical_ttb determine the direction
        of the comparison.
        """

        # Note: Due to the grouping step earlier in the process,
        # curr_char["upright"] will always equal prev_char["upright"].
        if curr_char["upright"]:
            x = self.x_tolerance
            y = self.y_tolerance
            ay = prev_char["top"]
            cy = curr_char["top"]
            if self.horizontal_ltr:
                ax = prev_char["x0"]
                bx = prev_char["x1"]
                cx = curr_char["x0"]
            else:
                ax = -prev_char["x1"]
                bx = -prev_char["x0"]
                cx = -curr_char["x1"]

        else:
            x = self.y_tolerance
            y = self.x_tolerance
            ay = prev_char["x0"]
            cy = curr_char["x0"]
            if self.vertical_ttb:
                ax = prev_char["top"]
                bx = prev_char["bottom"]
                cx = curr_char["top"]
            else:
                ax = -prev_char["bottom"]
                bx = -prev_char["top"]
                cx = -curr_char["bottom"]

        return bool(
            # Intraline test
            (cx < ax)
            or (cx > bx + x)
            # Interline test
            or (cy > ay + y)
        )

    def iter_chars_to_words(self, ordered_chars):
        current_word = []

        def start_next_word(new_char=None):
            nonlocal current_word

            if current_word:
                yield current_word

            current_word = [] if new_char is None else [new_char]

        for char in ordered_chars:
            text = char["text"]

            if not self.keep_blank_chars and text.isspace():
                yield from start_next_word(None)

            elif text in self.split_at_punctuation:
                yield from start_next_word(char)
                yield from start_next_word(None)

            elif current_word and self.char_begins_new_word(
                current_word[-1], char
            ):
                yield from start_next_word(char)

            else:
                current_word.append(char)

        # Finally, after all chars processed
        if current_word:
            yield current_word

    def iter_sort_chars(self, chars):
        def upright_key(x) -> int:
            return -int(x["upright"])

        for upright_cluster in cluster_objects(list(chars), upright_key, 0):
            upright = upright_cluster[0]["upright"]
            cluster_key = "doctop" if upright else "x0"

            # Cluster by line
            subclusters = cluster_objects(
                upright_cluster, itemgetter(cluster_key), self.y_tolerance
            )

            for sc in subclusters:
                # Sort within line
                sort_key = "x0" if upright else "doctop"
                to_yield = sorted(sc, key=itemgetter(sort_key))

                # Reverse order if necessary
                if not (self.horizontal_ltr if upright else self.vertical_ttb):
                    yield from reversed(to_yield)
                else:
                    yield from to_yield

    def iter_extract_tuples(self, chars):
        ordered_chars = (
            chars if self.use_text_flow else self.iter_sort_chars(chars)
        )

        grouping_key = itemgetter("upright", *self.extra_attrs)
        grouped_chars = itertools.groupby(ordered_chars, grouping_key)

        for _, char_group in grouped_chars:
            for word_chars in self.iter_chars_to_words(char_group):
                yield (self.merge_chars(word_chars), word_chars)

    def extract_wordmap(self, chars) -> WordMap:
        return WordMap(list(self.iter_extract_tuples(chars)))

    def extract_words(self, chars: list) -> list:
        words = [word for word, word_chars in self.iter_extract_tuples(chars)]
        return words


############################################################################
# Functions
############################################################################


def line_to_edge(line):
    edge = dict(line)
    edge["orientation"] = "h" if (line["top"] == line["bottom"]) else "v"
    return edge


def cluster_list(xs, tolerance=0) -> list:
    if tolerance == 0:
        return [[x] for x in sorted(xs)]
    if len(xs) < 2:
        return [[x] for x in sorted(xs)]
    groups = []
    xs = sorted(xs)
    current_group = [xs[0]]
    last = xs[0]
    for x in xs[1:]:
        if x <= (last + tolerance):
            current_group.append(x)
        else:
            groups.append(current_group)
            current_group = [x]
        last = x
    groups.append(current_group)
    return groups


def make_cluster_dict(values, tolerance) -> dict:
    clusters = cluster_list(list(set(values)), tolerance)

    nested_tuples = [
        [(val, i) for val in value_cluster]
        for i, value_cluster in enumerate(clusters)
    ]

    return dict(itertools.chain(*nested_tuples))


def cluster_objects(xs, key_fn, tolerance) -> list:
    if not callable(key_fn):
        key_fn = itemgetter(key_fn)

    values = map(key_fn, xs)
    cluster_dict = make_cluster_dict(values, tolerance)

    get_0, get_1 = itemgetter(0), itemgetter(1)

    cluster_tuples = sorted(
        ((x, cluster_dict.get(key_fn(x))) for x in xs), key=get_1
    )

    grouped = itertools.groupby(cluster_tuples, key=get_1)

    return [list(map(get_0, v)) for k, v in grouped]


def merge_bboxes(bboxes):
    """
    Given an iterable of bounding boxes, return the smallest bounding box
    that contains them all.
    """
    x0, top, x1, bottom = zip(*bboxes)
    return (min(x0), min(top), max(x1), max(bottom))


def objects_to_bbox(objects):
    """
    Given an iterable of objects, return the smallest bounding box that
    contains them all.
    """
    return merge_bboxes(map(bbox_getter, objects))
