from dynamic_system.models.dynamic_system import DynamicSystem
from dynamic_system.models.model import Model, ModelState, ModelInput


class Press(Model):
    def __init__(self, dynamic_system: DynamicSystem, name: str):
        super().__init__(dynamic_system, state={
            "p": 0,
            "s": 0
        }, name=name)

    def internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        state["p"] = max(state["p"] - 1, 0)
        state["s"] = 1 * min(state["p"], 1)
        return state

    def externalStateTransitionFunction(self, state: ModelState, parts: ModelInput, event_time: float) -> ModelState:
        values = parts.values()
        state["s"] = state["s"] - event_time
        for part in values:
            if state["p"] > 0:
                state["p"] = state["p"] + part
            elif state["p"] is 0:
                state["p"] = part
                state["s"] = 1
                self._currentDynamicSystem.schedule(self, 1)
        return state

    def timeAdvanceFunction(self, state: ModelState) -> float:
        return state["s"]

    def outputFunction(self, state: ModelState) -> int:
        if state["p"] > 0:
            return 1
        return 0


    def __str__(self):
        return self.getID() + " -> s" + str(self._currentState)