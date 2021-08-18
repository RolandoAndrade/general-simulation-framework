from __future__ import annotations

from typing import TYPE_CHECKING

from core.entity.core.entity import Entity
from core.entity.core.entity_property import EntityProperties
from core.entity.properties.expression_property import ExpressionProperty

if TYPE_CHECKING:
    from models.core.base_model import BaseModel


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

    def get_properties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            "Weight": self._weight
        }

    def __init__(self, from_model: BaseModel, to_model: BaseModel, weight: ExpressionProperty, name: str = None):
        """
        Args:
            to (BaseModel): Destination model.
            weight (ExpressionProperty): Weight of the connection.
            name (str): Name of the path.
        """
        if name is None:
            super().__init__("model" + str(Path._serial_id))
            Path._serial_id = Path._serial_id + 1
        else:
            super().__init__(name)
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

    def __eq__(self, other):
        return self._to == other

    def __hash__(self):
        return hash(self._to)

    def __lt__(self, other):
        return self.get_weight() < other.get_weight()
