from core.entity.core import EntityProperties
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class Cell(DiscreteEventModel):
    def __init__(self, alive: bool):
        super().__init__(DiscreteEventDynamicSystem(), state=alive)

    def _internal_state_transition_function(self, state: bool) -> bool:
        return state

    def _external_state_transition_function(self, state: bool, inputs: ModelInput,
                                            event_time: Time) -> bool:
        next_state: bool = list(inputs.values())[0]
        return next_state

    def _time_advance_function(self, state: ModelState) -> Time:
        return Time(1)

    def _output_function(self, state: bool) -> bool:
        return state

    def get_properties(self) -> EntityProperties:
        return {

        }