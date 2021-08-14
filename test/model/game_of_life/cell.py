from __future__ import annotations
from typing import Dict

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from models.models.discrete_event_model import (
    DiscreteEventModel,
)
from models.core.base_model import ModelState


class Cell(DiscreteEventModel):
    ALIVE = True
    DEAD = False

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        i: int,
        j: int,
        state: bool = DEAD,
    ):
        super().__init__(dynamic_system, str(i) + "," + str(j))
        self.set_up_state(state)

    def _output_function(self, state: bool) -> bool:
        return state

    def _internal_state_transition_function(self, state: bool) -> bool:
        return state

    def _external_state_transition_function(
        self, state: bool, inputs: Dict[str, bool], event_time: float
    ) -> ModelState:
        values = inputs.values()
        count = 0
        for v in values:
            if v:
                count = count + 1
        return (not state and count == 3) or (state and 2 <= count <= 3)

    def _time_advance_function(self, state: ModelState) -> float:
        return 1

    def __str__(self):
        if self.get_state():
            return "\u2665"
        else:
            return "-"
