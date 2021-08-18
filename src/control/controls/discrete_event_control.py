from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Dict
from control.core.thread_control import ThreadControl
from core.debug.domain.debug import debug
from core.types import Time
from models.models.discrete_event_model import ModelInput

if TYPE_CHECKING:
    from simulation.simulation_engines.discrete_event_simulation_engine import (
        DiscreteEventSimulationEngine,
    )


class DiscreteEventControl(ThreadControl):
    """Control that executes the discrete-event simulation in a new thread"""

    _simulator: DiscreteEventSimulationEngine
    """Overrides simulator type"""

    _time: Time
    """Current time of the simulation"""

    def __init__(self, simulator: DiscreteEventSimulationEngine):
        """
        Args:
            simulator (DiscreteEventSimulationEngine): Simulation engine to be
                executed.
        """
        ThreadControl.__init__(self, simulator)
        self._time = Time(0)
        self._is_paused = False

    def _execute(self, frequency: Time = 0, wait_time: Time = 0, stop_time: Time = 0):
        """Executes the simulation loop number of seconds.

        Args:
            frequency (Time): Frequency of the simulation computation.
            wait_time (Time): Delay execution for a given.
            stop_time (Time): Duration of the simulation.
        """
        while not self._is_paused:
            self._time = self._time + self._simulator.get_time_of_next_event()
            self._simulator.compute_next_state(time=self._time)
            sleep(wait_time)
            if 0 < stop_time < self._time:
                self._is_paused = True

    @debug("Simulation starts")
    def start(self,
              start_input: Dict[str, ModelInput] = None,
              frequency: Time = 0,
              stop_time: Time = 0,
              wait_time: Time = 0):
        """Starts the simulation

        Args:
            start_input: Input of the dynamic system.
            frequency (Time): Frequency of the simulation computation.
            stop_time (Time): Time of the simulation
            wait_time (Time): Delay execution for a given number of seconds.
        """
        self._is_paused = False
        self._simulator.compute_next_state(start_input)
        self._start_thread(frequency, wait_time, stop_time)

    @debug("Simulation paused")
    def pause(self):
        """Pauses the simulation"""
        self._is_paused = True

    @debug("Simulation ended")
    def stop(self):
        """Stops the simulation"""
        self._is_paused = True
        self._time = 0
