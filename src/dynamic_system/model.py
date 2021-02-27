from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from core.events.event_bus import subscriber, subscribe
from dynamic_system.events.internal_state_transition_event import InternalStateTransitionEvent

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues
    from dynamic_system.input_manager import InputManager

from dynamic_system.base_model import BaseModel

@subscriber
class Model(BaseModel):
    """A dynamic system that changes in response to its environment and affects
    its environment as it changes
    """

    _input_manager: InputManager

    def receive_input(self, model_id: int, inputs: BagOfValues):
        self._input_manager.save_input(model_id, inputs)
        if self._input_manager.is_ready():
            all_inputs = self._input_manager.get_inputs()
            out = self.output_function(all_inputs)
            self.notify_output(out)

    @abstractmethod
    @subscribe(InternalStateTransitionEvent)
    def internal_state_transition_function(self):
        """Implements the internal state transition function. The internal state transition function computes the next state
        of the model from the state of an autonomous action

         .. math:: \delta_int \; : \; S \longrightarrow S
        """
        pass

    @abstractmethod
    def external_state_transition_function(self, bag_xb: BagOfValues, event_time: float):
        """Implements the external state transition function. The external state transition function computes the
        next state of the model from its current total state Q and a bag xb of inputs in X

         .. math:: \delta_ext \; : \; Q \; x \; X \longrightarrow S

        :param bag_xb: set of bags with elements in X (inputs set)
        :param event_time: time of event
        """
        pass

    def confluent_state_transition_function(self, bag_xb: BagOfValues):
        """Implements the confluent state transition function. The confluent state transition function computes the
        next state of the model from its current state S and a bag xb of inputs in X

         .. math:: \delta_con \; : \; S \; x \; X \longrightarrow S

        :param bag_xb: set of bags with elements in X (inputs set)
        """
        return self.external_state_transition_function(bag_xb, self.time_advance_function())

    @abstractmethod
    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        """Implements the output function. The output function maps the current state s
        to a bag yb of outputs in Y

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