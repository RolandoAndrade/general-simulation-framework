from typing import Any

from core.entity.core import EntityProperties
from core.types import Time
from core.types.model_input import ModelInput
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class ModelMock(DiscreteEventModel):
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        pass

    def _external_state_transition_function(self, state: ModelState, inputs: ModelInput,
                                            event_time: Time) -> ModelState:
        pass

    def _time_advance_function(self, state: ModelState) -> Time:
        pass

    def _output_function(self, state: ModelState) -> Any:
        pass

    def get_properties(self) -> EntityProperties:
        pass