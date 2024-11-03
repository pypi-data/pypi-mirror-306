"""Tabular data formatter with column types/formatting options and other features."""

__version__ = "1.0"

import sys
import re
from vegetable.output.table import TableFormat
from vegetable.format import *


class TableColumn:
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
        precision=2,
        plus=False,
        formatter=None,
        highlighter=None,
    ):
        self.name = name
        self.table = table
        self.index = index
        self.nvl = nvl
        self.evl = evl
        self.expand = expand
        if width is None:
            width = len(name)
        if len(name) > width:
            width = len(name)
        if align is None:
            align = {None: "L", int: "R", float: "R", str: "L"}.get(type)
            if align is None:
                align = "L"
        self.aligner = PaddedStringFormatter(width, align, fill)
        if isinstance(formatter, ValueFormatter) or callable(formatter):
            self.formatter = formatter
        else:
            if type is float:
                self.formatter = FloatFormatter(width, precision, fill, plus, thousands)
            elif type is int:
                self.formatter = IntFormatter(width, fill, plus, thousands)
            else:
                self.formatter = str
        self.highlighter = highlighter

    def __str__(self):
        return f"column name={self.name} width={self.aligner.width} formatter={self.formatter}"

    @property
    def aligned_name(self):
        return self.aligner(self.name)

    def format(self, value, pad):
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


class Table:
    def __init__(self, formatter=TableFormat()):
        self.columns = list()
        self.data = list()
        self.formatter = formatter
        self.limit = None

    def column(self, name, **kwargs):
        index = len(self.columns)
        self.columns.append(TableColumn(name, self, len(self.columns), **kwargs))

    def row(self, record):
        """add a record to the table data"""
        if type(record) is dict:
            self.add_dict(record)
        elif type(record) is list:
            self.add_list(record)
        else:
            raise RuntimeError(
                f"don't know how to append a record of type {type(record)}"
            )

    def add_list(self, record):
        self.add_dict(self.list_to_dict(record))

    def add_dict(self, record):
        self.data.append(record)

    def list_to_dict(self, record):
        rec = dict()
        for i in range(len(record)):
            rec[self.columns[i].name] = record[i]
        return rec

    def header_str(self):
        return self.formatter.header(self)

    def separator_str(self):
        return self.formatter.separator(self)

    def row_str(self, record, append=False, row_idx=None):
        """format a record without adding it to the table"""
        if type(record) is dict:
            return self.row_str_dict(record, append, row_idx)
        elif type(record) is list:
            return self.row_str_list(record, append, row_idx)
        else:
            raise RuntimeError(
                f"don't know how to append a record of type {type(record)}"
            )

    def row_str_list(self, record, append, row_idx):
        return self.row_str_dict(self.list_to_dict(record), append, row_idx)

    def row_str_dict(self, record, append, row_idx):
        if append:
            self.add_dict(record)
        return self.formatter.row(self, record, row_idx)

    def sort(self, key, reverse=False):
        self.data.sort(key=lambda x: x[key], reverse=reverse)

    def __str__(self):
        return self.formatter(self, limit=self.limit)
