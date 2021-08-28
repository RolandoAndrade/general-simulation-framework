from __future__ import annotations

from typing import Any

from core.entity.core import EntityProperties
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.buffer.buffers import InputBuffer
from queue_simulator.sink.sink_state import SinkState


class Sink(DiscreteEventModel):
    """Sink of entities"""

    def _internal_state_transition_function(self, state: SinkState) -> SinkState:
        return state

    def _external_state_transition_function(self, state: SinkState, inputs: ModelInput,
                                            event_time: Time) -> SinkState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.input_buffer.add(r_inputs)
        self.schedule(self.get_time())
        return state

    def _time_advance_function(self, state: SinkState) -> Time:
        return Time(1)

    def _output_function(self, state: SinkState) -> Any:
        return state.input_buffer.empty()

    def get_properties(self) -> EntityProperties:
        return {

        }

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str):
        super(Sink, self).__init__(dynamic_system, name, SinkState(InputBuffer(name)))

    def __str__(self):
        return self.get_id()