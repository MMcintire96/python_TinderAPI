import json
import pprint

#old version of the wrapper -- thanks to https://github.com/sharkbound

class MissingValue:
    __slots__ = ()
    VALUE = '<MissingValue>'

    def __getattr__(self, item):
        return self

    def __getitem__(self, item):
        return self

    def __iter__(self):
        yield from ()

    def __contains__(self, item):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return self.VALUE

    def __str__(self):
        return self.VALUE


MISSING_VALUE = MissingValue()


class JsonWrapper:
    def __init__(self, data, iter_keys_only=False):
        """
        :param data: the JSON data to wrap, can be a list, tuple, or dict
        :param iter_keys_only:
            sets the behavior when iterating over the wrapper when it contains a dict.
            False means that it will iterate over dict KEY/VALUE pairs,
                aka {'name': 'john doe'} would iterate as: ('name', 'john does');
            True means the it will only iterate over dict KEYS,
                aka {'name': 'john doe'} would iterate as: ('name')
        """
        self.iter_keys_only = iter_keys_only
        self._data = data

    def pretty(self):
        """
        returns a pretty printed version of the data this wrapper holds
        """
        return pprint.pformat(self._data)

    def _wrap(self, key, value, no_key=False):
        if value is not MISSING_VALUE and isinstance(value, (dict, list, tuple)):
            value = self.__class__(value, iter_keys_only=self.iter_keys_only)
            if not no_key:
                self._data[key] = value
        return value

    def _get_value(self, item):
        value = None
        if isinstance(self._data, dict):
            value = self._data.get(item)
        elif (isinstance(self._data, (list, tuple)) and
              isinstance(item, int) and
              -len(self._data) <= item < len(self._data)):
            value = self._data[item]
        return self._wrap(item, value if value is not None else MISSING_VALUE)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self._get_value(item)

    def __getitem__(self, item):
        return self._get_value(item)

    def __contains__(self, item):
        if isinstance(item, int) and isinstance(self._data, (list, tuple)):
            l = len(self._data)
            return -l <= item < l

        return item in self._data

    def __bool__(self):
        return bool(self._data)

    def __iter__(self):
        if isinstance(self._data, dict):
            yield from (self._data if self.iter_keys_only else self._data.items())
        elif isinstance(self._data, (list, tuple)):
            yield from (self._wrap(None, v, no_key=True) for v in self._data)
        else:
            try:
                yield from self._data
            except TypeError:
                yield from ()

    def __repr__(self):
        return f'<JsonWrapper {self._data.__class__.__name__}>'

    def __str__(self):
        if isinstance(self._data, dict):
            return pprint.pformat(tuple(self._data))

        return pprint.pformat(self._data)


def has_value(value):
    """
    verifies that a value is not MISSING_VALUE
    True return means it is not MISSING_VALUE
    False return means that the value was MISSING_VALUE
    :param value: the value to check if it is not MISSING_VALUE
    """
    return value is not MISSING_VALUE

# def test():
#     data = JsonWrapper({
#         'bio': r'¯\_(ツ)_/¯',
#         'photos': [
#             {
#                 'url': 'url here'
#             }
#         ]
#     })
#
#     assert data.photos[0].url == 'url here'
#     assert data.photos[100].url is MISSING_VALUE
#     assert data.bio == r'¯\_(ツ)_/¯'
#     assert data.missing is MISSING_VALUE
