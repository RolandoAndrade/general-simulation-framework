from __future__ import annotations

from abc import abstractmethod

from core.debug.domain.debug import debug

from typing import Any, Set, TYPE_CHECKING, Dict

DynamicSystemOutput = Dict[str, Any]

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_model import BaseModel

    DynamicSystemModels = Dict[str, BaseModel]


class BaseDynamicSystem:
    _models: DynamicSystemModels
    """Models of the dynamic system"""

    def __init__(self):
        self._models = {}

    @debug("Adding model to the dynamic system")
    def add(self, model: BaseModel):
        """Adds a model to the dynamic system.

        Args:
            model (BaseModel): Model to be added.
        """
        if model.getDynamicSystem() != self:
            raise Exception("Invalid dynamic system")
        self._models[model.getID()] = model

    @abstractmethod
    def getOutput(self) -> DynamicSystemOutput:
        raise NotImplementedError

    @abstractmethod
    def stateTransition(self, *args, **kwargs) -> DynamicSystemOutput:
        raise NotImplementedError
