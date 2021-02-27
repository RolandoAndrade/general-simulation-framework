from plistlib import Dict
from typing import Any, List, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from dynamic_system.atomic_models.value import Value


class BagOfValues(Dict[str, Value]):
    def __init__(self, values: Union[Value, List[Value], None]):
        super().__init__()
        if not (values is None):
            self.add(values)

    def is_empty(self):
        return len(self.keys()) == 0

    def add(self, values: Union[Value, List[Value]]):
        if values is List:
            for val in values:
                self[val.name] = val
        else:
            self[values.name] = values
