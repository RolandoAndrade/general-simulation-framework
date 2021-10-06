"""Entity
=============================
This module contains the definition of entities.
It has the abstract definition of Entity. Entities are elements with identity and properties.

Example:
    Creating an entity::

        class Model(Entity):
            _count: NumberProperty

            def __init__(self, name: str):
                super().__init__(name)
                self._count = NumberProperty(0)

            def get_properties(self) -> EntityProperties:
                return {
                    'count': self._count
                }
"""


from __future__ import annotations

from abc import abstractmethod

from gsf.core.entity.core import EntityManager, static_entity_manager
from gsf.core.entity.core.entity_property import EntityProperties


class Entity:
    """Entity

    Unique component with an identification.

    Attributes:
        _id (str): Identifier of the entity.
        _entity_manager (EntityManager): Delegated entity manager.
    """

    _id: str
    """Identification of the entity."""

    _entity_manager: EntityManager
    """Manager of the names of entities."""

    def __init__(self, name: str, entity_manager: EntityManager = None):
        """
        Args:
            name (str): Identifier of the entity.
            entity_manager (EntityManager): Delegated entity manager.
        """
        self._id = None
        self._entity_manager = entity_manager or static_entity_manager
        self.set_id(name)

    def set_id(self, name: str):
        """Sets the identifier of the entity.

        Args:
            name (str): Identifier of the entity.
        """
        if self._entity_manager.name_already_exists(name):
            raise NameError("Name already taken by another entity")
        self._entity_manager.replace_name(name, self.get_id())
        self._id = name

    def get_id(self) -> str:
        """Gets the identifier of the entity."""
        return self._id

    @abstractmethod
    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        raise NotImplementedError
