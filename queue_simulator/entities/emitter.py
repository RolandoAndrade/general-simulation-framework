from core.entity.core import Entity, EntityEmitter, EntityProperties
from queue_simulator.entities import NameGenerator, AvailableEntities
from queue_simulator.entities.generated_entity import GeneratedEntity
from queue_simulator.shared.models import SerializableComponent


class Emitter(SerializableComponent, EntityEmitter):
    """Entity entities for a queue network system"""

    _properties: EntityProperties
    """Properties of the entities to be generated."""

    _entity_manager: NameGenerator

    def __init__(self, name: str, entity_manager: NameGenerator = None):
        super().__init__(name, entity_manager)
        self._properties = {}

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return self._properties

    def generate(self) -> Entity:
        """Generates an entity"""
        return GeneratedEntity(self._entity_manager.get_name(AvailableEntities.ENTITY),
                               self._properties, self._entity_manager)

    def __str__(self):
        return self.get_id()
