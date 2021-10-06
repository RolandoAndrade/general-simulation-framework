"""Boolean Property
=============================
Concrete property with boolean type.

Example:
    Creating the property::

        property = BooleanProperty(True)
"""


from gsf.core.entity.core.entity_property import EntityProperty
from gsf.core.entity.core.property_type import PropertyType


class BooleanProperty(EntityProperty):
    """Boolean property

    Defines a property with the boolean type.
    """


    def __init__(self, value: bool):
        super().__init__(value, PropertyType.BOOLEAN)

    def __bool__(self):
        return self.get_value()

    def __eq__(self, other):
        return other == self.get_value()

    def get_value(self) -> bool:
        """Returns the value of the property"""
        return super().get_value()
