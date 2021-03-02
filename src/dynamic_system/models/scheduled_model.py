from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.models.model import Model


@dataclass
class ScheduledModel:
    _model: Model
    _time: float

    def getModel(self) -> Model:
        return self._model

    def getTime(self) -> float:
        return self._time

    def decreaseTime(self, time: float):
        return self._time - time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time
