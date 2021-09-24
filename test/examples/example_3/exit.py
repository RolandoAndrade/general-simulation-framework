from typing import Any, Dict

from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class Exit(DiscreteEventModel):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
        super().__init__(dynamic_system, state=0)

    def _external_state_transition_function(self, state: int, inputs: Dict[str, int],
                                            event_time: Time) -> int:
        return state + sum(inputs.values())

    def _time_advance_function(self, state: ModelState) -> Time:
        return Time(-1)

    def _output_function(self, state: ModelState) -> int:
        return state

    def __str__(self):
        return "Exit"
