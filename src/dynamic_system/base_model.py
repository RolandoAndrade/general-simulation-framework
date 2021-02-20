from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues

from abc import abstractmethod


class BaseModel:
    @abstractmethod
    def state_transition_function(self, bag_xb: BagOfValues):
        """Implements the state transition function

        :param bag_xb: set of bags with elements in X (inputs set)
        """
        pass

    @abstractmethod
    def output_function(self, output_bag: BagOfValues):
        """Implements the output function

        :param output_bag: set of bags with elements in Y (outputs set)
        """
        pass

    def compute_output(self):
        """Computes the output given by the output function
        """
        self.output_function(self._output_bag)