from __future__ import annotations

from abc import abstractmethod
from typing import Any, Set, Dict, TYPE_CHECKING

from core.debug.domain.debug import debug
from dynamic_system.core.base_model import BaseModel
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)

if TYPE_CHECKING:
    ModelInput = Dict[str, Any]
    ModelState = Any


class DiscreteEventModel(BaseModel):
    """DiscreteEventModel with an state"""

    # current state of the model
    _currentState: ModelState

    # current dynamic system of the model
    _currentDynamicSystem: DiscreteEventDynamicSystem

    # output models of the model
    _outputModels: Set[DiscreteEventModel]

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        name: str = None,
        state: ModelState = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
        """
        super().__init__(name)
        # Init the model
        self.setUpState(state)
        # Add the model to the dynamic system
        self._currentDynamicSystem = dynamic_system
        self._currentDynamicSystem.add(self)
        self._outputModels = set()
        self.schedule(self.getTime())

    @debug("Adding output")
    def add(self, model: DiscreteEventModel):
        """Adds a model as an input for the current model in the dynamic system.

        Args:
            model (DiscreteEventModel): Model to be an input.
        """
        self._currentDynamicSystem.add(model)
        self._outputModels.add(model)

    @debug("Getting output models")
    def getOutputModels(self) -> Set[DiscreteEventModel]:
        """Returns the output models of the current model"""
        return self._outputModels

    @debug("Retrieving dynamic system")
    def getDynamicSystem(self) -> DiscreteEventDynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self._currentDynamicSystem

    @debug("Scheduling model")
    def schedule(self, time: float):
        """Schedules an autonomous event

        Args:
            time (float): Time when the event will be executed.
        """
        self._currentDynamicSystem.schedule(self, time)

    @debug("Setting up the state")
    def setUpState(self, state: ModelState):
        """s

        Sets up the state of the model.

        Args:
            state (ModelState): New state of the model.
        """
        self._currentState = state

    @debug("Getting output")
    def getOutput(self) -> Any:
        """Gets the output of the model."""
        return self.outputFunction(self._currentState)

    @debug("Getting time")
    def getTime(self) -> float:
        """Gets the time of the next autonomous event."""
        return self.timeAdvanceFunction(self._currentState)

    @debug("Executing state transition")
    def stateTransition(self, inputs: ModelInput = None, event_time: float = 0):
        """Executes the state transition using the state given by the state
        transition function. If there are not inputs is an internal transition,
        otherwise it is an external transition.

        Args:
            inputs (ModelInput): Input trajectory x. If it is None, the state
                transition is autonomous
            event_time (float): Time of the event. If there are inputs and the
                time is ta(s), it is an confluent transition.
        """
        new_state: ModelState
        if inputs is None:
            # is an autonomous event
            new_state = self.internalStateTransitionFunction(self._currentState)
        elif event_time is self.getTime():
            # is an confluent event
            new_state = self.confluentStateTransitionFunction(
                self._currentState, inputs
            )
        else:
            # time is between autonomous events, so it is an external event
            new_state = self.externalStateTransitionFunction(
                self._currentState, inputs, event_time
            )
        self.setUpState(new_state)

    def confluentStateTransitionFunction(
        self, state: ModelState, inputs: ModelInput
    ) -> ModelState:
        """
        .. math:: \delta_con(s,x)

        Implements the confluent state transition function delta. The
        confluent state transition executes an external transition function at
        the time of an autonomous event.

        .. math:: \delta_con \; : \; S \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
        """
        new_state = self.internalStateTransitionFunction(state)
        return self.externalStateTransitionFunction(
            new_state, inputs, 0
        )  # 0 because is equal to (e = ta(s)) ½ ta(s)

    @abstractmethod
    def internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        """
        .. math:: \delta_int(s)

        Implements the internal state transition function delta. The internal
        state transition function takes the system from its state at the time of
        the autonomous event to a subsequent state.

        .. math:: \delta_int \; : \; S \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
        """
        raise NotImplementedError

    @abstractmethod
    def externalStateTransitionFunction(
        self, state: ModelState, inputs: ModelInput, event_time: float
    ) -> ModelState:
        """
        .. math:: \delta_ext((s,e), x)

        Implements the external state transition function delta. The external
        state transition function computes the next state of the model from its
        current total state (s,e) Q at time of an input and the input itself.

            .. math:: \delta_ext \; : \; Q \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        raise NotImplementedError

    @abstractmethod
    def timeAdvanceFunction(self, state: ModelState) -> float:
        """ta(s)

        Implement the model’s time advance function ta. The time advance
        function schedules output from the model and autonomous changes in its
        state.

        .. math:: ta \; : \; S \longrightarrow R_{0^\infty}

        Args:
            state (ModelState): Current state of the system.
        """
        raise NotImplementedError

    @abstractmethod
    def outputFunction(self, state: ModelState) -> Any:
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer when e=ta(s).

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (ModelState): current state s of the model.
        """
        raise NotImplementedError

    def __str__(self):
        name = self.getID()
        state = self._currentState
        return name + ": {'state': " + str(state) + "}"
