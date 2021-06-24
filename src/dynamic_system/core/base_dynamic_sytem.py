from __future__ import annotations

from abc import abstractmethod

from core.debug.domain.debug import debug

from typing import Any, TYPE_CHECKING, Dict

DynamicSystemOutput = Dict[str, Any]

if TYPE_CHECKING:
    from models.models.discrete_event_model import BaseModel

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

    @debug("Removing model of the dynamic system")
    def remove(self, model: BaseModel):
        """Removes a model of the dynamic system.

        Args:
            model (BaseModel): Model to be removed.
        """
        if model.getID() in self._models:
            self._models.pop(model.getID())
            for m in self._models:
                # Removes the model from all the existing models
                self._models[m].remove(model)
        else:
            raise Exception("Model not found")

    @abstractmethod
    def getOutput(self) -> DynamicSystemOutput:
        raise NotImplementedError

    @abstractmethod
    def stateTransition(self, *args, **kwargs) -> DynamicSystemOutput:
        raise NotImplementedError
