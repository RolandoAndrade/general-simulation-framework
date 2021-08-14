from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from reports.core.base_report import BaseReport
from simulation.core.base_simulator import BaseSimulator

if TYPE_CHECKING:
    from models.models.discrete_event_model import ModelInput
    from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
        DiscreteEventDynamicSystem,
    )


class DiscreteEventSimulationEngine(BaseSimulator):
    """Simulation engine for discrete-event simulation"""

    _dynamic_system: DiscreteEventDynamicSystem
    _lastEventTime: float

    def __init__(
        self, dynamic_system: DiscreteEventDynamicSystem, reportGenerator: BaseReport
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem):
        """
        super().__init__(dynamic_system, reportGenerator)
        self._dynamicSystem = dynamic_system
        self._lastEventTime = 0
        self._isOutputUpToUpdate = False

    def getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._dynamicSystem.get_time_of_next_events()

    def compute_next_state(self, inputs: Dict[str, ModelInput] = None, time: float = 0):
        """Compute the next state of the dynamic system

        Args:
            inputs: Input for the dynamic system
            time (float): time of the event.
        """
        if (
            time - self._lastEventTime is self.getTimeOfNextEvent()
        ):  # Time to change the output
            out = self.compute_output()
            if out:
                self._report_generator.add_output(out, time)
        self._dynamicSystem.state_transition(inputs, time - self._lastEventTime)
        self._lastEventTime = time
        self._isOutputUpToUpdate = False

    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        if not self._isOutputUpToUpdate:
            self._isOutputUpToUpdate = True
            return self._dynamicSystem.get_output()
        return None
