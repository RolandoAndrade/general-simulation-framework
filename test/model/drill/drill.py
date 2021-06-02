from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)

from dynamic_system.models.discrete_event_model import (
    DiscreteEventModel,
)

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_model import (
        ModelState,
        ModelInput,
    )


class Drill(DiscreteEventModel):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str):
        super().__init__(dynamic_system, state={"p": 0, "s": 0}, name=name)

    def internalStateTransitionFunction(self, state: Dict[str, float]) -> ModelState:
        state["p"] = max(state["p"] - 1, 0)
        state["s"] = 2 * min(state["p"], 1)
        return state

    def externalStateTransitionFunction(
        self, state: Dict[str, float], parts: ModelInput, event_time: float
    ) -> ModelState:
        values = parts.values()
        state["s"] = state["s"] - event_time
        for part in values:
            if state["p"] > 0:
                state["p"] = state["p"] + part
            elif state["p"] == 0:
                state["p"] = part
                state["s"] = 2
                self._currentDynamicSystem.schedule(self, 2)
        return state

    def timeAdvanceFunction(self, state: ModelState) -> float:
        return state["s"]

    def outputFunction(self, state: ModelState) -> int:
        if state["p"] > 0:
            return 1
        return 0
