"""Entity Property
=============================
This module contains the definition of the generic property.
It has the definition of the EntityProperty that allows to define the properties of an entity with
a value, type and category.

Example:
    Creating properties::

        number_property = EntityProperty(0, PropertyType.NUMBER, "Category 1")
        string_property = EntityProperty("0", PropertyType.STRING, "Category 1")
        boolean_property = EntityProperty(True, PropertyType.BOOLEAN, "Category 2")
"""

from __future__ import annotations

from typing import Dict, TypeVar, Generic

from gsf.core.entity.core.property_type import PropertyType

T = TypeVar("T")


class EntityProperty(Generic[T]):
    """Property of an entity

    Contains a value, type and category to describe an entity,

    Attributes:
        __value (T): Property value
        __type (str): Property type
        __category (str): Property category
    """

    __value: T
    """Property value"""

    __type: str
    """Property type"""

    __category: str
    """Property category"""

    def __init__(
        self,
        value: T = None,
        property_type: str = PropertyType.STRING,
        category: str = "Generic",
    ):
        self.__value = value
        self.__type = property_type
        self.__category = category

    def get_type(self) -> str:
        """Returns the name of the property"""
        return self.__type

    def get_category(self) -> str:
        """Returns the category of the property"""
        return self.__category

    def get_value(self) -> T:
        """Returns the value of the property"""
        return self.__value

    def set_value(self, value: T):
        """Sets the value of the property"""
        if value is not None and not PropertyType.validate(value, self.get_type()):
            raise Exception(
                "Expected "
                + self.get_type()
                + "typing, but received "
                + str(type(value))
            )
        self.__value = value


EntityProperties = Dict[str, EntityProperty]
"""Group of properties of an entity"""
