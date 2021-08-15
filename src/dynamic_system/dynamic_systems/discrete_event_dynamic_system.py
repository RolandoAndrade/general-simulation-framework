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

    DynamicSystemModels = Dict[str, DiscreteEventModel]
    from core.types import DynamicSystemInput


class DiscreteEventDynamicSystem(BaseDynamicSystem, ABC):
    """Dynamic system for discrete-event models"""

    _models: DynamicSystemModels
    """Models of the dynamic system"""

    _outputs: DynamicSystemOutput
    """Output of the models"""

    _scheduler: Scheduler
    """Scheduler of events"""

    def __init__(self, scheduler: Scheduler = Scheduler()):
        """
        Args:
            scheduler (Scheduler): Future event list manager
        """
        super().__init__()
        self._scheduler = scheduler

    @debug("Scheduling model")
    def schedule(self, model: DiscreteEventModel, time: float):
        """Schedules an event at the specified time

        Args:
            model (DiscreteEventModel): Model with an autonomous event scheduled
            time (float): Time to execute event
        """
        self._scheduler.schedule(model, time)

    @debug("Retrieving next models")
    def get_next_models(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event"""
        return self._scheduler.get_next_models()

    @debug("Getting time of next event")
    def get_time_of_next_events(self) -> int:
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
            self._outputs[model.get_id()] = output
        return self._outputs

    @debug("Executing state transition")
    def state_transition(
            self, input_models_values: DynamicSystemInput = None, event_time: float = 0
    ):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        Args:
            input_models_values (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            event_time (float): Time of the event.
        """
        # subtract time
        self._scheduler.update_time(event_time)

        input_models = self._execute_external(input_models_values, event_time)

        autonomous_models = self._execute_autonomous(event_time, input_models)

    def _execute_autonomous(
            self, event_time: float, input_models: Set[DiscreteEventModel]
    ) -> Set[DiscreteEventModel]:
        """Executes autonomous transition for the given input and external
        events of the affected models.

        Args:
            event_time (float): Time of the event.
            input_models: Models that its state was changed by the external
                transition.
        """
        all_autonomous_models = set()
        # there are models expecting an autonomous event
        if self.get_time_of_next_events() == 0:
            # get the models that will execute an autonomous event
            all_autonomous_models = self._scheduler.pop_next_models()

            # remove models that executed an external event
            autonomous_models: Set[DiscreteEventModel] = all_autonomous_models.difference(input_models)

            affected_models, affected_models_inputs = self._get_affected_models_inputs(
                all_autonomous_models, input_models
            )

            # remove from autonomous models, models that will execute a confluent transition
            confluent_models = autonomous_models.intersection(affected_models)
            autonomous_models = autonomous_models.difference(affected_models)
            external_models = affected_models.difference(confluent_models)

            # execute autonomous event
            for model in autonomous_models:
                model.state_transition(None, event_time)

            # execute confluent event
            for model in confluent_models:
                model.state_transition(affected_models_inputs[model.get_id()], model.get_time())

            # execute external event
            for model in external_models:
                model.state_transition(affected_models_inputs[model.get_id()], event_time)

        return all_autonomous_models

    def _select_outputs_from_multiple_outputs(self, outputs: Set[Path]) -> Set[DiscreteEventModel]:
        """Returns outputs given its weights. Weight 1 ignores any other
        weights. Weights represent percentage of propagation

        Args:
            outputs: Set of output paths for a model.
        """
        ones = [path.get_model() for path in outputs if path.get_weight() == 1]
        if len(ones) > 0:
            return cast(Any, ones)
        probability = random()
        a_probability = 0
        outs = list(outputs)
        outs.sort()
        for o in outs:
            if probability <= o.get_weight() + a_probability:
                return cast(Set[DiscreteEventModel], {o.get_model()})
            a_probability += o.get_weight()
        return set()

    def _get_affected_models_inputs(
            self,
            all_autonomous_models: Set[DiscreteEventModel],
            input_models: Set[DiscreteEventModel],
    ) -> (Set[DiscreteEventModel], Dict[str, ModelInput]):
        """Gets models that will change by the output computed

        Args:
            all_autonomous_models: Models that its outputs were computed.
            input_models: Models that its state was changed by the external
                transition.
        """
        affected_models_inputs: Dict[str, ModelInput] = {}
        affected_models = set()
        for model in all_autonomous_models:
            # get all output models
            outputs = model.get_output_models().difference(input_models)

            # extract relevant outputs by weight
            outputs = self._select_outputs_from_multiple_outputs(outputs)

            for out in outputs:
                # adds affected model to confluent models
                affected_models.add(out)

                # checks if the model exist
                if out.get_id() in affected_models_inputs:
                    # adds an input to an existing affected model
                    affected_models_inputs[out.get_id()][model.get_id()] = self._outputs[
                        model.get_id()
                    ]
                else:
                    # create a new input map for the affected model
                    affected_models_inputs[out.get_id()] = {
                        model.get_id(): self._outputs[model.get_id()]
                    }
        return affected_models, affected_models_inputs

    def _execute_external(
            self, input_model_values: DynamicSystemInput, event_time: float
    ) -> Set[DiscreteEventModel]:
        """Executes external transition for the given input.

        Args:
            input_model_values (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            event_time (float): Time of the event.
        """
        input_models = set()
        if input_model_values is not None:
            for model in input_model_values:
                self._models[model].state_transition(input_model_values[model], event_time)
                input_models.add(self._models[model])
        return input_models
