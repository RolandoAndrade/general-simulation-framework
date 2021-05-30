from __future__ import annotations
from typing import Dict

from dynamic_system.discrete_events.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from dynamic_system.discrete_events.models.discrete_event_model import (
    DiscreteEventModel,
    ModelState,
)


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
        self.setUpState(state)

    def outputFunction(self, state: bool) -> bool:
        return state

    def internalStateTransitionFunction(self, state: bool) -> bool:
        return state

    def externalStateTransitionFunction(
        self, state: bool, inputs: Dict[str, bool], event_time: float
    ) -> ModelState:
        values = inputs.values()
        count = 0
        for v in values:
            if v:
                count = count + 1
        return (not state and count == 3) or (state and 2 <= count <= 3)

    def timeAdvanceFunction(self, state: ModelState) -> float:
        return 1

    def __str__(self):
        if self._currentState:
            return "\u2665"
        else:
            return "-"
