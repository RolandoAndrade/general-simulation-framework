from abc import abstractmethod
from typing import Any


class UnitConversion:
    @abstractmethod
    def convert(self, value: Any, from_unit: str, to_unit: str):
        raise NotImplementedError
