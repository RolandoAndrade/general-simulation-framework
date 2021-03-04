from __future__ import annotations

from core.events.event_bus import subscriber, subscribe
from dynamic_system.models.base_model import BaseModel
from dynamic_system.events.compute_output_event import ComputeOutputEvent
from dynamic_system.utils.bag_of_values import BagOfValues


@subscriber
class InputModel(BaseModel):
    _inputs: BagOfValues

    def __init__(self, name: str = None, inputs: BagOfValues = None):
        super().__init__(name)
        self._inputs = inputs

    @subscribe(ComputeOutputEvent)
    def computeOutput(self):
        out = self._inputs
        self.notifyOutput(out)
