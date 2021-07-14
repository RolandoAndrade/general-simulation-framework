from core.components.entity.core.entity_property import EntityProperty
from core.components.entity.core.property_type import PropertyType
from core.components.expresions.expression import Expression


class ExpressionProperty(EntityProperty):
    def __init__(self, value: Expression):
        super().__init__(value, PropertyType.EXPRESSION)

    def getValue(self) -> Expression:
        """Returns the value of the property"""
        return super().getValue()
