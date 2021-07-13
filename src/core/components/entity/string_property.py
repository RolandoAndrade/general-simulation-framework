from core.components.entity.entity_property import EntityProperty
from core.components.entity.property_type import PropertyType


class StringProperty(str, EntityProperty):
    def __new__(cls, value: str):
        return str.__new__(cls, value)

    def __init__(self, value: str):
        super().__init__(value, PropertyType.STRING)

    def getValue(self) -> str:
        """Returns the value of the property"""
        return super().getValue()