from __future__ import annotations

from typing import TYPE_CHECKING

from core.events.event_bus import subscriber, subscribe
from dynamic_system.base_model import BaseModel
from dynamic_system.events.compute_output_event import ComputeOutputEvent

if TYPE_CHECKING:
    from dynamic_system.atomic_models.bag_of_values import BagOfValues


@subscriber
class InputModel(BaseModel):
    _inputs: BagOfValues

    @subscribe(ComputeOutputEvent)
    def compute_output(self) -> BagOfValues:
        out = self.output_function(self._inputs)
        return out

    def output_function(self, inputs: BagOfValues) -> BagOfValues:
        return inputs
