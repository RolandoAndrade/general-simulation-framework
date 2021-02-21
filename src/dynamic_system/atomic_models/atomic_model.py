from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues

from dynamic_system.base_model import BaseModel


class AtomicModel(BaseModel):
    """A dynamic system that changes in response to its environment and affects
    its environment as it changes
    """

    _output_bag: BagOfValues

    @abstractmethod
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

    def compute_output(self) -> BagOfValues:
        """Computes the output given by the output function

        :returns bag yb of outputs in Y
        """
        return self.output_function(self._output_bag)
