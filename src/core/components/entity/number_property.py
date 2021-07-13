from core.components.entity.entity_property import EntityProperty
from core.components.entity.property_type import PropertyType


class NumberProperty(EntityProperty):
    def __init__(self, property_name: str, value: float):
        super().__init__(property_name, value, PropertyType.NUMBER)

    def getValue(self) -> float:
        """Returns the value of the property"""
        return super().getValue()
