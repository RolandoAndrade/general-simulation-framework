from __future__ import annotations

from dynamic_system.models.model import Model

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues


class AndGate(Model):
    def internal_state_transition_function(self):
        pass

    def external_state_transition_function(self, xb: BagOfValues, event_time: float):
        pass

    def output_function(self, output_bag: BagOfValues) -> BagOfValues:
        bag = output_bag['Input']
        return bag['x'] and bag['y']

    def time_advance_function(self) -> float:
        return 0
