from __future__ import annotations

from abc import abstractmethod

from core.debug.domain.debug import debug

from typing import Any, TYPE_CHECKING, Dict, Set

DynamicSystemOutput = Dict[str, Any]

if TYPE_CHECKING:
    from models.models.discrete_event_model import BaseModel

    DynamicSystemModels = Set[BaseModel]


class BaseDynamicSystem:
    _models: DynamicSystemModels
    """Models of the dynamic system"""

    def __init__(self):
        self._models = set()

    @debug("Adding model to the dynamic system")
    def add(self, model: BaseModel):
        """Adds a model to the dynamic system.

        Args:
            model (BaseModel): Model to be added.
        """
        if model.get_dynamic_system() != self:
            raise Exception("Invalid dynamic system")
        self._models.add(model)

    @debug("Removing model of the dynamic system")
    def remove(self, model: BaseModel):
        """Removes a model of the dynamic system.

        Args:
            model (BaseModel): Model to be removed.
        """
        if model in self._models:
            self._models.remove(model)
        else:
            raise Exception("Model not found")

    @abstractmethod
    def get_output(self) -> DynamicSystemOutput:
        raise NotImplementedError

    @abstractmethod
    def state_transition(self, *args, **kwargs) -> DynamicSystemOutput:
        raise NotImplementedError
