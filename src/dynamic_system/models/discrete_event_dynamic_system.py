from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, List, Union

from dynamic_system.control.scheduler import Scheduler
from dynamic_system.models.dynamic_system import DynamicSystem

if TYPE_CHECKING:
    from dynamic_system.models.state_model import StateModel


class DiscreteEventDynamicSystem(DynamicSystem):
    _scheduler: Scheduler  # Scheduler of events

    def __init__(self, scheduler: Scheduler = Scheduler()):
        super().__init__()
        self._scheduler = scheduler

    def schedule(self, model: StateModel, time: float):
        """Schedules an event at the specified time
        :param model Model with an autonomous event scheduled
        :param time Time to execute event
        """
        self._scheduler.schedule(model, time)

    def getOutput(self) -> Dict[str, Any]:
        """Gets the output of all the models in the dynamic system"""
        # TODO Not compute all outputs of discrete-event models
        for model in self._models:
            self._outputs[model] = self._models[model].getOutput()
        return self._outputs

    def stateTransition(self, input_models_values: Dict[str, Any] = None, event_time: float = 0):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        :param input_models_values: Dictionary with key the identifier of the model
        :param event_time: Time of the event.
        and value the inputs for that model.
        """
        if input_models_values is None:
            input_models_values = {}

        for model in input_models_values:
            self._models[model].stateTransition(input_models_values[model], event_time)
        for model in self._inputs:
            if model not in input_models_values:
                vs = self._getValuesToInject(self._inputs[model])
                self._models[model].stateTransition(vs, event_time)

    def getNextModel(self) -> StateModel:
        """Get the next model that will execute an autonomous event"""
        return self._scheduler.getNextModel()

    def getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._scheduler.getTimeOfNextEvent()
