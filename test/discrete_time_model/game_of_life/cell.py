from __future__ import annotations

from typing import Dict

from dynamic_system.models.discrete_time_model import DiscreteTimeModel
from dynamic_system.models.dynamic_system import DynamicSystem


class Cell(DiscreteTimeModel):
    ALIVE = True
    DEAD = False

    def __init__(self, dynamic_system: DynamicSystem, i: int, j: int, state: bool = DEAD):
        super().__init__(dynamic_system, str(i) + "," + str(j))
        self.setUpState(state)

    def stateTransitionFunction(self, state: bool, inputs: Dict[str, bool]) -> bool:
        values = inputs.values()
        count = 0
        for v in values:
            if v:
                count = count + 1
        if (not state and count == 3) or (state and 2 <= count <= 3):
            return True
        return False

    def outputFunction(self, state: bool) -> bool:
        return state

    def __str__(self):
        if self._currentState:
            return "\u2665"
        else:
            return "-"
