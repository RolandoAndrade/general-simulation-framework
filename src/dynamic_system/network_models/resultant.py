from __future__ import annotations

from typing import TYPE_CHECKING, Set, Dict

from dynamic_system.atomic_models.bag_of_values import BagOfValues

if TYPE_CHECKING:
    from dynamic_system.network_models.network_model import NetworkModel

from dynamic_system.atomic_models.atomic_model import AtomicModel


class AtomicModelAdapter(AtomicModel):
    """Encapsulates a Network Model to make it appear as an Atomic Model"""

    _model: NetworkModel
    _components: Set[AtomicModel]
    _inputs: Dict[AtomicModel, BagOfValues]
    _outputs: Dict[AtomicModel, BagOfValues]

    def state_transition_function(self, bag_xb: BagOfValues):
        pass

    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        pass

    def route(self, values: BagOfValues, source: AtomicModel):
