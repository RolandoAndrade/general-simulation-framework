from __future__ import annotations

from typing import Any, Dict

from core.entity.core import EntityProperties, EntityManager
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from queue_simulator.queue_components.buffer.buffers import InputBuffer
from queue_simulator.queue_components.shared.models import SimulatorComponent
from queue_simulator.queue_components.shared.stats import Statistical, ComponentStats
from queue_simulator.queue_components.sink.sink_state import SinkState


class Sink(DiscreteEventModel, SimulatorComponent, Statistical):
    """Sink of entities"""

    def get_expressions(self) -> Dict[str, Any]:
        return self.get_state().get_state_expressions()

    def _internal_state_transition_function(self, state: SinkState) -> SinkState:
        return state

    def _external_state_transition_function(
            self, state: SinkState, inputs: ModelInput, event_time: Time
    ) -> SinkState:
        r_inputs = []
        for i in inputs:
            r_inputs += inputs[i]
        state.input_buffer.add(r_inputs)
        self.schedule(self.get_time())
        return state

    def _time_advance_function(self, state: SinkState) -> Time:
        return Time(0)

    def _output_function(self, state: SinkState) -> Any:
        return state.input_buffer.empty()

    def get_properties(self) -> EntityProperties:
        return {}

    def __init__(
            self,
            dynamic_system: DiscreteEventDynamicSystem,
            name: str,
            entity_manager: EntityManager = None,
    ):
        super(Sink, self).__init__(
            dynamic_system,
            name,
            SinkState(InputBuffer(name, entity_manager=entity_manager)),
            entity_manager,
        )

    def __str__(self):
        return self.get_id()

    def set_id(self, name: str):
        super(Sink, self).set_id(name)
        try:
            self.get_state().rename(name)
        except AttributeError:
            pass

    def get_stats(self) -> ComponentStats:
        return ComponentStats(
            "Sink", self.get_id(), [self.get_state().input_buffer.get_datasource()]
        )

    def clear(self):
        self.get_state().input_buffer.reset()
        self.unschedule()
