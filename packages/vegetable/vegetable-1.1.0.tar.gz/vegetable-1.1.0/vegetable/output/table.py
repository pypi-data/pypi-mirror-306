import re
from collections.abc import Iterable
from vegetable.output import OutputFormatter


class TableOutput(OutputFormatter):
    """
    Output Formatter with fixed with columns in terms of number of characters for printing to a terminal.
    """

    # TODO: have ASCII / UTF modes with different default gutter and separators.
    def __init__(self, gutter=" ┃ ", separator="━", header=True, record_separator=None):
        """
        Create a TableOutput formatter object.

        Args:
            gutter (str): a string to print between columns.
            separatpr (str): character to be repeated to create the separator line.
            header (bool): if True, include the header line in the output.
            record_separator (str): string to append at the end of each line. If None, is automatic according to OS.
        """
        super().__init__(record_separator=record_separator)
        self.gutter = gutter
        self.separator_char = separator
        self.show_header = header

    def __call__(self, table, limit=None):
        """
        Format a table and return the result as string.

        Args:
            table (Table): the table to format into a delimited string.
            limit (int): if +ve output only the first "limit" rows, if -ve, just the last "limit" rows.

        Note: If any data values mean the column widths exceed the set width of the column, and 
        the expand property is set for the column, the column will be expanded to the width of the\
        longest data item.
        """
        if len(table.data) > 0:
            for column in [x for x in table.columns if x.expand]:
                max_width = max(
                    [
                        len(
                            self.formatted_value(
                                row_values.get(column.name),
                                column,
                                None,
                                highlight=False,
                            )
                        )
                        for row_values in table.data
                    ]
                )
                if max_width > column.aligner.width:
                    # log.debug(
                    #     f"expanding column {column.name!r} from {column.aligner.width} to {max_width}"
                    # )
                    column.aligner.width = max_width
        s = ""
        if self.header:
            s += self.header(table)
            sep = self.separator(table)
            if len(sep) > 0:
                s += "\n"
                s += sep
        for row_idx in range(len(table.data)):
            if limit and row_idx >= limit:
                break
            if s != "":
                s += "\n"
            s += self.row(table, table.data[row_idx], row_idx)
        return s

    def header(self, table):
        """
        Return the header row as a string with column name separation by gutters.

        Args:
            table (Table): a table for which to produce a header string.
        """
        return self.gutter.join([x.aligned_name for x in table.columns])

    def separator(self, table):
        """
        Return the separator string separated by gutters.

        Args:
            table (Table): a table for which to produce a separator string.
        """
        if self.separator_char is None or len(self.separator_char) == 0:
            return ""
        if re.search(r"[┃|#]", self.gutter):
            g = self.gutter.replace(" ", self.separator_char)
            if self.separator_char == "━":
                g = g.replace("┃", "╋")
        else:
            g = self.gutter
        return g.join([self.separator_char * x.aligner.width for x in table.columns])

    def mast_head(self, table):
        """
        Return a string containing the header() and separator() lines joined with record_separator.

        Args:
            table (Table): a table for which to produce a the mast_head string.
        """
        result = self.header(table)
        if len(result) > 0:
            result += self.record_separator
        result += self.separator(table)
        return result

    def row(self, table, row_values, row_idx):
        """
        Return a string representation of a single row of data, with all format and highlights applied.

        Args:
            table (Table): a table for which to produce a row string.
            row_values (dict): a dict where keys are column names, and values are unformattred data items.
            row_idx (int): the row index. May be None if not known (line-by-line output mode).
        """
        rec = [
            self.formatted_value(row_values.get(c.name), c, row_idx)
            for c in table.columns
        ]
        return self.gutter.join(rec)

    def formatted_value(self, value, column, row_idx, highlight=True):
        """
        Return the formatted value of a single data item.

        Args:
            value (str, float, or int): the raw data value to format.
            column (TableColumn): the column in which the value is found.
            row_idx (int): the row index. May be None if not known (line-by-line output mode).
            highlight (bool)L if True, apply highlights.
        """
        string = column.format(value, pad=True)
        if not highlight or column.highlighter is None:
            return string
        else:
            if callable(column.highlighter):
                return column.highlighter(value, string, column, row_idx)
            if isinstance(column.highlighter, Iterable):
                for h in column.highlighter:
                    string = h(value, string, column, row_idx)
                return string
