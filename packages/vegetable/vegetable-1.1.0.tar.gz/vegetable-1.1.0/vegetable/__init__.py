"""Tabular data formatter with column types/formatting options and other features."""

__version__ = "1.1.0"

import sys
import re
from vegetable.output.table import TableOutput
from vegetable.format import *
from vegetable.column import *


class Table:
    def __init__(self, output=TableOutput()):
        self.columns = list()
        self.data = list()
        self.output = output
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
        return self.output.header(self)

    def separator_str(self):
        return self.output.separator(self)

    def mast_head(self):
        return self.output.mast_head(self)

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
        return self.output.row(self, record, row_idx)

    def sort(self, key, reverse=False):
        column = [c for c in self.columns if c.name == key][0]
        nvl = {
            float: lambda x: 0. if x is None else x,
            int: lambda x: 0 if x is None else x,
        }.get(column.type)
        if nvl is None:
            nvl = lambda x: "" if x is None else x
        self.data.sort(key=lambda x: column.type(nvl(x.get(key))), reverse=reverse)

    def __str__(self):
        return self.output(self, limit=self.limit)
