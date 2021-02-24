from __future__ import annotations

from typing import TYPE_CHECKING


from dynamic_system.base_model import BaseModel

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


class InputModel(BaseModel):

    _inputs: BagOfValues

    def compute_output(self) -> BagOfValues:
        self.output_function(self._inputs)

    def output_function(self, inputs: BagOfValues) -> BagOfValues:
        """Implements the output function. The output function maps the current state s
        to a bag yb of outputs in Y

        :param output_bag: set of bags with elements in Y (outputs set) where state will be mapped
        :returns bag yb of outputs in Y
        """
        return inputs