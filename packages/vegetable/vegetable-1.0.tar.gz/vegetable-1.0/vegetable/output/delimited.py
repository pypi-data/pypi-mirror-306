from vegetable.output import TableFormatter


class DelimitedFormat(TableFormatter):
    def __init__(
        self, delimiter=",", header=True, strip=True, escape="escape", escape_char="\\"
    ):
        assert escape_char != delimiter
        self.delimiter = delimiter
        self.show_header = header
        self.strip = strip

        def escape_err(x):
            if delimiter in x:
                raise RuntimeError(f"value {x!r} contains delimiter {delimiter!r}")
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

    def __call__(self, table, limit):
        data = table.data if limit is None else table.data[:limit]
        s = ""
        if self.show_header:
            s += self.header(table)
        for row in data:
            s += "\n"
            rec = list()
            for c in table.columns:
                v = c.format(row.get(c.name), pad=not self.strip)
                if self.strip:
                    v = v.strip()
                v = self.escaper(v)
                rec.append(v)
            s += self.delimiter.join(rec)
        return s

    def header(self, table):
        return self.delimiter.join([x.name for x in table.columns])
