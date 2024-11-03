from abc import ABC, abstractmethod


class ValueFormatter(ABC):
    @abstractmethod
    def __call__(self, value):
        pass


class PaddedStringFormatter(ValueFormatter):
    def __init__(self, width, align, fill=None, fn=None):
        assert type(width) is int and width > 0
        assert type(align) is str and align in ("L", "R", "C")
        self.width = width
        self.align = {"L": "ljust", "R": "rjust", "C": "center"}[align]
        self.fill = " " if fill is None else fill
        self.fn = fn

    def __call__(self, value):
        if self.fn:
            s = self.fn(value)
        else:
            s = str(value)
        return getattr(s, self.align)(self.width, self.fill)


class FloatFormatter(ValueFormatter):
    def __init__(self, width, precision, fill, plus, thousands):
        assert type(width) is int and width > 0
        assert type(precision) is int and precision >= 0
        assert fill in ("", "0", None)
        assert type(plus) is bool
        self.format = "{:"
        if plus:
            self.format += "+"
        if fill == "0":
            self.format += "0"
        self.format += str(width)
        if thousands:
            self.format += ","
        self.format += "." + str(precision) + "f}"

    def __call__(self, value):
        return str.format(self.format, float(value))

    def __str__(self):
        return f"float:{self.format}"


class IntFormatter(ValueFormatter):
    def __init__(self, width, fill, plus, thousands):
        assert type(width) is int and width > 0
        assert fill in ("", "0", None)
        assert type(plus) is bool
        self.format = "{:"
        if plus:
            self.format += "+"
        if fill == "0":
            self.format += "0"
        self.format += str(width)
        if thousands:
            self.format += ","
        self.format += "d}"

    def __call__(self, value):
        return str.format(self.format, int(value))

    def __str__(self):
        return f"int:{self.format}"
