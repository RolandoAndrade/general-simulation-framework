from dataclasses import dataclass
from typing import List

from queue_simulator.shared.stats.stat import Stat


@dataclass
class ItemStats:
    name: str
    stats: List[Stat]

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
