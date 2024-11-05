from abc import ABC, abstractmethod
import pdb


class ValueFormatter(ABC):
    @abstractmethod
    def __call__(self, value):
        pass


class StringFormatter(ValueFormatter):
    """
    Functor class (objects are callable), which format string values in a way that is suitable
    for output as fixed width columns in a table.
    """

    def __init__(self, width, align, fill=" "):
        """
        Create a functor object for formatting string values.

        Args:
            width (int): number of characters that the string will be padded to.
            align ("L", "R", or "C"): specify alignment - Left, Right or Center.
            fill (str of len 1): pad with specified fill character.
        """
        assert type(width) is int and width > 0
        assert type(align) is str and align in ("L", "R", "C")
        self.width = width
        self.align = {"L": "ljust", "R": "rjust", "C": "center"}[align]
        assert fill is None or (type(fill) is str and len(fill) == 1)
        self.fill = " " if fill is None else fill

    def __call__(self, value):
        """
        Takes a str value (or something that can be converted to a str, and returns a formatted string.
        """

        s = str(value)
        return getattr(s, self.align)(self.width, self.fill)


class FloatFormatter(ValueFormatter):
    """
    Functor class (objects are callable), which formats float values in a way that is suitable
    for output as fixed width columns in a table.
    """

    def __init__(self, width, scale, fill=False, plus=False, thousands=False):
        """
        Create a functor object for formatting floating point values.

        Args:
            width (int): number of characters of result when funtor is called.
            scale (int): the number of decimal places to display in result.
            fill (bool): if True pad on left with "0" (after sign). Note: padding will include thousand separators if requested.
            plus (bool): if True always show the sign, even if it's "+"
            thousands (bool): if True, include thousands separaors.
        """
        if scale is None:
            scale = 2
        assert type(width) is int and width > 0
        assert type(scale) is int and scale >= 0
        self.format = "{:"
        if plus:
            self.format += "+"
        if fill in ("0", True):
            self.format += "0"
        self.format += str(width)
        if thousands:
            self.format += ","
        self.format += "." + str(scale) + "f}"

    def __call__(self, value):
        """
        Takes a float value (or something that can be cast to a float, and returns a formatted string.
        """
        return str.format(self.format, float(value))

    def __str__(self):
        return f"float:{self.format}"


class IntFormatter(ValueFormatter):
    """
    Functor class (objects are callable), which formats integer values in a way that is suitable
    for output as fixed width columns in a table.
    """

    def __init__(self, width, fill=False, plus=False, thousands=False):
        """
        Create a functor object for formatting floating point values.

        Args:
            width (int): number of characters of result when funtor is called.
            fill (bool): if True pad on left with "0" (after sign). Note: padding will include thousand separators if requested.
            plus (bool): if True always show the sign, even if it's "+"
            thousands (bool): if True, include thousands separaors.
        """
        assert type(width) is int and width > 0
        self.format = "{:"
        if plus:
            self.format += "+"
        if fill in ("0", True):
            self.format += "0"
        self.format += str(width)
        if thousands:
            self.format += ","
        self.format += "d}"

    def __call__(self, value):
        """
        Takes an integer value (or something that can be cast to an int, and returns a formatted string.
        """
        return str.format(self.format, int(value))

    def __str__(self):
        return f"int:{self.format}"
