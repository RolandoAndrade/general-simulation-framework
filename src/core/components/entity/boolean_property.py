from core.components.entity.entity_property import EntityProperty
from core.components.entity.property_type import PropertyType


class BooleanProperty(EntityProperty):
    def __init__(self, property_name: str, value: bool):
        super().__init__(property_name, value, PropertyType.BOOLEAN)

    def getValue(self) -> bool:
        """Returns the value of the property"""
        return super().getValue()
