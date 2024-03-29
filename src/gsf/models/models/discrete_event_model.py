"""Discrete Event Model
==========================
This module contains the definition of a discrete-event simulation Model.
It has an abstract definition DiscreteEventModel that should be extended,
implementing its abstract methods.

Example:
    Creating a model::

        class Station(DiscreteEventModel):
            _processing_time: Expression

            def __init__(
                self, dynamic_system: DiscreteEventDynamicSystem, processing_time: Expression
            ):
                super().__init__(dynamic_system, state={"parts": 0, "remaining_time": -1})
                self._processing_time = processing_time

            def _internal_state_transition_function(self, state: StationState) -> StationState:
                state["parts"] = max(state["parts"] - 1, 0)
                self.schedule(self.get_time())
                return state

            def _external_state_transition_function(
                self, state: StationState, inputs: Dict[str, int], event_time: Time
            ) -> StationState:
                values = inputs.values()
                state["remaining_time"] = state["remaining_time"] - event_time
                for number_of_parts in values:
                    if state["parts"] > 0:
                        state["parts"] = state["parts"] + number_of_parts
                    elif state["parts"] == 0:
                        state["parts"] = number_of_parts
                        self.schedule(self.get_time())
                return state

            def _time_advance_function(self, state: StationState) -> Time:
                if state["parts"] < 1:
                    state["remaining_time"] = Time(-1)
                else:
                    state["remaining_time"] = Time(self._processing_time.evaluate())
                return state["remaining_time"]

            def _output_function(self, state: StationState) -> int:
                if state["parts"] > 0:
                    return 1
                return 0

            def __str__(self):
                return self.get_id()
"""


from __future__ import annotations

from abc import abstractmethod
from typing import Any, cast, TYPE_CHECKING

from gsf.core.debug.domain.debug import debug
from gsf.core.entity.properties.expression_property import ExpressionProperty
from gsf.core.mathematics.values.value import Value
from gsf.core.types import Time
from gsf.core.types.model_input import ModelInput
from gsf.models.core.base_model import BaseModel, ModelState
from gsf.dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)

if TYPE_CHECKING:
    from gsf.core.entity.core import EntityManager


class DiscreteEventModel(BaseModel):
    """DiscreteEventModel

    A discrete-event model executes can receive inputs at any time. Each event occurs at
    a particular instant in time and marks a change of state in the system.
    """

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        name: str = None,
        state: ModelState = None,
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
            entity_manager (EntityManager): Delegated entity manager.
        """
        super().__init__(dynamic_system, name, state, entity_manager)

    @debug("Scheduling model")
    def schedule(self, time: Time):
        """Schedules an autonomous event

        Args:
            time (float): Time when the event will be executed.
        """
        cast(DiscreteEventDynamicSystem, self.get_dynamic_system()).schedule(self, time)

    @debug("Unschedule model")
    def unschedule(self):
        """Unscheduled an autonomous event"""
        cast(DiscreteEventDynamicSystem, self.get_dynamic_system()).unschedule(self)

    @debug("Adding path")
    def add(
        self,
        model: DiscreteEventModel,
        weight: ExpressionProperty = ExpressionProperty(Value(1)),
        name: str = None,
    ) -> DiscreteEventModel:
        """Adds a model as an input for the current model in the dynamic system and returns the model added.

        Args:
            model (BaseModel): Output model to be added.
            weight (ExpressionProperty): Weight of the path.
            name (str): Name of the path.
        """
        return cast(DiscreteEventModel, super().add(model, weight, name))

    @debug("Getting time")
    def get_time(self) -> Time:
        """Gets the time of the next autonomous event."""
        try:
            return self._time_advance_function(self.get_state())
        except AttributeError:
            return Time(0)

    def get_output(self) -> Any:
        """Gets the output of the model."""
        return self._output_function(self.get_state())

    @debug("Executing state transition")
    def state_transition(self, inputs: ModelInput = None, event_time: Time = 0):
        """Executes the state transition using the state given by the state
        transition function. If there are no inputs is an internal transition,
        otherwise it is an external transition.

        Args:
            inputs (ModelInput): Input trajectory x. If it is None, the state
                transition is autonomous
            event_time (Time): Time of the event. If there are inputs and the
                time is ta(s), it is an confluent transition.
        """
        new_state: ModelState
        if inputs is None:
            # is an autonomous event
            new_state = self._internal_state_transition_function(self.get_state())
        elif event_time == self.get_time() or event_time == 0:
            # is an confluent event
            new_state = self._confluent_state_transition_function(
                self.get_state(), inputs
            )
        else:
            # time is between autonomous events, so it is an external event
            new_state = self._external_state_transition_function(
                self.get_state(), inputs, event_time
            )
        self.set_up_state(new_state)

    def _confluent_state_transition_function(
        self, state: ModelState, inputs: ModelInput
    ) -> ModelState:
        """
        .. math:: \delta_{con}(s,x)

        Implements the confluent state transition function delta. The
        confluent state transition executes an external transition function at
        the time of an autonomous event.

        .. math:: \delta_{con} \; : \; S \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
        """
        new_state = self._internal_state_transition_function(state)
        return self._external_state_transition_function(
            new_state, inputs, Time(0)
        )  # 0 because is equal to (e = ta(s)) ½ ta(s)

    @abstractmethod
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        """
        .. math:: \delta_{int}(s)

        Implements the internal state transition function delta. The internal
        state transition function takes the system from its state at the time of
        the autonomous event to a subsequent state.

        .. math:: \delta_{int} \; : \; S \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
        """
        raise NotImplementedError

    @abstractmethod
    def _external_state_transition_function(
        self, state: ModelState, inputs: ModelInput, event_time: Time
    ) -> ModelState:
        """
        .. math:: \delta_{ext}((s,e), x)

        Implements the external state transition function delta. The external
        state transition function computes the next state of the model from its
        current total state (s,e) Q at time of an input and the input itself.

            .. math:: \delta_{ext} \; : \; Q \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        raise NotImplementedError

    @abstractmethod
    def _time_advance_function(self, state: ModelState) -> Time:
        """.. math:: ta(s)

        Implement the model’s time advance function ta. The time advance
        function schedules output from the model and autonomous changes in its
        state.

        .. math:: ta \; : \; S \longrightarrow R_{0^\infty}

        Args:
            state (ModelState): Current state of the system.
        """
        raise NotImplementedError

    @abstractmethod
    def _output_function(self, state: ModelState) -> Any:
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer when e=ta(s).

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (ModelState): current state s of the model.
        """
        raise NotImplementedError
