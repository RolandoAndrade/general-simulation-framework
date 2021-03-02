from __future__ import annotations

from dynamic_system.models.model import Model

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues


class AndGate(Model):
    def internalStateTransitionFunction(self):
        pass

    def externalStateTransitionFunction(self, xb: BagOfValues, event_time: float):
        pass

    def outputFunction(self, output_bag: BagOfValues) -> BagOfValues:
        bag = output_bag['Input']
        return bag['x'] and bag['y']

    def timeAdvanceFunction(self) -> float:
        return 0
