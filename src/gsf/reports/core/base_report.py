"""Base Report
====================
This module contains the abstract definition of a simulation report.
It has the definition of BaseReport, that should be extended,
implementing its abstract methods.

Example:
    Creating a concrete report::

        class NewReport(BaseReport):

            def _get_results(
                self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
            ) -> ReportResult:
                print(outputs)

    Saving an output::

        report.add_output({model: model_output}, 1)

    Generating report::

        report.generate_report()
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Dict, Any, Set

from gsf.core.events import EventBus, DomainEvents, static_event_bus

DynamicSystemOutput = Dict[str, Any]
ReportResult = Any
Time = float


class BaseReport:
    """Base report generator

    Attributes:
        _outputs (Dict[Time, DynamicSystemOutput]): Saved outputs.
        _headers (Set[str]): Headers for the report table.
        _event_bus (EventBus): Event bus of the module.
    """

    _outputs: Dict[Time, DynamicSystemOutput]
    """Saved outputs"""

    _headers: Set[str]
    """Headers for the report table"""

    _event_bus: EventBus
    """Event bus of the module."""

    def __init__(self, event_bus: EventBus = None):
        """
        Args:
            event_bus (EventBus): Event bus of the module.
        """
        self._outputs = {}
        self._headers = set()
        self._event_bus = event_bus or static_event_bus

    def add_output(self, output: DynamicSystemOutput, time: Time):
        """Saves an output into the report registry.

        Args:
            output (DynamicSystemOutput): Report to save.
            time (Time): Time of the given output.
        """
        for key in output:
            self._headers.add(key)
        self._outputs[time] = output
        self._event_bus.emit(DomainEvents.OUTPUT_SAVED, output)

    def generate_report(self) -> ReportResult:
        """Returns the generated report from the saved outputs."""
        return self._get_results(self._headers, self._outputs)

    @abstractmethod
    def _get_results(
        self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
    ) -> ReportResult:
        """Generates the report."""
        raise NotImplementedError
