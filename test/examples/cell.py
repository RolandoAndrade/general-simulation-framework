from typing import Any, Dict

from core.entity.core import EntityProperties
from core.entity.properties import StringProperty
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel


class Cell(DiscreteEventModel):
    ALIVE = True
    DEAD = False

    _symbol: StringProperty

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, state: bool, symbol: str = None):
        super().__init__(dynamic_system, state=state)
        self._symbol = StringProperty(symbol or "\u2665")
        self.schedule(self.get_time())

    def _internal_state_transition_function(self, state: bool) -> bool:
        return state

    def _external_state_transition_function(
            self, state: bool, inputs: Dict[str, bool], event_time: Time
    ) -> bool:
        next_state: bool = list(inputs.values())[0]
        return next_state

    def _time_advance_function(self, state: bool) -> Time:
        return Time(1)

    def _output_function(self, state: bool) -> bool:
        return state

    def get_properties(self) -> EntityProperties:
        return {
            "CellSymbol": self._symbol
        }

    def __str__(self):
        is_alive = self.get_state()
        if is_alive:
            return self._symbol
        else:
            return "-"
