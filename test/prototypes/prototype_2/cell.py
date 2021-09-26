from typing import Dict

from gsf.core.entity.core import EntityProperties
from gsf.core.types import Time
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.models import DiscreteEventModel


class Cell(DiscreteEventModel):
    def __init__(
        self, alive: bool, dynamic_system: DiscreteEventDynamicSystem, i: int, j: int
    ):
        super().__init__(
            dynamic_system, name="(" + str(i) + "," + str(j) + ")", state=alive
        )
        self.schedule(self.get_time())

    def _internal_state_transition_function(self, state: bool) -> bool:
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(
        self, state: bool, inputs: Dict[str, bool], event_time: Time
    ) -> bool:
        values = inputs.values()
        count = 0
        for v in values:
            if v:
                count = count + 1
        if (not state and count == 3) or (state and 2 <= count <= 3):
            return True
        return False

    def _time_advance_function(self, state: Dict[str, bool]) -> Time:
        return Time(1)

    def _output_function(self, state: bool) -> bool:
        return state

    def get_properties(self) -> EntityProperties:
        return {}

    def __str__(self):
        if self.get_state():
            return "\u2665"
        return "-"
