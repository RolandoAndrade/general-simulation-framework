from __future__ import annotations

from typing import Set, Dict, TYPE_CHECKING


from dynamic_system.base_model import BaseModel

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


class NetworkModel(BaseModel):
    """Group of atomic and network models that are connected"""

    _inputs: Set[BaseModel]

    def state_transition_function(self, bag_xb: BagOfValues):
        for model in self._inputs:
            model.state_transition_function(bag_xb)

    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        for model in self._inputs:
            model.compute_output()

    def compute_output(self) -> BagOfValues:
        return self.output_function(self._output_bag)