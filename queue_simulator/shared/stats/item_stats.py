from typing import Set

from queue_simulator.shared.stats.stat import Stat


class ItemStats:
    name: str
    stats: Set[Stat]
