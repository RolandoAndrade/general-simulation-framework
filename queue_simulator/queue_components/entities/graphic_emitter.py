from typing import Any

from queue_simulator.queue_components.entities import Emitter, NameGenerator
from queue_simulator.queue_components.shared.graphic import GraphicComponent
from queue_simulator.queue_components.shared.graphic.graphic_component import SerializedGraphicComponent


class GraphicEmitter(Emitter, GraphicComponent):
    def __init__(self, name: str, entity_manager: NameGenerator):
        super().__init__(name, entity_manager)
        self.set_position({'x': 0, 'y': 0})

    def serialize(self) -> SerializedGraphicComponent:
        d: Any = super().serialize()
        d.update({'position': self.get_position()})
        return d
