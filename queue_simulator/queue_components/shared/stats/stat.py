from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Stat:
    name: str
    value: Decimal

    def __hash__(self):
        return hash(str(self))

    def serialize(self):
        return {"name": self.name, "value": str(self.value)}
