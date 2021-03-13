from __future__ import annotations
from dynamic_system.models.discrete_time_model import DiscreteTimeModel
from dynamic_system.models.discrete_event_dynamic_system import DynamicSystem


class Cell(DiscreteTimeModel):
    ALIVE = True
    DEAD = False

    def __init__(self, dynamic_system: DynamicSystem, state: bool = DEAD):
        super().__init__(dynamic_system)
        self.setUpState(state)

    def stateTransitionFunction(self, state: bool, inputs: bool) -> bool:
        return inputs

    def outputFunction(self, state: bool) -> bool:
        return state

    def __str__(self):
        if self._currentState:
            return "*"
        else:
            return "0"
