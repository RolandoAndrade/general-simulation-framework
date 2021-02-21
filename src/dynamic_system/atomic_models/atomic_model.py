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
    def state_transition_function(self, bag_xb: BagOfValues):
        """Implements the state transition function. The state transition function computes the next
         state of the model from its current state s and a bag xb of inputs in X

        :param bag_xb: set of bags with elements in X (inputs set)
        """
        pass

    @abstractmethod
    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        """Implements the output function. The output function maps the current state s
        to a bag yb of outputs in Y

        :param output_bag: set of bags with elements in Y (outputs set) where state will be mapped
        :returns bag yb of outputs in Y
        """
        pass

    def compute_output(self) -> BagOfValues:
        """Computes the output given by the output function

        :returns bag yb of outputs in Y
        """
        return self.output_function(self._output_bag)
