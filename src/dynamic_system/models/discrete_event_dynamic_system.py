from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Set

from dynamic_system.control.scheduler import Scheduler
from dynamic_system.models.dynamic_system import DynamicSystem

if TYPE_CHECKING:
    from dynamic_system.models.state_model import StateModel

DynamicSystemOutput = Dict[str, Any]
DynamicSystemInput = Dict[str, Any]


class DiscreteEventDynamicSystem(DynamicSystem):
    """Discrete event dynamic system implementation"""
    _scheduler: Scheduler  # Scheduler of events
    _changedModels: Set[StateModel]
    _wasOutputComputed: bool

    def __init__(self, scheduler: Scheduler = Scheduler()):
        """
        Args:
            scheduler (Scheduler): Future event list manager
        """
        super().__init__()
        self._scheduler = scheduler
        self._wasOutputComputed = False
        self._changedModels = set()

    def add(self, model: StateModel):
        """Adds a model to the dynamic system

        Args:
            model (StateModel): model to be added
        """
        super(DiscreteEventDynamicSystem, self).add(model)
        self._wasOutputComputed = False

    def schedule(self, model: StateModel, time: float):
        """Schedules an event at the specified time

        Args:
            model (StateModel): Model with an autonomous event scheduled
            time (float): Time to execute event
        """
        self._scheduler.schedule(model, time)

    def getOutput(self) -> DynamicSystemOutput:
        """Gets the output of all the models in the dynamic system. Changes only
        the model that changes at time t
        """
        if not self._wasOutputComputed:  # if the output of the network is not computed yet
            for model in self._models:
                self._outputs[model] = self._models[model].getOutput()
            self._wasOutputComputed = True
        else:
            self._outputs = {}
            models = self._scheduler.getNextModels()
            for model in models:
                self._outputs[model.getID()] = model.getOutput()
                for nn in self._inputs:
                    if model.getID() in self._inputs[nn]:
                        self._changedModels.add(self._models[nn])
        return self._outputs

    def stateTransition(self, input_models_values: DynamicSystemInput = None, event_time: float = 0):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        Args:
            input_models_values (DynamicSystemInput): Dictionary with key the identifier of the model
            event_time (float): Time of the event.
        """
        self._scheduler.updateTime(event_time)

        input_models = set()

        if input_models_values is not None:  # execute external transition
            for model in input_models_values:
                self._models[model].stateTransition(input_models_values[model], event_time)
            input_models = set([self._models[inp] for inp in input_models_values])

        if self.getTimeOfNextEvent() is 0:  # there are models expecting an autonomous event
            # get models that changed their input by the external events executed above
            external_models = self._changedModels
            external_models = external_models.difference(input_models)

            # get autonomous models that did not executed an external event (not confluent)
            r_autonomous_models = self._scheduler.popNextModels().difference(input_models)

            # remove models which inputs changed (not changed)
            autonomous_models = r_autonomous_models.difference(external_models)

            # TODO verify if this is necessary
            autonomous_models = autonomous_models.difference(input_models)  # do not repeat

            for model in autonomous_models:  # execute autonomous events
                model.stateTransition(None, event_time)

            for model in external_models:  # execute external transition for models that changed their inputs
                vs = self._getValuesToInject(self._inputs[model.getID()])
                model.stateTransition(vs, event_time)

            for model in r_autonomous_models:  # schedule all the models to its next time
                self._scheduler.schedule(model, model.getTime())

        self._changedModels = set()

    def getNextModel(self) -> Set[StateModel]:
        """Get the next model that will execute an autonomous event"""
        return self._scheduler.getNextModels()

    def getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._scheduler.getTimeOfNextEvent()
