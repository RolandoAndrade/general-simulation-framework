from dataclasses import dataclass
from typing import Set

from queue_simulator.shared.stats.data_source import DataSource


@dataclass
class ComponentStats:
    object_type: str
    name: str
    data_sources: Set[DataSource]
