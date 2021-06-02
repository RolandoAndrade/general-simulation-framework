from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from reports.core.base_report import BaseReport
from simulation.core.base_simulator import BaseSimulator

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_model import ModelInput
    from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
        DiscreteEventDynamicSystem,
    )


class DiscreteEventSimulationEngine(BaseSimulator):
    """Simulation engine for discrete-event simulation"""

    _dynamicSystem: DiscreteEventDynamicSystem
    _lastEventTime: float

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, reportGenerator: BaseReport):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem):
        """
        super().__init__(dynamic_system, reportGenerator)
        self._dynamicSystem = dynamic_system
        self._lastEventTime = 0
        self._isOutputUpToUpdate = False

    def _getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._dynamicSystem.getTimeOfNextEvent()

    def computeNextState(self, inputs: Dict[str, ModelInput] = None, time: float = 0):
        """Compute the next state of the dynamic system

        Args:
            inputs: Input for the dynamic system
            time (float): time of the event.
        """
        print(time - self._lastEventTime)
        print(self._getTimeOfNextEvent())
        if (
                time - self._lastEventTime is self._getTimeOfNextEvent()
        ):  # Time to change the output
            out = self.computeOutput()
            if out:
                self._reportGenerator.addOutput(out, time)
        self._dynamicSystem.stateTransition(inputs, time - self._lastEventTime)
        self._lastEventTime = time
        self._isOutputUpToUpdate = False

    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        if not self._isOutputUpToUpdate:
            self._isOutputUpToUpdate = True
            return self._dynamicSystem.getOutput()
        return None
