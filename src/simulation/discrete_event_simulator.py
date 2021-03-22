from typing import Dict, Any

from dynamic_system.models.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from simulation.base_simulator import BaseSimulator


class DiscreteEventSimulator(BaseSimulator):
    _dynamicSystem: DiscreteEventDynamicSystem
    _lastEventTime: float

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
        super().__init__(dynamic_system)
        self._dynamicSystem = dynamic_system
        self._lastEventTime = 0
        self._isOutputUpToUpdate = False

    def _getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._dynamicSystem.getTimeOfNextEvent()

    def computeNextState(self, inputs: Dict[str, Any] = None, time: float = 0):
        """Compute the next state of the dynamic system

        :param inputs: Input for the dynamic system
        :param time: time of the event.
        """
        if time is self._getTimeOfNextEvent():  # Time to change the output
            self.computeOutput()
        self._lastEventTime = time
        self._dynamicSystem.stateTransition(inputs, time - self._lastEventTime)
        self._isOutputUpToUpdate = False

    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        if not self._isOutputUpToUpdate:
            self._isOutputUpToUpdate = True
            self._dynamicSystem.getOutput()
