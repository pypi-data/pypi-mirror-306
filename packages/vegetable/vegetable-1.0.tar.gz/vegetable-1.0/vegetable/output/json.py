import json as json
from vegetable.output import TableFormatter


class JsonFormat(TableFormatter):
    def __init__(self, rows=dict, **kwargs):
        assert rows in (dict, list)
        self.rows = rows
        self.json_kwargs = kwargs

    def __call__(self, table, limit):
        data = table.data if limit is None else table.data[:limit]
        if self.rows is dict:
            return json.dumps(data, **self.json_kwargs)
        else:
            return json.dumps([list(x.values()) for x in data], **self.json_kwargs)

    def header(self, table):
        return self.delimiter.join([x.name for x in table.columns])
