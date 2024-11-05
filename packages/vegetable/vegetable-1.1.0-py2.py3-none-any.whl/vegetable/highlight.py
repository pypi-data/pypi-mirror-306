from abc import ABC, abstractmethod
from collections.abc import Iterable
from colored import Style
import re
import logging
import pdb

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Highlighter(ABC):
    """
    Base class for table element highlighting functors.
    """

    def __init__(self, reset=True, trim=True):
        """
        Base class initialization.

        Args:
            reset (bool, optional): if True, reset text attributes after the highlight of each field.
            trim (bool, optional): if True, apply text attributes to the field value excluding lead and trailing whitespace.
        """
        self.reset = reset
        self.trim = trim

    @abstractmethod
    def __call__(self, value, string, column, row_idx):
        """
        Apply the highlight to a value. Must be implemented by derived classes.

        Args:
            value (any type): the value in the source data before any formatting has been applied.
            string (str): the formatted string value of the field including whitespace padding.
            column (TableColumn): link to column (and table) details.
            row_idx (int or None): data row number if known, if not (i.e. line-by-line mode) will be None.
        """
        pass

    def apply(self, string, attribs):
        """
        Insert attributes - should be called from __call__() if the highlighter is a match.

        Args:
            string (str): the formatted and whitespace-padded field value to highlight.
            attribs (str, list, tuple or set): the text attributes (escape sequences) to apply.
        """
        if attribs is None or len(attribs) == 0:
            return string
        pre, value, post = self.split_ws(string)
        result = pre
        if type(attribs) in (list, tuple, set):
            result += "".join(attribs)
        else:
            result += attribs
        result += value
        if self.reset:
            result += Style.reset
        return result + post

    def split_ws(self, string):
        """
        Split a string value into a tuple of leading whitespace, formatted value and trailing whitespace.
        """
        try:
            if self.trim:
                try:
                    m = re.match(r"(\s*)(.*)(\s*)$", string)
                    if m:
                        return m.group(1), m.group(2), m.group(3)
                except:
                    pass
            return "", string, ""
        except:
            log.debug("while splitting to whitespace and value", exc_info=True)
            return "", string, ""


class NumberRange:
    """
    Utilty class to determine if a numeric value is within a specified number range.

    Matching works like Python ranges i.e. 1-4 matches 1, 2, 3, but not 4
    """

    def __init__(self, *args):
        """
        Create a NumberRange object from either a string or an iterable with two numeric values.

        If *args contains a single value, it is assumed to be a string. It can take for form of
        "m-", "m-n" or "-n" where "m" and "n" are integers or floats..

        If *args has two elements, they are assumed to be numeric lower and upper bounds (or None
        for unbounded on lower or upper end).
        """
        assert len(args) in (1, 2)
        if len(args) == 1:
            assert type(args[0]) is str
            s, e = args[0].split("-")
            self.start = None if s == "" else float(s)
            self.end = None if e == "" else float(e)
        else:
            self.start, self.end = [None if x is None else float(x) for x in args]
        assert sum([1 if type(x) is float else 0 for x in [self.start, self.end]]) > 0

    def __contains__(self, value):
        """
        Return True if the specified value is within the NumberRange,
        i.e. start <= value < end
        """
        if self.start is not None and value < self.start:
            return False
        if self.end is not None and value >= self.end:
            return False
        return True


class HighlightRange(Highlighter):
    """
    Highlight based on field value. e.g. if a field value is less than 20, use green text,
    but >= 20, use red text.

    The value will be case to the column type before testing, so make sure the column type
    is numeric.
    """

    def __init__(self, ranges, reset=True, trim=True):
        """
        Create object.

        Args:
            ranges (list of tuples): each tuple is (NumberRange string, text attribute(s))

        Example:

        HighlightRange(
            [
                ("-100",      None),
                ((100, 150"), Fore.yellow),
                ((100, None), [Fore.red, Style.bold]),
            ]
        )
        """
        super().__init__(reset, trim)
        self.ranges = list()
        for r, a in ranges:
            if a is not None:
                self.ranges.append((NumberRange(r), a))

    def __call__(self, value, string, column, row_idx):
        # pdb.set_trace()
        try:
            for r, a in self.ranges:
                if column.type(value) in r:
                    return self.apply(string, a)
        except:
            log.debug(
                f"while testing range for {value!r} row={row_idx!r} col={column.name}",
                exc_info=True,
            )
        return string


