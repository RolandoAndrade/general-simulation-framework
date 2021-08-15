from __future__ import annotations

from abc import abstractmethod


from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from reports.core.base_report import BaseReport


class BaseSimulator:
    _dynamic_system: BaseDynamicSystem
    _is_output_up_to_update: bool
    _report_generator: BaseReport

    def __init__(
        self, dynamic_system: BaseDynamicSystem, base_generator: BaseReport
    ):
        self._dynamic_system = dynamic_system
        self._is_output_up_to_update = False
        self._report_generator = base_generator

    @abstractmethod
    def compute_next_state(self, *args, **kwargs):
        """Compute the next state of the dynamic system."""
        raise NotImplementedError

    @abstractmethod
    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed yet"""
        raise NotImplementedError
