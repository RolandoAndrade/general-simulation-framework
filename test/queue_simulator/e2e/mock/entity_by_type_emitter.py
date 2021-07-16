from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_emitter import EntityEmitter
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.string_property import StringProperty


class MockEntity(Entity):
    __type: StringProperty

    def __init__(self, name: str, e_type: str):
        """
        Args:
            name (str): Name of the entity
            e_type (str): Type of the entity
        """
        super().__init__(name)
        self.__type = StringProperty(e_type)

    def getProperties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            'type': self.__type
        }


class EntityByTypeEmitter(EntityEmitter):
    __emitted = 0
    __type: str

    def __init__(self, e_type: str):
        self.__type = e_type

    def generate(self) -> Entity:
        self.__emitted += 1
        return MockEntity(self.__type + "_" + str(self.__emitted), self.__type)
