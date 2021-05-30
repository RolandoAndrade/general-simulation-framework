from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.discrete_events.models.discrete_event_model import (
        DiscreteEventModel,
    )


@dataclass
class ScheduledModel:
    """Event scheduled"""

    _model: DiscreteEventModel
    _time: float

    def getModel(self) -> DiscreteEventModel:
        """Gets the scheduled model."""
        return self._model

    def getTime(self) -> float:
        """Gets the time of the scheduled model."""
        return self._time

    def decreaseTime(self, time: float) -> float:
        """Decreases the time for the scheduled model.

        Args:
            time (float): Time variation.
        """
        self._time = self._time - time
        return self._time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time

    def __eq__(self, other: ScheduledModel):
        return self._model == other._model
