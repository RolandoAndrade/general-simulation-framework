from __future__ import annotations

from typing import Any, TYPE_CHECKING

from core.components.entity.core.entity import Entity
from core.components.entity.core.entity_property import EntityProperties
from core.components.entity.properties.expression_property import ExpressionProperty

if TYPE_CHECKING:
    from models.core.base_model import BaseModel


class Path(Entity):
    """Connection between models."""
    _serial_id = 0
    """Serial of the path"""

    _to: BaseModel
    """Final model."""

    _weight: ExpressionProperty
    """Weight of the path"""

    def getProperties(self) -> EntityProperties:
        """Lists the properties of the entity"""
        return {
            "Weight": self._weight
        }

    def __init__(self, to: BaseModel, weight: ExpressionProperty, name: str = None):
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
        self._to = to
        self._weight = weight

    def getModel(self) -> BaseModel:
        """Return the destination model"""
        return self._to

    def getWeight(self) -> float:
        """Return the evaluation of the weight."""
        return self._weight.getValue().evaluate()

    def __eq__(self, other):
        return self._to == other

    def __hash__(self):
        return hash(self._to)

    def __lt__(self, other):
        return self.getWeight() < other.getWeight()
