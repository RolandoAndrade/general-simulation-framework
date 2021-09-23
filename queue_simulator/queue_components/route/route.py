from typing import Dict, Any

from core.entity.properties import ExpressionProperty
from core.mathematics.values.value import Value
from models.core import Path, BaseModel
from queue_simulator.queue_components.entities import NameGenerator, AvailableEntities
from queue_simulator.queue_components.shared.models import SimulatorComponent, SerializedComponent


class SerializedRoute(SerializedComponent):
    origin: str
    destination: str


class Route(Path, SimulatorComponent):
    def get_expressions(self) -> Dict[str, Any]:
        return {}

    def __init__(
            self, from_model: BaseModel, to_model: BaseModel, entity_manager: NameGenerator
    ):
        super().__init__(
            from_model,
            to_model,
            ExpressionProperty(Value(1)),
            entity_manager.get_name(AvailableEntities.PATH),
            entity_manager=entity_manager,
        )

    def serialize(self) -> SerializedRoute:
        s: Dict[str, Any] = super().serialize()
        s.update({'origin': self.get_source_model().get_id()})
        s.update({'destination': self.get_destination_model().get_id()})
        return s
