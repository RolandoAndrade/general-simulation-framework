from __future__ import annotations
from core.debug.domain.debug import debug

from typing import Any, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_model import BaseModel


class BaseDynamicSystem:
    @debug("Adding model to the dynamic system")
    def add(self, model: BaseModel):
        """Adds a model to the dynamic system.

        Args:
            model (DiscreteEventModel): Model to be added.
        """
        if model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")
        self._models[model.getID()] = model
