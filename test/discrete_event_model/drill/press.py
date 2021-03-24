from typing import Any, Dict

from dynamic_system.models.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from dynamic_system.models.discrete_event_model import DiscreteEventModel


class Press(DiscreteEventModel):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
        super().__init__(dynamic_system, state={
            "p": 0,
            "s": 0
        }, name="Press")

    def internalStateTransitionFunction(self, state: Dict[str, float]) -> Dict[str, float]:
        state["p"] = max(state["p"] - 1, 0)
        state["s"] = 1 * min(state["p"], 1)
        return state

    def externalStateTransitionFunction(self, state: Dict[str, float], parts: int, event_time: float) -> \
            Dict[str, float]:
        if state["p"] > 0:
            state["p"] = state["p"] + parts
            state["s"] = state["s"] - event_time
        elif state["p"] is 0:
            state["p"] = parts
            state["s"] = 1
            self._currentDynamicSystem.schedule(self, 1)
        return state

    def timeAdvanceFunction(self, state: Dict[str, float]) -> float:
        return state["s"]

    def outputFunction(self, state: Dict[str, float]) -> int:
        if state["p"] > 0:
            return 1
        return 0


    def __str__(self):
        return "Press -> s" + str(self._currentState)
