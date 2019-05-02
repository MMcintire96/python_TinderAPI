import json

class NoValue:
    __slots__ = tuple()

    def __getattr__(self, item):
        return self

    def __bool__(self):
        return False

    def __str__(self):
        return '<NoValue>'

novalue = NoValue()

class JsonToObjectWrapper:
    def __str__(self):
        return str(self.__dict__.keys())

    def __getattr__(self, item):
        return self.__dict__.get(item) or novalue

    def __bool__(self):
        return bool(self.__dict__)


def json_to_object(value):
    if isinstance(value, dict) or hasattr(value, '__dict__'):
        obj = JsonToObjectWrapper()
        items = getattr(value, '__dict__', value).items()
        for k, v in items:
            setattr(obj, k, json_to_object(v))
        return obj
    elif isinstance(value, list):
        return list(map(json_to_object, value))
    elif isinstance(value, tuple):
        return tuple(map(json_to_object, value))
    return value
