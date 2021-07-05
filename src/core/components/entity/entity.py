from __future__ import annotations

from typing import Set, Dict, Any

from core.components.entity.entity_property import EntityProperties


class Entity:
    """Unique component with an identification."""

    _id: str
    """Identification of the entity."""

    _savedNames: Set[str] = ["DYNAMIC_SYSTEM_CALL"]
    """Static list of entities saved."""

    _properties: EntityProperties
    """Properties of the entity"""

    def __init__(self, name: str, properties=None):
        if properties is None:
            properties = {}
        self.setID(name)
        self.setProperties(properties)

    def setID(self, name: str):
        """Sets the identifier of the entity.

        Args:
            name (str): Identifier of the entity.
        """
        if name in Entity._savedNames:
            raise Exception("Name already taken by another entity")
        else:
            self._id = name

    def getID(self) -> str:
        """Gets the identifier of the entity."""
        return self._id

    def setProperties(self, properties: EntityProperties):
        """Sets properties of the entity.

        Args:
            properties (EntityProperties): Properties of the entity.
        """
        if properties is None:
            properties = {}
        self._properties = properties

    def getProperties(self) -> EntityProperties:
        """Gets the properties of the entity"""
        return self._properties

    def setProperty(self, property_name: str, value: Any):
        """Sets value of an entity property.

        Args:
            property_name (str): Name of the property
            value: Value of the property
        """
        self._properties[property_name] = value
