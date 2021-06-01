from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    DynamicSystemOutput = Dict[str, Any]
    ReportResult = Any


class BaseReport:
    # TODO May outputs + time could be a dict?
    _outputs: List[DynamicSystemOutput]
    _times: List[float]

    def __init__(self):
        self._outputs = []
        self._times = []

    def addOutput(self, output: DynamicSystemOutput, time: float):
        self._outputs.append(output)
        self._times.append(time)

    @abstractmethod
    def getResults(self, output: DynamicSystemOutput, time: float) -> ReportResult:
        pass
