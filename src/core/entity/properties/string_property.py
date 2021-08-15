from core.entity.core.entity_property import EntityProperty
from core.entity.core.property_type import PropertyType


class StringProperty(str, EntityProperty):
    def __new__(cls, value: str):
        return str.__new__(cls, value)

    def __init__(self, value: str):
        super().__init__(value, PropertyType.STRING)

    def get_value(self) -> str:
        """Returns the value of the property"""
        return super().get_value()
