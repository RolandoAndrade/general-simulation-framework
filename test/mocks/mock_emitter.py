from core.entity.core.entity import Entity
from core.entity.core.entity_emitter import EntityEmitter
from core.entity.core.entity_property import EntityProperties
from core.entity.properties.string_property import StringProperty


class MockEntity(Entity):

    def __init__(self, name: str):
        """
        Args:
            name (str): Name of the entity
        """
        super().__init__(name)

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            'type': StringProperty('Mock')
        }

    def __str__(self):
        return self.get_id()


class MockEmitter(EntityEmitter):
    __emitted = 0

    def generate(self) -> Entity:
        self.__emitted += 1
        return MockEntity(str(self.__emitted))
