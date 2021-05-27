from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from simulation.base_simulator import BaseSimulator

if TYPE_CHECKING:
    from dynamic_system.models.model import ModelInput
    from dynamic_system.models.discrete_event_dynamic_system import DynamicSystem


class SimulationEngine(BaseSimulator):
    """Simulation engine for discrete-event simulation"""
    _dynamicSystem: DynamicSystem
    _lastEventTime: float

    def __init__(self, dynamic_system: DynamicSystem):
        """
        Args:
            dynamic_system (DynamicSystem):
        """
        super().__init__(dynamic_system)
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
        if time - self._lastEventTime is self._getTimeOfNextEvent():  # Time to change the output
            self.computeOutput()
        self._dynamicSystem.stateTransition(inputs, time - self._lastEventTime)
        self._lastEventTime = time
        self._isOutputUpToUpdate = False

    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        if not self._isOutputUpToUpdate:
            self._isOutputUpToUpdate = True
            self._dynamicSystem.getOutput()
