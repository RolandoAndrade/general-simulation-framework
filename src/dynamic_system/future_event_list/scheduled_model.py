from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.config import FLOATING_POINT_DIGITS
from core.debug.domain.debug import debug

if TYPE_CHECKING:
    from models.core.base_model import (
        BaseModel,
    )


@dataclass
class ScheduledModel:
    """Event scheduled"""

    _model: BaseModel
    _time: float

    @debug("Getting the model")
    def getModel(self) -> BaseModel:
        """Gets the scheduled model."""
        return self._model

    @debug("Getting the time")
    def getTime(self) -> float:
        """Gets the time of the scheduled model."""
        return self._time

    @debug("Decreasing time")
    def decreaseTime(self, time: float) -> float:
        """Decreases the time for the scheduled model.

        Args:
            time (float): Time variation.
        """
        self._time = round(self._time - time, FLOATING_POINT_DIGITS)
        return self._time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time

    def __eq__(self, other: ScheduledModel):
        return self._model == other._model
