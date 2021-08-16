from __future__ import annotations

from typing import Any

from core.entity.core import EntityProperty, EntityProperties


class Label:
    """Label that indicates the value of a property"""
    __properties_source: EntityProperties
    """Source where the property should be retrieved."""

    __linked_property: str
    """Property to be observed"""

    def __init__(self, properties_source: EntityProperties, linked_property: str = None):
        """
        Args:
            properties_source (EntityProperties): Source where the property
                should be retrieved.
            linked_property (str): Property to be linked.
        """
        self.link(properties_source, linked_property)

    def link(self, properties_source: EntityProperties, linked_property: str = None):
        """Links the label to a property.

        Args:
            properties_source (EntityProperties): Source where the property
                should be retrieved.
            linked_property (str): Property to be linked.
        """
        self.__linked_property = linked_property
        self.__properties_source = properties_source

    def get_value(self) -> Any:
        """Gets the value of the property."""
        if self.__properties_source[self.__linked_property] is not None:
            if self.__properties_source[self.__linked_property] is not None:
                print("entro")
                print(self.__properties_source[self.__linked_property])
                return self.__properties_source[self.__linked_property].get_value()
        return 0
