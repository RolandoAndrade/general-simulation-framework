from dataclasses import dataclass
from typing import Set

from queue_simulator.shared.stats.stat import Stat

@dataclass
class ItemStats:
    name: str
    stats: Set[Stat]
