from __future__ import annotations
from typing import List, TYPE_CHECKING, Union, Dict, TypeVar

from dynamic_system.utils.value import Value

V = TypeVar("V")


class BagOfValues(Dict[str, V]):

    def __init__(self, values: Union[Value, List[Value]] = None):
        super().__init__()
        if not (values is None):
            self.add(values)

    def is_empty(self):
        return len(self.keys()) == 0

    def add(self, values: Union[Value, List[Value]]):
        if type(values) is list:
            for val in values:
                self[val.name] = val
        else:
            self[values.name] = values

    def __getitem__(self, item):
        r = super(BagOfValues, self).__getitem__(item)
        if r is not None:
            return r.value
        return r

    def __setitem__(self, key, value):
        if type(value) is Value:
            super(BagOfValues, self).__setitem__(key, value)
        else:
            super(BagOfValues, self).__setitem__(key, Value(key, value))

    def __str__(self):
        s = "BagOfValues "
        s += "{ "
        if len(self.keys()) > 0:
            for key in self:
                s += "'" + key + "': " + str(self[key]) + ", "
            s = s[:-2]
        s += " }"
        return s
