from __future__ import annotations

from typing import Set


class Entity:
    """Unique component with an identification."""

    # identification of the entity.
    _id: str

    # static list of entities saved.
    _savedNames: Set[str] = ["DYNAMIC_SYSTEM_CALL"]

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
