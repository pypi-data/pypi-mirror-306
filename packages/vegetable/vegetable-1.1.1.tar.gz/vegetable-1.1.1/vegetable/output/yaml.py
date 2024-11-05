import yaml

from vegetable.output import OutputFormatter


class YamlOutput(OutputFormatter):
    def __init__(self, rows=dict, **kwargs):
        assert rows in (dict, list)
        self.rows = rows
        self.json_kwargs = kwargs

    def __call__(self, table, limit):
        if limit is None or limit == 0:
            data = table.data 
        elif limit > 0:
            data = table.data[:limit]
        else:
            data = table.data[limit:]
        if self.rows is dict:
            return yaml.safe_dump(data, **self.json_kwargs)
        else:
            return yaml.safe_dump([list(x.values()) for x in data], **self.json_kwargs)
