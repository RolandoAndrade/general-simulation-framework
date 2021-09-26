from typing import Any

from gsf.core.entity.core import EntityProperties
from gsf.core.types import Time
from gsf.core.types.model_input import ModelInput
from gsf.models.core import ModelState
from gsf.models.models import DiscreteEventModel


class ModelMock(DiscreteEventModel):
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        raise NotImplementedError()

    def _external_state_transition_function(
        self, state: ModelState, inputs: ModelInput, event_time: Time
    ) -> ModelState:
        raise NotImplementedError()

    def _time_advance_function(self, state: ModelState) -> Time:
        raise NotImplementedError()

    def _output_function(self, state: ModelState) -> Any:
        return 1

    def get_properties(self) -> EntityProperties:
        raise NotImplementedError()
