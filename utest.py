import json


# example below for usage

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


# converts JSON to a object that allows for safe . access
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


with open(r'data.txt')as f:
    data = json.load(f)

# usage:
# parse the data
data = json_to_object(data)

# get the attribute:
fail = data.photos[0]
valid = data.photos[0].processedFiles[0].url

# check if it does not exists
if fail is novalue:
    print('fail was a missing key')

#  check if it is not the global novalue value
#  novalue is what is returned on missing keys to prevent errors
#  it also allows safe chaining of . access, as it can be chained and keep returning itself
if valid is not novalue:
    print('non-missing data found:', valid)
