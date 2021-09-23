from typing import Any

from core.entity.core import EntityManager
from core.events import EventBus
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.queue_components.shared.graphic import GraphicComponent
from queue_simulator.queue_components.shared.graphic.graphic_component import SerializedGraphicComponent
from queue_simulator.queue_components.sink import Sink


class GraphicSink(Sink, GraphicComponent):
    event_bus: EventBus

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str,
                 entity_manager: EntityManager, event_bus: EventBus):
        super().__init__(dynamic_system, name, entity_manager=entity_manager)
        self.set_position({'x': 0, 'y': 0})
        self.event_bus = event_bus

    def serialize(self) -> SerializedGraphicComponent:
        d: Any = super().serialize()
        d.update({'position': self.get_position()})
        return d

    def state_transition(self, inputs: ModelInput = None, event_time: Time = 0):
        super().state_transition(inputs, event_time)
        self.event_bus.emit("state_changed", {
            'name': self.get_id(),
            'state': {
                'input_buffer': str(self.get_state().input_buffer.current_number_of_entities)
            }
        })
