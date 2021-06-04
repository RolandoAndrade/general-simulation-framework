from __future__ import annotations

from abc import abstractmethod
from typing import Dict, Any, Set

DynamicSystemOutput = Dict[str, Any]
ReportResult = Any
Time = float


class BaseReport:
    _outputs: Dict[Time, DynamicSystemOutput]
    _headers: Set[str]

    def __init__(self):
        self._outputs = {}
        self._headers = set()

    def addOutput(self, output: DynamicSystemOutput, time: float):
        for key in output:
            self._headers.add(key)
        self._outputs[time] = output

    def generateReport(self) -> ReportResult:
        return self._getResults(self._headers, self._outputs)

    @abstractmethod
    def _getResults(
        self, headers: Set[str], outputs: Dict[Time, DynamicSystemOutput]
    ) -> ReportResult:
        raise NotImplementedError
