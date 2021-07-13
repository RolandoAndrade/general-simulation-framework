from __future__ import annotations

from typing import Any, Dict

from core.components.entity.property_type import PropertyType


class EntityProperty:
    """Property of an entity"""

    __value: Any
    """Property value"""

    __type: str
    """Property type"""

    def __init__(self,
                 value: Any = None,
                 property_type: str = PropertyType.STRING):
        self.__value = value
        self.__type = property_type

    def getType(self) -> str:
        """Returns the name of the property"""
        return self.__type

    def getValue(self) -> Any:
        """Returns the value of the property"""
        return self.__value

    def setValue(self, value: Any):
        """Sets the value of the property"""
        if value is not None and not PropertyType.validate(value, self.getType()):
            raise Exception("Expected " + self.getType() + "typing, but received " + type(value))
        self.__value = value


EntityProperties = Dict[str, EntityProperty]
"""Group of properties of an entity"""
