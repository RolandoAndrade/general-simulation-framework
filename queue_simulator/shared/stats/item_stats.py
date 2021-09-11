from dataclasses import dataclass
from typing import Set

from queue_simulator.shared.stats.stat import Stat


@dataclass
class ItemStats:
    name: str
    stats: Set[Stat]

    def serialize(self):
        s = []
        for stat in self.stats:
            s.append(stat.serialize())
        return {
            'name': self.name,
            'stats': s
        }

    def __hash__(self):
        return hash(str(self))
