from __future__ import annotations
from typing import Dict, TypeVar, Any

V = TypeVar("V")


class BagOfValues(Dict[str, V]):
    """Container of multiple values"""

    def copy(self) -> BagOfValues:
        return BagOfValues(super(BagOfValues, self).copy())

    def addValue(self, name: str, value: Any) -> BagOfValues:
        """Add a value to the bag and return the bag"""
        self[name] = value
        return self
