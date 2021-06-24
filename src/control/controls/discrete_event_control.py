from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Dict
from control.core.thread_control import ThreadControl
from models.models.discrete_event_model import ModelInput

if TYPE_CHECKING:
    from simulation.simulation_engines.discrete_event_simulation_engine import DiscreteEventSimulationEngine


class DiscreteEventControl(ThreadControl):
    _simulator: DiscreteEventSimulationEngine
    _time: float

    def __init__(self, simulator: DiscreteEventSimulationEngine):
        ThreadControl.__init__(self, simulator)
        self._time = 0

    def _execute(self, frequency: float = 0, wait_time: float = 0):
        while not self._isPaused:
            self._time += self._simulator.getTimeOfNextEvent()
            self._simulator.computeNextState(time=self._time)
            sleep(wait_time)

    def start(self, start_input: Dict[str, ModelInput] = None, frequency: float = 0, wait_time: float = 0):
        self._isPaused = False
        self._simulator.computeNextState(start_input)
        self._thread.start()

    def pause(self):
        self._isPaused = True

    def stop(self):
        self._isPaused = True
        self._time = 0
