from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING

from dynamic_system.models.state_model import StateModel

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_dynamic_system import DiscreteEventDynamicSystem


class DiscreteEventModel(StateModel):
    """Discrete event abstract model"""
    _currentDynamicSystem: DiscreteEventDynamicSystem

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str = None, state=None):
        """
        Args:
            dynamic_system (DynamicSystem): Dynamic system of the model.
            name (str): Name of the model.
            state (Any): Initial state of the model.
        """
        super().__init__(dynamic_system, name, state)
        self._currentDynamicSystem.schedule(self, self.timeAdvanceFunction(self._currentState))

    def confluentStateTransitionFunction(self, state: Any, inputs: Any) -> Any:
        """
        .. math:: \delta_con(s,x)

        Implements the confluent state transition function delta. The
        confluent state transition executes an external transition function at
        the time of an autonomous event.

        .. math:: \delta_con \; : \; S \; x \; X \longrightarrow S

        Args:
            state (Any):
            inputs (Any):
        """
        new_state = self.internalStateTransitionFunction(state)
        return self.externalStateTransitionFunction(new_state, inputs, 0)  # 0 because is equal to (e = ta(s)) ½ ta(s)

    def stateTransition(self, inputs: Any = None, event_time: float = 0):
        """Executes the state transition using the state given by the state
        transition function. If there are not inputs is an internal
        transition, otherwise it is an external transition.

        Args:
            inputs (Any): Input trajectory x. If it is None, the state
                transition is autonomous
            event_time (float): Time of the event. If there are inputs and the
                time is ta(s), it is an confluent transition.
        """
        new_state: Any
        if inputs is None:
            # is an autonomous event
            new_state = self.internalStateTransitionFunction(self._currentState)
        elif event_time is self.timeAdvanceFunction(self._currentState):
            # is an confluent event
            new_state = self.confluentStateTransitionFunction(self._currentState, inputs)
        else:
            # time is between autonomous events, so it is an external event
            new_state = self.externalStateTransitionFunction(self._currentState, inputs, event_time)
        self.setUpState(new_state)

    @abstractmethod
    def internalStateTransitionFunction(self, state: Any) -> Any:
        """
        .. math:: \delta_int(s)

        Implements the internal state transition function delta. The internal
        state transition function takes the system from its state at the time of
        the autonomous event to a subsequent state.

        .. math:: \delta_int \; : \; S \longrightarrow S

        Args:
            state (Any): Current state of the model.
        """
        pass

    @abstractmethod
    def externalStateTransitionFunction(self, state: Any, inputs: Any, event_time: float) -> Any:
        """
        .. math:: \delta_ext((s,e), x)

        Implements the external state transition function delta. The external
        state transition function computes the next state of the model from its
        current total state (s,e) Q at time of an input and the input itself.

            .. math:: \delta_ext \; : \; Q \; x \; X \longrightarrow S

        Args:
            state (Any): Current state of the model.
            inputs (Any): Input trajectory x.
            event_time (float): Time of event e.
        """
        pass

    @abstractmethod
    def timeAdvanceFunction(self, state: Any) -> float:
        """ta(s)

        Implement the model’s time advance function ta. The time advance
        function schedules output from the model and autonomous changes in its
        state.

        .. math:: ta \; : \; S \longrightarrow R_{0^\infty}

        Args:
            state (Any): Current state of the system.
        """
        pass

    def getTime(self) -> float:
        """Gets the time of the next autonomous event."""
        return self.timeAdvanceFunction(self._currentState)

    @abstractmethod
    def outputFunction(self, state: Any) -> Any:  # Overwritten documentation
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer when e=ta(s).

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (Any): current state s of the model.
        """
        pass
