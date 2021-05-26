from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.models.model import Model


@dataclass
class ScheduledModel:
    """Event scheduled"""
    _model: Model
    _time: float

    def getModel(self) -> Model:
        """Gets the scheduled model."""
        return self._model

    def getTime(self) -> float:
        """Gets the time of the scheduled model."""
        return self._time

    def decreaseTime(self, time: float) -> float:
        """Decreases the time for the scheduled model.

        :param time: Time variation.
        """
        self._time = self._time - time
        return self._time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time

    def __eq__(self, other: ScheduledModel):
        return self._model == other._model
