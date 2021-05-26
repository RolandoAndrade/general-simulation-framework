from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, List, Union, Set
from dynamic_system.control.scheduler import Scheduler

if TYPE_CHECKING:
    from dynamic_system.models.model import Model, ModelInput
    DynamicSystemOutput = DynamicSystemInput = Dict[str, Any]
    DynamicSystemModels = Dict[str, Model]


class DynamicSystem:
    _models: DynamicSystemModels
    _outputs: DynamicSystemOutput  # Output of all the models
    _scheduler: Scheduler  # Scheduler of events

    def __init__(self, scheduler: Scheduler = Scheduler()):
        """
        Args:
            scheduler (Scheduler): Future event list manager
        """
        self._models = dict()
        self._scheduler = scheduler

    def add(self, model: Model):
        """Adds a model to the dynamic system.
        :param model: Model to be added."""
        if model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")
        self._models[model.getID()] = model

    def schedule(self, model: Model, time: float):
        """Schedules an event at the specified time

        Args:
            model (StateModel): Model with an autonomous event scheduled
            time (float): Time to execute event
        """
        self._scheduler.schedule(model, time)

    def getNextModels(self) -> Set[Model]:
        """Gets the next models that will execute an autonomous event"""
        return self._scheduler.getNextModels()

    def getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._scheduler.getTimeOfNextEvent()

    def getOutput(self) -> DynamicSystemOutput:
        """Gets the output of all the models in the dynamic system. Changes only
        the model that changes at time t
        """
        models = self.getNextModels()
        self._outputs = {}
        for model in models:
            output = model.getOutput()
            self._outputs[model.getID()] = output
        return self._outputs

    def stateTransition(self, input_models_values: DynamicSystemInput = None, event_time: float = 0):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        Args:
            input_models_values (DynamicSystemInput): Dictionary with key the identifier of the model
            and value the input for that model.
            event_time (float): Time of the event.
        """
        # subtract time
        self._scheduler.updateTime(event_time)

        input_models = set()

        # execute external transition for the given input
        if input_models_values is not None:
            for model in input_models_values:
                self._models[model].stateTransition(input_models_values[model], event_time)
                input_models.add(input_models_values[model])

        # there are models expecting an autonomous event
        if self.getTimeOfNextEvent() is 0:
            # get the models that will execute an autonomous event
            all_autonomous_models = self._scheduler.popNextModels()

            # remove models that executed an external event
            autonomous_models = all_autonomous_models.difference(input_models)

            # get models that will change by the output computed
            affected_models_inputs: Dict[str, ModelInput] = {}

            affected_models = set()

            for model in autonomous_models:
                outputs = model.getOutputModels().difference(input_models)
                for out in outputs:
                    # adds affected model to confluent models
                    affected_models.add(out)

                    # checks if the model exist
                    if out.getID() in affected_models_inputs:
                        # adds an input to an existing affected model
                        affected_models_inputs[out.getID()][model.getID()] = self._outputs[model.getID()]
                    else:
                        # create a new input map for the affected model
                        affected_models_inputs[out.getID()] = {
                            model.getID(): self._outputs[model.getID()]
                        }

            # remove from autonomous models, models that will execute a confluent transition
            autonomous_models = autonomous_models.difference(affected_models)

            # execute autonomous event
            for model in autonomous_models:
                model.stateTransition(None, event_time)

            for model in affected_models:
                model.stateTransition(affected_models_inputs[model.getID()], event_time)
            for model in all_autonomous_models:
                self.schedule(model, model.getTime())
