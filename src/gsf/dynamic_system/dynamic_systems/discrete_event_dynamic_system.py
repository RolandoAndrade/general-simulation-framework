from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Dict, Set, cast, Any

from gsf.core.debug.domain.debug import debug
from gsf.core.events import EventBus

from gsf.dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from gsf.dynamic_system.future_event_list.scheduler import Scheduler
from gsf.models.core.path import Path
import numpy as np

if TYPE_CHECKING:
    from gsf.models.models.discrete_event_model import (
        DiscreteEventModel,
        ModelInput,
    )

    DynamicSystemModels = Set[DiscreteEventModel]
    DynamicSystemPaths = Dict[DiscreteEventModel, Set[Path]]
    DynamicSystemOutput = Dict[DiscreteEventModel, Any]
    from gsf.core.types import DynamicSystemInput, Time


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

    def __init__(self, scheduler: Scheduler = None, event_bus: EventBus = None):
        """
        Args:
            scheduler (Scheduler): Future event list manager
            event_bus (EventBus): Event bus for domain events.
        """
        BaseDynamicSystem.__init__(self, event_bus)
        self._outputs = {}
        self._scheduler = scheduler or Scheduler()

    @debug("Scheduling model")
    def schedule(self, model: DiscreteEventModel, time: Time):
        """Schedules an event at the specified time

        Args:
            model (DiscreteEventModel): Model with an autonomous event scheduled
            time (Time): Time to execute event
        """
        self._scheduler.schedule(model, time)

    @debug("Scheduling model")
    def unschedule(self, model: DiscreteEventModel):
        """Undo a scheduled event

        Args:
            model (DiscreteEventModel): Model with an autonomous event scheduled
        """
        self._scheduler.unschedule(model)

    def remove(self, model: DiscreteEventModel):
        """Removes a model of the dynamic system.

        Args:
            model (DiscreteEventModel): Model to be removed.
        """
        super(DiscreteEventDynamicSystem, self).remove(model)
        self.unschedule(model)

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
        models = self.get_next_models()
        self._outputs = {}
        for model in models:
            output = model.get_output()
            self._outputs[model] = output
        return self._outputs

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
        self._scheduler.update_time(event_time)

        # execute external / confluent transition
        models_already_executed = self._execute_external(
            input_models_values, event_time
        )
        # execute autonomous / external by internal output / confluent transition
        autonomous_models = self._execute_autonomous(
            models_already_executed, event_time
        )

    def _execute_external(
        self, input_model_values: DynamicSystemInput, event_time: Time
    ) -> Set[DiscreteEventModel]:
        """Executes external transition for the given input.

        Args:
            input_model_values (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            event_time (Time): Time of the event.
        """
        input_models = set()
        if input_model_values is not None:
            for model in input_model_values:
                model.state_transition({model: input_model_values[model]}, event_time)
                input_models.add(model)
        return cast(Any, input_models)

    def _execute_autonomous(
        self, models_already_executed: Set[DiscreteEventModel], event_time: Time
    ) -> Set[DiscreteEventModel]:
        """Executes autonomous transition for the given input and external
        events of the affected models.

        Args:
            event_time (Time): Time of the event.
            models_already_executed: Models that its state was changed by the external
                transition and must be ignored.
        """
        all_autonomous_models = set()

        # there are models expecting an autonomous event
        if self.get_time_of_next_events() <= 0:
            # get the models that will execute an autonomous event
            all_autonomous_models = self._scheduler.pop_next_models()

            # ignore models that executed an external event
            autonomous_models = all_autonomous_models.difference(
                models_already_executed
            )

            # get models that were affected by an output
            (
                affected_models,
                inputs_of_affected_models,
            ) = self._get_affected_models_and_its_inputs()

            # models that were affected and will execute an autonomous event.
            confluent_models = autonomous_models.intersection(affected_models)

            # models that will execute only and autonomous event
            autonomous_models = autonomous_models.difference(affected_models)

            # models that were affected but will not execute an autonomous events.
            external_models = affected_models.difference(confluent_models)

            for model in confluent_models:
                # execute confluent state transition
                model.state_transition(inputs_of_affected_models[model])

            for model in autonomous_models:
                # execute autonomous state transition
                model.state_transition()

            for model in external_models:
                # execute external state transition
                model.state_transition(inputs_of_affected_models[model], event_time)

        return all_autonomous_models

    def _get_affected_models_and_its_inputs(
        self,
    ) -> (Set[DiscreteEventModel], Dict[DiscreteEventModel, ModelInput]):
        """Gets models that were affected by an output"""
        affected_models = set()
        insert_input: Dict[DiscreteEventModel, ModelInput] = {}
        for emitter_model in self._outputs:
            emitter_model: DiscreteEventModel = emitter_model
            # get the correct paths
            paths = self._get_effective_paths(emitter_model)
            for path in paths:
                affected_model: DiscreteEventModel = cast(
                    Any, path.get_destination_model()
                )
                affected_models.add(affected_model)
                if affected_model in insert_input:
                    insert_input[affected_model][
                        emitter_model.get_id()
                    ] = self._outputs[emitter_model]
                else:
                    insert_input[affected_model] = {
                        emitter_model.get_id(): self._outputs[emitter_model]
                    }
        return affected_models, insert_input

    def _get_effective_paths(self, emitter_model: DiscreteEventModel) -> Set[Path]:
        """Gets the correct paths for an output"""
        if emitter_model in self._paths:
            # check for full probability paths.
            ones = [
                path for path in self._paths[emitter_model] if path.get_weight() == 1
            ]
            if len(ones) > 0:
                return set(ones)
            # there are not multiple paths, so it has to select one.
            weights = []
            effective_path = []
            for path in self._paths[emitter_model]:
                weights.append(path.get_weight())
                effective_path.append(path)
            choice = np.random.choice(len(weights), p=weights)
            return {effective_path[choice]}
        return set()
