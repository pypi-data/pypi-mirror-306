from vegetable.output import OutputFormatter


class DelimitedOutput(OutputFormatter):
    """
    Output Formatter with one record per line and fields separated by some delimiting string.
    """
    def __init__(
        self, delimiter=",", header=True, strip=True, escape="escape", escape_char="\\", record_separator=None
    ):
        """
        Create a DelimitedOutput formatter object.

        Args:
            delimiter (str): field delimiter.
            header (bool): if True, first row of output will contain column names.
            strip (bool): if True, remove whitespace from start and end of field values.
            escape (str): choose how to handle field values that contain the delimiter string.
            escape_char (str): a string used for some values of escape.
            record_separator (str): string to append at the end of each line. If None, is automatic according to OS.
        
        Valid values for escape: 
        * "escape": prefixes the delimiter with escape_char.
        * "replace": replaces delimiter with escape_char.
        * "delete": removes the delimiter from field values.
        * "error": raises a ValueError if delimiter is found in a field value.
        * "ignore": ignore it - let there is a delimiter in a field value.


        """
        super().__init__(record_separator)
        assert escape_char != delimiter
        self.delimiter = delimiter
        self.show_header = header
        self.strip = strip

        def escape_err(x):
            if delimiter in x:
                raise ValueError(f"value {x!r} contains delimiter {delimiter!r}")
            return x

        if escape == "escape":
            self.escaper = lambda x: x.replace(delimiter, escape_char + delimiter)
        elif escape == "replace":
            self.escaper = lambda x: x.replace(delimiter, escape_char)
        elif escape == "delete":
            self.escaper = lambda x: x.replace(delimiter, "")
        elif escape == "error":
            self.escaper = escape_err
        elif escape == "ignore":
            self.escaper = lambda x: x
        else:
            raise RuntimeError("unknown escape_method: {escape_method!r}")

    def __call__(self, table, limit=None):
        """
        Format a table and return the result as string.

        Args:
            table (Table): the table to format into a delimited string.
            limit (int): if +ve output only the first "limit" rows, if -ve, just the last "limit" rows.
        """
        if limit is None:
            data = table.data 
        elif limit > 0:
            data = table.data[:limit]
        else:
            data = table.data[limit:]
        s = ""
        if self.show_header:
            s += self.header(table)
        for row_idx in range(len(data)):
            if s != "":
                s += "\n"
            s += self.row(table, table.data[row_idx], row_idx)
        return s

    def header(self, table):
        """
        Return the header row as a string of delimited fields.

        Args:
            table (Table): a table for which to produce a header string.
        """
        if self.strip:
            return self.delimiter.join([c.name for c in table.columns])
        else:
            return self.delimiter.join([c.aligner(c.name) for c in table.columns])

    def separator(self, table):
        """
        For delimited output, this always returns "".

        Args:
            table (Table): a table for which to produce a separator string.
        """
        return ""

    def mast_head(self, table):
        return self.header(table)

    def row(self, table, row_values, row_idx):
        """
        Return a string representation of a single row of data, with all formats applied.

        Args:
            table (Table): a table for which to produce a row string.
            row_values (dict): a dict where keys are column names, and values are unformattred data items.
            row_idx (int): the row index. May be None if not known (line-by-line output mode).
        """
        rec = list()
        for c in table.columns:
            v = c.format(row_values.get(c.name), pad=not self.strip)
            if self.strip:
                v = v.strip()
            v = self.escaper(v)
            rec.append(v)
        return self.delimiter.join(rec)
