from typing import Dict, Any

from dynamic_system.models.dynamic_system import DynamicSystem
from simulation.base_simulator import BaseSimulator


class DiscreteTimeSimulator(BaseSimulator):
    _time: float

    def __init__(self, dynamic_system: DynamicSystem):
        super().__init__(dynamic_system)
        self._time = 0

    def computeNextState(self, inputs: Dict[str, Any] = None):
        """Compute the next state of the dynamic system

        :param inputs: Input for the dynamic system
        """
        self.computeOutput()
        self._time = self._time + 1
        self._dynamicSystem.stateTransition(inputs)
        self._isOutputUpToUpdate = False

    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        if not self._isOutputUpToUpdate:
            self._isOutputUpToUpdate = True
            self._dynamicSystem.getOutput()
