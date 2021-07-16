from typing import Any

from core.components.entity.core.entity_property import EntityProperties
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput


class Server(DiscreteEventModel):
    """Server of processes"""

    def _internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        pass

    def _externalStateTransitionFunction(self, state: ModelState, inputs: ModelInput, event_time: float) -> ModelState:
        pass

    def _timeAdvanceFunction(self, state: ModelState) -> float:
        pass

    def _outputFunction(self, state: ModelState) -> Any:
        pass

    def getProperties(self) -> EntityProperties:
        pass
