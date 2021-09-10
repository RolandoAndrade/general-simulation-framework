from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Stat:
    name: str
    value: Decimal
