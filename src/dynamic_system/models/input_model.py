from __future__ import annotations

from typing import TYPE_CHECKING

from core.events.event_bus import subscriber, subscribe
from dynamic_system.models.base_model import BaseModel
from dynamic_system.events.compute_output_event import ComputeOutputEvent

if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues


@subscriber
class InputModel(BaseModel):
    inputs: BagOfValues

    def __init__(self, inputs: BagOfValues):
        super().__init__()
        self._inputs = inputs

    @subscribe(ComputeOutputEvent)
    def receive_input(self):
        out = self._inputs
        self.notify_output(out)
