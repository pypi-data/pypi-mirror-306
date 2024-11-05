from vegetable.format import *


class TableColumn:
    """
    Object that holds formatting information for a column in a table.
    """

    def __init__(
        self,
        name,
        table,
        index,
        type=str,
        align=None,
        width=None,
        expand=True,
        nvl="",
        evl="?",
        fill=None,
        thousands=False,
        scale=None,
        plus=False,
        formatter=None,
        highlighter=None,
    ):
        """
        Create a TableColumn.

        Uses only the options appropriate for the column data type.

        Args:
            name (string): is the title of the column that will appear in table headers.
            table (object): a reference to the table in which the column is used.
            index (int): the index of the column in the table (0=first)
            type (type): the type of the column data. May be str, int, or float.
            align ("L", "R", or "C"): determines text alignment: Left, Right or Center.
            width (int): width of column in characters. If not set, len(name) will be used.
            expand (bool): if True, and table is printed in "full" mode, column width will be expanded to width of longest entry.
            nvl (str): "None value" - a string value to use if a value in the column is None.
            evl (str): "Exception value" - a string value to use if a value in the column yields an exception while formatting.
            thousands (bool): for numeric values, print thousand separators.
            scale (int): for  columns with type=float, the number of decimal places to format with.
            plus (bool): for numeric types, will include sign even for +ve values.
            formatter (callable): for columns with type=str, a function convery objects to a string representation.
            highlighter (object of type Highlighter): a rule for highlighting values in this column.
        """
        self.name = name
        self.table = table
        self.index = index
        self.nvl = nvl
        self.evl = evl
        self.expand = expand
        self.type = type
        if width is None:
            width = len(name)
        if len(name) > width:
            width = len(name)
        if align is None:
            align = {None: "L", int: "R", float: "R", str: "L"}.get(type)
            if align is None:
                align = "L"
        self.aligner = StringFormatter(width, align, fill)
        if isinstance(formatter, ValueFormatter) or callable(formatter):
            self.formatter = formatter
        else:
            if type is float:
                self.formatter = FloatFormatter(width, scale, fill, plus, thousands)
            elif type is int:
                self.formatter = IntFormatter(width, fill, plus, thousands)
            else:
                self.formatter = str
        self.highlighter = highlighter

    @property
    def width(self):
        return self.aligner.width

    def __str__(self):
        return f"column name={self.name} width={self.aligner.width} formatter={self.formatter}"

    @property
    def aligned_name(self):
        """
        Get the name of the column in a string padded and aligned to the proper width for the column.
        """
        return self.aligner(self.name)

    def format(self, value, pad):
        """
        Convert a data value to a formatted string.
        """
        try:
            if value is None:
                formatted = self.nvl
            else:
                formatted = self.formatter(value)
        except:
            formatted = self.evl
        if not pad:
            return formatted
        else:
            return self.aligner(formatted)
