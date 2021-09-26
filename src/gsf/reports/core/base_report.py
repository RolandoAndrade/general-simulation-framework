from __future__ import annotations

from abc import abstractmethod
from typing import Dict, Any, Set

from gsf.core.events import EventBus, DomainEvents, static_event_bus

DynamicSystemOutput = Dict[str, Any]
ReportResult = Any
Time = float


class BaseReport:
    """Base report generator"""

    _outputs: Dict[Time, DynamicSystemOutput]
    """Saved outputs"""

    _headers: Set[str]
    """Headers for the report table"""

    _event_bus: EventBus
    """Headers for the report table"""

    def __init__(self, event_bus: EventBus = None):
        self._outputs = {}
        self._headers = set()
        self._event_bus = event_bus or static_event_bus

    def add_output(self, output: DynamicSystemOutput, time: Time):
        for key in output:
            self._headers.add(key)
        self._outputs[time] = output
        self._event_bus.emit(DomainEvents.OUTPUT_SAVED, output)

    def generate_report(self) -> ReportResult:
        return self._get_results(self._headers, self._outputs)

    @abstractmethod
    def _get_results(
        self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
    ) -> ReportResult:
        raise NotImplementedError
