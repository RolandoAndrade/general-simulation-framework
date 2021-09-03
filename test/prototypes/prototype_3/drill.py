from typing import Any

from core.entity.core import EntityProperties
from core.types import Time
from core.types.model_input import ModelInput
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class Drill(DiscreteEventModel):
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        state["p"] = max(state["p"] - 1, 0)
        state["s"] = 2 * min(state["p"], 1)
        self.schedule(Time(state["s"]))
        return state

    def _external_state_transition_function(self, state: ModelState, inputs: ModelInput,
                                            event_time: Time) -> ModelState:
        values = inputs.values()
        state["s"] = state["s"] - event_time
        for part in values:
            if state["p"] > 0:
                state["p"] = state["p"] + part
            elif state["p"] == 0:
                state["p"] = part
                state["s"] = 2
                self.schedule(Time(2))
        return state

    def _time_advance_function(self, state: ModelState) -> Time:
        return state["s"]

    def _output_function(self, state: ModelState) -> Any:
        if state["p"] > 0:
            return 1
        return 0

    def get_properties(self) -> EntityProperties:
        pass

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, name: str):
        super().__init__(dynamic_system, state={
            "p": 0,
            "s": 0
        }, name=name)

    def __str__(self):
        return self.get_id() + " -> s" + str(self.get_state)
