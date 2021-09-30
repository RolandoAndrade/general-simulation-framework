"""Scheduled Model
=================================
This module contains the definition of a scheduled model.
It has the definition of the ScheduledModel that allows is used by the scheduler to sort events by time.

Example:
    Creating a scheduled model::

        model  = ScheduledModel(model, Time(2))
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from gsf.core.debug.domain.debug import debug
from gsf.core.types import Time

if TYPE_CHECKING:
    from gsf.models.core.base_model import (
        BaseModel,
    )


@dataclass
class ScheduledModel:
    """Event scheduled

    It contains a model and the time where an autonomous event will be executed.

    Attributes:
        _model (BaseModel): Model to be scheduled.
        _time (Time): Time to be executed the event.
    """

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
        """Decreases the time of the scheduled model.

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
