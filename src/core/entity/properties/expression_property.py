from core.expresions.expression import Expression
from core.entity.core.entity_property import EntityProperty
from core.entity.core.property_type import PropertyType


class ExpressionProperty(EntityProperty):
    def __init__(self, value: Expression):
        super().__init__(value, PropertyType.EXPRESSION)

    def get_value(self) -> Expression:
        """Returns the value of the property"""
        return super().get_value()
