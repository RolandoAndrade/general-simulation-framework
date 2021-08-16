from __future__ import annotations

from abc import abstractmethod
from typing import Set

from core.entity.core.entity_property import EntityProperties


class Entity:
    """Unique component with an identification."""

    _id: str
    """Identification of the entity."""

    _saved_names: Set[str] = ["DYNAMIC_SYSTEM_CALL"]
    """Static list of entities saved."""

    def __init__(self, name: str):
        self.set_id(name)

    def set_id(self, name: str):
        """Sets the identifier of the entity.

        Args:
            name (str): Identifier of the entity.
        """
        if name in Entity._saved_names:
            raise Exception("Name already taken by another entity")
        else:
            self._id = name

    def get_id(self) -> str:
        """Gets the identifier of the entity."""
        return self._id

    @property
    @abstractmethod
    def properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        raise NotImplementedError
