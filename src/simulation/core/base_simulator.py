from __future__ import annotations

from abc import abstractmethod

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from reports.core.base_report import BaseReport


class BaseSimulator:
    _dynamic_system: DiscreteEventDynamicSystem
    _is_output_up_to_update: bool
    _report_generator: BaseReport

    def __init__(
        self, dynamic_system: DiscreteEventDynamicSystem, reportGenerator: BaseReport
    ):
        self._dynamic_system = dynamic_system
        self._is_output_up_to_update = False
        self._report_generator = reportGenerator

    @abstractmethod
    def compute_next_state(self, *args, **kwargs):
        """Compute the next state of the dynamic system."""
        raise NotImplementedError

    @abstractmethod
    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        raise NotImplementedError
