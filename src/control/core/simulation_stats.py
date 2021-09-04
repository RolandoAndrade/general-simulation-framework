from dataclasses import dataclass

from core.types import Time


@dataclass
class SimulationStats:
    time: Time
    stop_time: Time
    frequency: Time
    is_paused: bool
