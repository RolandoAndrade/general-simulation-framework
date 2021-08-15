from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Dict
from control.core.thread_control import ThreadControl
from core.config import FLOATING_POINT_DIGITS
from core.debug.domain.debug import debug
from models.models.discrete_event_model import ModelInput

if TYPE_CHECKING:
    from simulation.simulation_engines.discrete_event_simulation_engine import (
        DiscreteEventSimulationEngine,
    )


class DiscreteEventControl(ThreadControl):
    """Control that executes the discrete-event simulation in a new thread"""

    _simulator: DiscreteEventSimulationEngine
    """Overrides simulator type"""

    _time: float
    """Current time of the simulation"""

    def __init__(self, simulator: DiscreteEventSimulationEngine):
        ThreadControl.__init__(self, simulator)
        self._time = 0
        self._is_paused = False

    def _execute(self, frequency: float = 0, wait_time: float = 0, stop_time: float = 0):
        while not self._is_paused:
            self._time = round(self._time + self._simulator.get_time_of_next_event(), FLOATING_POINT_DIGITS)
            self._simulator.compute_next_state(time=self._time)
            sleep(wait_time)
            if 0 < stop_time < self._time:
                self._is_paused = True

    @debug("Simulation starts")
    def start(self,
              start_input: Dict[str, ModelInput] = None,
              frequency: float = 0,
              stop_time: float = 0,
              wait_time: float = 0):
        self._is_paused = False
        self._simulator.compute_next_state(start_input)
        self._start_thread(frequency, wait_time, stop_time)

    @debug("Simulation paused")
    def pause(self):
        self._is_paused = True

    @debug("Simulation ended")
    def stop(self):
        self._is_paused = True
        self._time = 0
