from core.components.entity.entity_property import EntityProperty
from core.components.entity.property_type import PropertyType


class StringProperty(EntityProperty):
    def __init__(self, property_name: str, value: str):
        super().__init__(property_name, value, PropertyType.STRING)

    def getValue(self) -> str:
        """Returns the value of the property"""
        return super().getValue()