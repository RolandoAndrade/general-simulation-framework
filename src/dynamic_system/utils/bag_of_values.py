from __future__ import annotations
from typing import Dict, TypeVar

V = TypeVar("V")


class BagOfValues(Dict[str, V]):

    def copy(self) -> BagOfValues:
        return BagOfValues(super(BagOfValues, self).copy())
