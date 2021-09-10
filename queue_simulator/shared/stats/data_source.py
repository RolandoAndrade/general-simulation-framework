from dataclasses import dataclass
from typing import Set

from queue_simulator.shared.stats.item_stats import ItemStats


@dataclass
class DataSource:
    name: str
    item_stats: Set[ItemStats]
