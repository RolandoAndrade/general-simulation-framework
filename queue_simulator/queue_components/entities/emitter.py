from typing import Dict, Any

from core.entity.core import Entity, EntityEmitter, EntityProperties
from core.entity.properties import NumberProperty
from queue_simulator.queue_components.entities import NameGenerator, AvailableEntities
from queue_simulator.queue_components.entities.generated_entity import GeneratedEntity
from queue_simulator.queue_components.shared.models import SimulatorComponent


class Emitter(SimulatorComponent, EntityEmitter):
    """Entity entities for a queue network system"""

    _generated: NumberProperty
    """Number of generated entities"""

    _properties: EntityProperties
    """Properties of the entities to be generated."""

    _entity_manager: NameGenerator

    def __init__(self, name: str, entity_manager: NameGenerator = None):
        super().__init__(name, entity_manager)
        self._properties = {}
        self._generated = NumberProperty(0)

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return self._properties

    def generate(self) -> Entity:
        """Generates an entity"""
        self._generated += 1
        return GeneratedEntity(
            self._entity_manager.get_name(AvailableEntities.ENTITY),
            self._properties,
            self._entity_manager,
        )

    def __str__(self):
        return self.get_id()

    def get_expressions(self) -> Dict[str, Any]:
        return {
            "GeneratedEntities": {
                "value": self.get_id() + "." + str(self._generated),
                "call": self._generated.get_value
            }
        }
