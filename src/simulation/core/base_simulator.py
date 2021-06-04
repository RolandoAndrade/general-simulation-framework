from __future__ import annotations

from abc import abstractmethod

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from reports.core.base_report import BaseReport


class BaseSimulator:
    _dynamicSystem: DiscreteEventDynamicSystem
    _isOutputUpToUpdate: bool
    _reportGenerator: BaseReport

    def __init__(
        self, dynamic_system: DiscreteEventDynamicSystem, reportGenerator: BaseReport
    ):
        self._dynamicSystem = dynamic_system
        self._isOutputUpToUpdate = False
        self._reportGenerator = reportGenerator

    @abstractmethod
    def computeNextState(self, *args, **kwargs):
        """Compute the next state of the dynamic system."""
        raise NotImplementedError

    @abstractmethod
    def computeOutput(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        raise NotImplementedError
