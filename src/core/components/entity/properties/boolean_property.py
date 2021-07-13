from core.components.entity.core.entity_property import EntityProperty
from core.components.entity.core.property_type import PropertyType


class BooleanProperty(EntityProperty):
    def __init__(self, value: bool):
        super().__init__(value, PropertyType.BOOLEAN)

    def __bool__(self):
        return self.getValue()

    def __eq__(self, other):
        return other == self.getValue()

    def getValue(self) -> bool:
        """Returns the value of the property"""
        return super().getValue()
