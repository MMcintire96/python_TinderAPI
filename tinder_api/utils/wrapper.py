import json
#userman2

class NoValue:
    __slots__ = ()

    def __getattr__(self, item):
        return self

    def __getitem__(self, item):
        return self

    def __iter__(self):
        yield from ()

    def __bool__(self):
        return False

    def __str__(self):
        return '<NoValue>'


NOVALUE = NoValue()


class JsonWrapper:
    def __init__(self, data, iter_keys_only=False):
        self.iter_keys_only = iter_keys_only
        self._data = data

    def _wrap_if_needed(self, key, value, no_key=False):
        if value is not NOVALUE and isinstance(value, (dict, list, tuple)):
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
              item in range(-len(self._data), len(self._data))):
            value = self._data[item]
        return self._wrap_if_needed(item, value if value is not None else NOVALUE)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self._get_value(item)

    def __getitem__(self, item):
        return self._get_value(item)

    def __contains__(self, item):
        return item in self._data

    def __bool__(self):
        return bool(self.__dict__)

    def __iter__(self):
        if isinstance(self._data, dict):
            if self.iter_keys_only:
                yield from self._data
            else:
                yield from self._data.items()
        elif isinstance(self._data, (list, tuple)):
            yield from (self._wrap_if_needed(None, v, no_key=True) for v in self._data)
        else:
            try:
                yield from self._data
            except:
                yield from ()

    def __str__(self):
        if isinstance(self._data, (list, tuple)):
            return str(self._data)
        elif isinstance(self._data, dict):
            return str(tuple(self._data))
        return str(self._data)
