from __future__ import annotations

from typing import Dict, TypeVar, Generic

from core.components.entity.core.property_type import PropertyType

T = TypeVar('T')


class EntityProperty(Generic[T]):
    """Property of an entity"""

    __value: T
    """Property value"""

    __type: str
    """Property type"""

    def __init__(self,
                 value: T = None,
                 property_type: str = PropertyType.STRING):
        self.__value = value
        self.__type = property_type

    def getType(self) -> str:
        """Returns the name of the property"""
        return self.__type

    def getValue(self) -> T:
        """Returns the value of the property"""
        return self.__value

    def setValue(self, value: T):
        """Sets the value of the property"""
        if value is not None and not PropertyType.validate(value, self.getType()):
            raise Exception("Expected " + self.getType() + "typing, but received " + type(value))
        self.__value = value


EntityProperties = Dict[str, EntityProperty]
"""Group of properties of an entity"""
