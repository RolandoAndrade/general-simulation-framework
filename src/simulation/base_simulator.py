from __future__ import annotations

from abc import abstractmethod

from dynamic_system.models.discrete_event_dynamic_system import DynamicSystem


class BaseSimulator:
    _dynamicSystem: DynamicSystem
    _isOutputUpToUpdate: bool

    def __init__(self, dynamic_system: DynamicSystem):
        self._dynamicSystem = dynamic_system
        self._isOutputUpToUpdate = False

    @abstractmethod
    def computeNextState(self, *args, **kwargs):
        """Compute the next state of the dynamic system."""
        pass

    @abstractmethod
    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        pass
