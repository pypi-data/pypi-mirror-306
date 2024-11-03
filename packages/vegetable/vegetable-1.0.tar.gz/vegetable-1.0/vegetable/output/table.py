import re
from collections.abc import Iterable
from vegetable.output import TableFormatter


class TableFormat(TableFormatter):
    def __init__(self, gutter=" ┃ ", separator="━", header=True):
        self.gutter = gutter
        self.separator_char = separator
        self.show_header = header

    def __call__(self, table, limit=None):
        # check if any columns need expanding
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
        return self.gutter.join([x.aligned_name for x in table.columns])

    def separator(self, table):
        if self.separator_char is None or len(self.separator_char) == 0:
            return ""
        if re.search(r"[┃|#]", self.gutter):
            g = self.gutter.replace(" ", self.separator_char)
            if self.separator_char == "━":
                g = g.replace("┃", "╋")
        else:
            g = self.gutter
        return g.join([self.separator_char * x.aligner.width for x in table.columns])

    def row(self, table, row_values, row_idx):
        rec = [
            self.formatted_value(row_values.get(c.name), c, row_idx)
            for c in table.columns
        ]
        return self.gutter.join(rec)

    def formatted_value(self, value, column, row_idx, highlight=True):
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
