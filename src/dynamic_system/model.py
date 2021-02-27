from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from core.events.event_bus import subscriber, subscribe
from dynamic_system.events.external_state_transition_event import ExternalStateTransitionEvent


if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues
    from dynamic_system.input_manager import InputManager
    from dynamic_system.scheduler import Scheduler, static_scheduler

from dynamic_system.base_model import BaseModel


@subscriber
class Model(BaseModel):
    """A dynamic system that changes in response to its environment and affects
    its environment as it changes
    """

    _input_manager: InputManager
    _last_inputs: BagOfValues
    _scheduler: Scheduler

    def __init__(self, scheduler: Scheduler = static_scheduler):
        self._scheduler = scheduler
        self._scheduler.schedule(self, self.time_advance_function())

    def receive_input(self, model_id: int, inputs: BagOfValues):
        self._input_manager.save_input(model_id, inputs)
        if self._input_manager.is_ready():
            self._last_inputs = self._input_manager.get_inputs()
            self.notify_output(self._last_output)
            self._input_manager.clear()

    def internal_transition(self):
        return self.internal_state_transition_function()

    def confluent_transition(self):
        return self.confluent_state_transition_function(self._last_inputs)

    @subscribe(ExternalStateTransitionEvent)
    def _external_transition(self, event: ExternalStateTransitionEvent):
        return self.external_state_transition_function(self._last_inputs, event.get_time())

    @abstractmethod
    def internal_state_transition_function(self):
        """Implements the internal state transition function. The internal state transition function computes the next state
        of the model from the state of an autonomous action

         .. math:: \delta_int \; : \; S \longrightarrow S
        """
        pass

    @abstractmethod
    def external_state_transition_function(self, xb: BagOfValues, event_time: float):
        """Implements the external state transition function. The external state transition function computes the
        next state of the model from its current total state Q and a bag xb of inputs in X

         .. math:: \delta_ext \; : \; Q \; x \; X^b \longrightarrow S

        :param xb: Inputs for the transition
        :param event_time: time of event
        """
        pass

    def confluent_state_transition_function(self, xb: BagOfValues):
        """Implements the confluent state transition function. The confluent state transition function computes the
        next state of the model from its current state S and a bag xb of inputs in X

         .. math:: \delta_con \; : \; S \; x \; X^b \longrightarrow S

        """
        self.internal_state_transition_function()
        return self.external_state_transition_function(xb, self.time_advance_function())

    @abstractmethod
    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        """Implements the output function. The output function maps the current state S
        to a bag yb of outputs in Y

        .. math:: \lambda \; : \; S \; \longrightarrow Y^b

        :param output_bag: set of bags with elements in Y (outputs set) where state will be mapped
        :returns bag yb of outputs in Y
        """
        pass

    @abstractmethod
    def time_advance_function(self) -> float:
        """Implement the model’s time advance function.

        :returns time of the autonomous event
        """
        pass
