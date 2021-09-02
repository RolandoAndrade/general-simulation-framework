from __future__ import annotations

from typing import TYPE_CHECKING

from core.entity.core.entity import Entity
from core.entity.core.entity_property import EntityProperties
from core.entity.properties.expression_property import ExpressionProperty

if TYPE_CHECKING:
    from models.core.base_model import BaseModel
    from core.entity.core import EntityManager


class Path(Entity):
    """Connection between models."""

    _serial_id = 0
    """Serial of the path"""

    _from: BaseModel
    """Final model."""

    _to: BaseModel
    """Final model."""

    _weight: ExpressionProperty
    """Weight of the path"""

    def __init__(
        self,
        from_model: BaseModel,
        to_model: BaseModel,
        weight: ExpressionProperty,
        name: str = None,
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            from_model (BaseModel): Source model of the path.
            to_model (BaseModel): Destination model of the path.
            weight (ExpressionProperty): Weight of the connection.
            name (str): Name of the path.
        """
        if name is None:
            super().__init__("path" + str(Path._serial_id), entity_manager)
            Path._serial_id = Path._serial_id + 1
        else:
            super().__init__(name, entity_manager)
        self._from = from_model
        self._to = to_model
        self._weight = weight

    def get_source_model(self) -> BaseModel:
        """Return the source model"""
        return self._from

    def get_destination_model(self) -> BaseModel:
        """Return the destination model"""
        return self._to

    def get_weight(self) -> float:
        """Return the evaluation of the weight."""
        return self._weight.get_value().evaluate()

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {"Weight": self._weight}

    def set_weight(self, weight: ExpressionProperty):
        """Sets the weight of the path

        Args:
            weight (ExpressionProperty): Weight of the path.
        """
        self._weight = weight

    def __eq__(self, other):
        """Checks if the path is equal or contains the given model.

        Args:
            other: Other model or path.
        """
        if isinstance(other, Path):
            return super().__eq__(other)
        return self._to == other or self._from == other

    def __hash__(self):
        return hash(str(self))
