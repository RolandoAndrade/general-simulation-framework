from __future__ import annotations
from abc import ABC
from random import random
from typing import TYPE_CHECKING, Dict, Set, cast, Any

from core.debug.domain.debug import debug

from dynamic_system.core.base_dynamic_sytem import (
    BaseDynamicSystem,
    DynamicSystemOutput,
)
from dynamic_system.future_event_list.scheduler import Scheduler
from models.core.path import Path

if TYPE_CHECKING:
    from models.models.discrete_event_model import (
        DiscreteEventModel,
        ModelInput,
    )

    DynamicSystemModels = Set[DiscreteEventModel]
    DynamicSystemPaths = Dict[DiscreteEventModel, Set[Path]]
    from core.types import DynamicSystemInput, Time


class DiscreteEventDynamicSystem(ABC, BaseDynamicSystem):
    """Dynamic system for discrete-event models"""

    _models: DynamicSystemModels
    """Models of the dynamic system."""

    _paths: DynamicSystemPaths
    """Paths of the dynamic system. Dict[Origin, Set[Output]]"""

    _outputs: DynamicSystemOutput
    """Output of the models"""

    _scheduler: Scheduler
    """Scheduler of events"""

    def __init__(self, scheduler: Scheduler = Scheduler()):
        """
        Args:
            scheduler (Scheduler): Future event list manager
        """
        super(BaseDynamicSystem, self).__init__()
        self._paths = {}
        self._outputs = {}
        self._scheduler = scheduler

    @debug("Scheduling model")
    def schedule(self, model: DiscreteEventModel, time: Time):
        """Schedules an event at the specified time

        Args:
            model (DiscreteEventModel): Model with an autonomous event scheduled
            time (Time): Time to execute event
        """
        self._scheduler.schedule(model, time)

    @debug("Retrieving next models")
    def get_next_models(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event"""
        return self._scheduler.get_next_models()

    @debug("Getting time of next event")
    def get_time_of_next_events(self) -> Time:
        """Get time of the next event"""
        return self._scheduler.get_time_of_next_event()

    @debug("Getting output of the dynamic system")
    def get_output(self) -> DynamicSystemOutput:
        """Gets the output of all the models in the dynamic system. Changes only
        the model that changes at time t
        """
        pass

    @debug("Executing state transition")
    def state_transition(
            self, input_models_values: DynamicSystemInput = None, event_time: Time = 0
    ):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        Args:
            input_models_values (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            event_time (Time): Time of the event.
        """
        pass

