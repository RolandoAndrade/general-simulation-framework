from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Set
from dynamic_system.discrete_events.future_event_list.scheduler import Scheduler

if TYPE_CHECKING:
    from dynamic_system.discrete_events.models.discrete_event_model import (
        DiscreteEventModel,
        ModelInput,
    )

    DynamicSystemOutput = Dict[str, Any]
    DynamicSystemModels = Dict[str, DiscreteEventModel]
    DynamicSystemInput = Dict[str, ModelInput]


class DiscreteEventDynamicSystem:
    """Dynamic system for discrete-event models"""

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

    def add(self, model: DiscreteEventModel):
        """Adds a model to the dynamic system.

        Args:
            model (DiscreteEventModel): Model to be added.
        """
        if model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")
        self._models[model.getID()] = model

    def schedule(self, model: DiscreteEventModel, time: float):
        """Schedules an event at the specified time

        Args:
            model (DiscreteEventModel): Model with an autonomous event scheduled
            time (float): Time to execute event
        """
        self._scheduler.schedule(model, time)

    def getNextModels(self) -> Set[DiscreteEventModel]:
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

    def stateTransition(
        self, inputModelsValues: DynamicSystemInput = None, eventTime: float = 0
    ):
        """Executes the state transition of the models. If an input is given,
        the models defined as its inputs will be ignored.

        Args:
            inputModelsValues (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            eventTime (float): Time of the event.
        """
        # subtract time
        self._scheduler.updateTime(eventTime)

        inputModels = self._executeExternal(inputModelsValues, eventTime)

        autonomousModels = self._executeAutonomous(eventTime, inputModels)

        # schedules models that executed its autonomous transition
        for model in autonomousModels:
            self.schedule(model, model.getTime())

    def _executeAutonomous(
        self, eventTime: float, inputModels: Set[DiscreteEventModel]
    ) -> Set[DiscreteEventModel]:
        """Executes autonomous transition for the given input and external
        events of the affected models.

        Args:
            eventTime (float): Time of the event.
            inputModels: Models that its state was changed by the external
                transition.
        """
        allAutonomousModels = set()
        # there are models expecting an autonomous event
        if self.getTimeOfNextEvent() == 0:
            # get the models that will execute an autonomous event
            allAutonomousModels = self._scheduler.popNextModels()

            # remove models that executed an external event
            autonomousModels = allAutonomousModels.difference(inputModels)

            affectedModels, affectedModelsInputs = self._getAffectedModelsInputs(
                allAutonomousModels, inputModels
            )

            # remove from autonomous models, models that will execute a confluent transition
            autonomousModels = autonomousModels.difference(affectedModels)

            # execute autonomous event
            for model in autonomousModels:
                model.stateTransition(None, eventTime)

            for model in affectedModels:
                model.stateTransition(affectedModelsInputs[model.getID()], eventTime)

        return allAutonomousModels

    def _getAffectedModelsInputs(
        self,
        allAutonomousModels: Set[DiscreteEventModel],
        inputModels: Set[DiscreteEventModel],
    ) -> (Set[DiscreteEventModel], Dict[str, ModelInput]):
        """Gets models that will change by the output computed

        Args:
            allAutonomousModels: Models that its outputs were computed.
            inputModels: Models that its state was changed by the external
                transition.
        """
        affectedModelsInputs: Dict[str, ModelInput] = {}
        affectedModels = set()
        for model in allAutonomousModels:
            outputs = model.getOutputModels().difference(inputModels)
            for out in outputs:
                # adds affected model to confluent models
                affectedModels.add(out)

                # checks if the model exist
                if out.getID() in affectedModelsInputs:
                    # adds an input to an existing affected model
                    affectedModelsInputs[out.getID()][model.getID()] = self._outputs[
                        model.getID()
                    ]
                else:
                    # create a new input map for the affected model
                    affectedModelsInputs[out.getID()] = {
                        model.getID(): self._outputs[model.getID()]
                    }
        return affectedModels, affectedModelsInputs

    def _executeExternal(
        self, inputModelValues: DynamicSystemInput, eventTime: float
    ) -> Set[DiscreteEventModel]:
        """Executes external transition for the given input.

        Args:
            inputModelValues (DynamicSystemInput): Dictionary with key the
                identifier of the model.
            eventTime (float): Time of the event.
        """
        input_models = set()
        if inputModelValues is not None:
            for model in inputModelValues:
                self._models[model].stateTransition(inputModelValues[model], eventTime)
                input_models.add(self._models[model])
        return input_models
