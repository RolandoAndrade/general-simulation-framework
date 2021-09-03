from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from core.config import FLOATING_POINT_DIGITS
from core.debug.domain.debug import debug
from core.types import Time

if TYPE_CHECKING:
    from models.core.base_model import (
        BaseModel,
    )


@dataclass
class ScheduledModel:
    """Event scheduled"""

    _model: BaseModel
    _time: Time

    @debug("Getting the model")
    def get_model(self) -> BaseModel:
        """Gets the scheduled model."""
        return self._model

    @debug("Getting the time")
    def get_time(self) -> Time:
        """Gets the time of the scheduled model."""
        return self._time

    @debug("Decreasing time")
    def decrease_time(self, time: Time) -> Time:
        """Decreases the time for the scheduled model.

        Args:
            time (int): Time variation.
        """
        self._time = max((self._time - time), Time(0))
        return self._time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time

    def __eq__(self, other: Union[ScheduledModel, BaseModel]):

        if isinstance(other, ScheduledModel):
            return self._model == other._model
        return self._model == other
