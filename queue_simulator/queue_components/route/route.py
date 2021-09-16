from typing import Dict, Any

from core.entity.properties import ExpressionProperty
from core.mathematics.values.value import Value
from models.core import Path, BaseModel
from queue_simulator.queue_components.entities import NameGenerator, AvailableEntities
from queue_simulator.queue_components.shared.models import SimulatorComponent


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
