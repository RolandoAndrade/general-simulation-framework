from core.components.entity.entity_property import EntityProperty
from core.components.entity.property_type import PropertyType


class NumberProperty(float, EntityProperty):
    def __new__(cls, value: float):
        return float.__new__(cls, value)

    def __init__(self, value: float):
        super().__init__(value, PropertyType.NUMBER)

    def getValue(self) -> float:
        """Returns the value of the property"""
        return super().getValue()
