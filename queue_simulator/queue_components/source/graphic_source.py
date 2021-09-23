from typing import Any

from core.entity.core import EntityManager
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from queue_simulator.queue_components.shared.graphic import GraphicComponent
from queue_simulator.queue_components.shared.graphic.graphic_component import SerializedGraphicComponent
from queue_simulator.queue_components.source import Source


class GraphicSource(Source, GraphicComponent):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str, entity_manager: EntityManager):
        super().__init__(dynamic_system, name, entity_manager=entity_manager)
        self.set_position({'x': 0, 'y': 0})

    def serialize(self) -> SerializedGraphicComponent:
        d: Any = super().serialize()
        d.update({'position': self.get_position()})
        return d