class HighlightValue(Highlighter):
    """
    Highlight based the value in a cell. User provides condition evaluation function.
    """

    def __init__(self, condition, style, reset=True, trim=True):
        """
        Create a HighlightValue

        Args:
            condition (fn(arg) -> bool): is called for each value with the value as the argument, returns True/False.
            style (str or list): a text attribute (or list of attributes) to apply when condition returns True.
        """
        super().__init__(reset, trim)
        self.condition = condition
        self.style = style

    def __call__(self, value, string, column, row_idx):
        try:
            if self.condition(value):
                return self.apply(string, self.style)
        except:
            log.debug(
                "while testing condition for {value!r} row={row_idx!r} col={column.name}",
                exc_info=True,
            )
        return string


class HighlightRownum(Highlighter):
    """
    Highlight based on row number (startin at 1).
    """

    def __init__(self, condition, style, reset=True, trim=True):
        """
        Create a highlighter based on row number.

        Args:
            condition (fn(arg) -> bool): function called with row number and returns True or False.
            style (str or list): a text attribute (or list of attributes) to apply when condition returns True.
        """
        super().__init__(reset, trim)
        self.condition = condition
        self.style = style

    def __call__(self, value, string, column, row_idx):
        try:
            if self.condition(row_idx + 1):
                return self.apply(string, self.style)
        except:
            log.debug(
                "while testing condition for {value!r} row={row_idx!r} col={column.name}",
                exc_info=True,
            )
        return string


class HighlightTrend(Highlighter):
    """
    Highlight based on differences between rows in a table (either ffrom previous row, or from first row).

    The column type is used to cast the value before testing - the type should be numeric (i.e. float or
    int).
    """

    def __init__(
        self,
        rising,
        falling,
        no_change=None,
        compared_to_first=False,
        reset=True,
        trim=True,
    ):
        """
        Create a HighlightTrend object.

        Args:
            rising (str or list): a text attribute (or list of attributes) to apply when value is > previous row.
            falling (str or list): a text attribute (or list of attributes) to apply when value < prevous row.
            no_change (str or list): a text attribute (or list of attributes) to apply when value == previous row.
            compared_to_first (bool): instead of comparing value to the previous row, compare to the first row.
            rising (str or list):
        """
        super().__init__(reset, trim)
        self.rising = rising
        self.falling = falling
        self.no_change = no_change
        self.compared_to_first = compared_to_first

    def __call__(self, value, string, column, row_idx):
        try:
            style = self.no_change
            data = column.table.data
            if row_idx is None or row_idx <= 0 or value is None:
                pass
            else:
                if self.compared_to_first:
                    prev = data[0].get(column.name)
                else:
                    prev = data[row_idx - 1].get(column.name)
                if prev is None:
                    pass
                else:
                    # Avoid problems with type mismatches, e.g. str < int
                    prev = column.type(prev)
                    if value > prev:
                        style = self.rising
                    elif value < prev:
                        style = self.falling
            return self.apply(string, style)
        except:
            log.debug(
                "while determining trend for {value!r} row={row_idx!r} col={column.name}",
                exc_info=True,
            )
        return string


class HighlightMinMax(Highlighter):
    """
    Highlight the minimum and maximum values in a column.

    The column values are case to the type of the column before evaluation, so make sure the column type is
    numeric (i.e. float or int) to avoid unusual behavior.
    """

    def __init__(self, min=None, max=None, reset=True, trim=True):
        """
        Create a HighlightTrend object.

        Args:
            min (str or list): a text attribute (or list of attributes) to apply when value is minimum in column.
            max (str or list): a text attribute (or list of attributes) to apply when value is maximum in column.
        """
        super().__init__(reset, trim)
        self.min_style = min
        self.max_style = max

    def __call__(self, value, string, column, row_idx):
        try:
            if self.min_style is None and self.max_style is None:
                return string

            if column.table.limit is None:
                data = column.table.data
            else:
                data = column.table.data[: column.table.limit]

            styles = []

            def append_style(style):
                if isinstance(style, Iterable):
                    for s in style:
                        styles.append(s)
                else:
                    styles.append(style)

            def force_type(v):
                if v is None:
                    return None
                try:
                    return column.type(v)
                except:
                    return None

            column_values = [force_type(x.get(column.name)) for x in data]
            if self.min_style is not None:
                try:
                    if value <= min(filter(lambda x: x is not None, column_values)):
                        append_style(self.min_style)
                except:
                    pass
            if self.max_style is not None:
                try:
                    if value >= max(filter(lambda x: x is not None, column_values)):
                        append_style(self.max_style)
                except:
                    pass

            if len(styles) > 0:
                return self.apply(string, styles)
            else:
                return string
        except:
            log.error(
                "while determining minmax for {value!r} row={row_idx!r} col={column.name}",
                exc_info=True,
            )
        return string
