from typing import Any, List

from gsf.core.entity.core import EntityProperties
from gsf.core.types import Time
from gsf.core.types.model_input import ModelInput
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.core import ModelState
from gsf.models.models import DiscreteEventModel


class Generator(DiscreteEventModel):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, pieces: List[int]):
        super().__init__(dynamic_system, name="Generator", state=pieces)
        self.schedule(Time(0))

    def _internal_state_transition_function(self, state: List[int]) -> ModelState:
        state.pop(0)
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(
        self, state: ModelState, inputs: ModelInput, event_time: Time
    ) -> ModelState:
        return state

    def _time_advance_function(self, state: List[int]) -> Time:
        return Time(1) if len(state) > 0 else Time(-1)

    def _output_function(self, state: List[int]) -> Any:
        return state[0]

    def get_properties(self) -> EntityProperties:
        return {}

    def __str__(self):
        return self.get_id()
