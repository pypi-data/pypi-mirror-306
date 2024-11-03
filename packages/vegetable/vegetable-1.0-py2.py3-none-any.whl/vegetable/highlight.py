from abc import ABC, abstractmethod
from collections.abc import Iterable
from colored import Style


class Highlighter(ABC):
    def __init__(self, reset):
        self.apply = self.apply_with_reset if reset else self.apply_no_reset

    @abstractmethod
    def __call__(self, value, string, column, row_idx):
        pass

    def apply_no_reset(self, string, attribs):
        if attribs is None:
            return string
        result = ""
        if type(attribs) in (list, tuple, set):
            result += "".join(attribs)
        else:
            result += attribs
        return result + string

    def apply_with_reset(self, string, attribs):
        return self.apply_no_reset(string, attribs) + Style.reset


class NumberRange:
    def __init__(self, *args):
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
        if self.start is not None and value < self.start:
            return False
        if self.end is not None and value >= self.end:
            return False
        return True


class HighlightRange(Highlighter):
    def __init__(self, ranges, reset=True):
        """ranges is a list of tuples with the first element being some argument that
        can be used to initialize a NumberRange, and the second is an iterable of
        "coloured" formatting attributes, e.g.

        HighlightRange([
            ("-100",      None),
            ((100, 150"), Fore.yellow),
            ((100, None), [Fore.red, Style.bold]),
        ])
        """
        super(HighlightRange, self).__init__(reset)
        self.ranges = list()
        for r, a in ranges:
            if a is not None:
                self.ranges.append((NumberRange(r), a))

    def __call__(self, value, string, column, row_idx):
        for r, a in self.ranges:
            if value in r:
                return self.apply(string, a)
        return string


class HighlightValue(Highlighter):
    def __init__(self, condition, style, reset=True):
        super(HighlightValue, self).__init__(reset)
        self.condition = condition
        self.style = style

    def __call__(self, value, string, column, row_idx):
        if self.condition(value):
            return self.apply(string, self.style)
        else:
            return string


class HighlightRownum(Highlighter):
    def __init__(self, condition, style, reset=True):
        super(HighlightRownum, self).__init__(reset)
        self.condition = condition
        self.style = style

    def __call__(self, value, string, column, row_idx):
        if self.condition(row_idx + 1):
            return self.apply(string, self.style)
        else:
            return string


class HighlightTrend(Highlighter):
    def __init__(
        self, rising, falling, no_change=None, compared_to_first=False, reset=True
    ):
        super(HighlightTrend, self).__init__(reset)
        self.rising = rising
        self.falling = falling
        self.no_change = no_change
        self.compared_to_first = compared_to_first

    def __call__(self, value, string, column, row_idx):
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
                if value > prev:
                    style = self.rising
                elif value < prev:
                    style = self.falling
        return self.apply(string, style)


class HighlightMinMax(Highlighter):
    def __init__(self, min=None, max=None, reset=True):
        super(HighlightMinMax, self).__init__(reset)
        self.min_style = min
        self.max_style = max

    def __call__(self, value, string, column, row_idx):
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

        column_values = [x.get(column.name) for x in data]
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
