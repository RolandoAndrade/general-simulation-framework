"""Simulation Stats
==============
This module contains the definition of the SimulationStats dataclass.

Example:
    Creating a simulation stat::

        stat = SimulationStats(time=1, stop_time=3, frequency=Time(0.5), False)

"""

from dataclasses import dataclass

from gsf.core.types import Time


@dataclass
class SimulationStats:
    """
    Attributes:
        time (Time): current time of the simulation.
        stop_time (Time): time when the simulation will stop.
        frequency (Time): frequency of the simulation step.
        is_paused (bool): bool that indicates if the simulation is running.
    """

    time: Time
    stop_time: Time
    frequency: Time
    is_paused: bool
