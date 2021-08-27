from core.entity.core import Entity, EntityEmitter, EntityProperties
from queue_simulator.entities.generated_entity import GeneratedEntity


class Emitter(Entity, EntityEmitter):
    """Entity entities for a queue network system"""

    _properties: EntityProperties
    """Properties of the entities to be generated."""

    def __init__(self, name: str):
        super().__init__(name)
        self._properties = {}

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return self._properties

    def generate(self) -> Entity:
        """Generates an entity"""
        return GeneratedEntity(self.get_id(), self._properties)
