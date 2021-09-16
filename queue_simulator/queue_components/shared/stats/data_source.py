from dataclasses import dataclass
from typing import List

from queue_simulator.queue_components.shared.stats.item_stats import ItemStats


@dataclass
class DataSource:
    name: str
    item_stats: List[ItemStats]

    def serialize(self):
        s = []
        for stat in self.item_stats:
            s.append(stat.serialize())
        return {"name": self.name, "itemStats": s}

    def __hash__(self):
        return hash(str(self))
