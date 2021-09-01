from typing import Dict

from core.entity.core import EntityProperties
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class Cell(DiscreteEventModel):
    def __init__(self, alive: bool, dynamic_system: DiscreteEventDynamicSystem, i: int, j: int):
        super().__init__(dynamic_system, name="(" + str(i) + "," + str(j) + ")", state=alive)
        self.schedule(self.get_time())

    def _internal_state_transition_function(self, state: bool) -> bool:
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(self, state: bool, inputs: Dict[str, bool],
                                            event_time: Time) -> bool:
        values = inputs.values()
        count = 0
        for v in values:
            if v:
                count = count + 1
        if (not state and count == 3) or (state and 2 <= count <= 3):
            return True
        return False

    def _time_advance_function(self, state: ModelState) -> Time:
        return Time(1)

    def _output_function(self, state: bool) -> bool:
        return state

    def get_properties(self) -> EntityProperties:
        return {

        }

    def __str__(self):
        if self.get_state():
            return "\u2665"
        else:
            return "-"