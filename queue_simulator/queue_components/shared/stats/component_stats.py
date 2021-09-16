from dataclasses import dataclass
from typing import List

from queue_simulator.queue_components.shared.stats.data_source import DataSource


@dataclass
class ComponentStats:
    object_type: str
    name: str
    data_sources: List[DataSource]

    def serialize(self):
        s = []
        for stat in self.data_sources:
            s.append(stat.serialize())
        return {"objectType": self.object_type, "name": self.name, "dataSources": s}
