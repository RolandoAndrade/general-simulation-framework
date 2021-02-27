from typing import Any


class Value:
    name: str
    value: Any

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
