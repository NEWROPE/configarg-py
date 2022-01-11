from functools import reduce
import json

def read_json(path):
    with open(path) as f:
        return json.load(f)

class Config:
    def __init__(self, data):
        self.__data = data

    def __getitem__(self, path):
        return reduce(lambda data, key: data[key], path.split('.'), self.__data)

    def configure(self, parser, table):
        defaults = {}
        for src, dest in table.items():
            try:
                defaults[dest] = self[src]
            except KeyError:
                pass
        parser.set_defaults(**defaults)

    @classmethod
    def read(cls, path, load=read_json):
        return cls(load(path))

    @classmethod
    def read_from_option(cls, parser, field, args=None, **kwargs):
        args, _ = parser.parse_known_args(args=args)
        path = getattr(args, field)
        if path is None:
            return None
        return cls.read(path, **kwargs)
