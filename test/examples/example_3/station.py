from typing import TypedDict, Dict

from gsf.core.entity.core import EntityProperties
from gsf.core.expressions import Expression
from gsf.core.types import Time
from gsf.dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from gsf.models.models import DiscreteEventModel


class StationState(TypedDict):
    """State definition of the station"""

    parts: int
    remaining_time: Time


class Station(DiscreteEventModel):
    """Station of the simulator

    It processes the inputs that receives. Its state has the number of parts that currently are inside the
    station and the remaining time to finish to process one of that parts.

    Attributes:
        _processing_time(Expression): time to process one part.
    """

    _processing_time: Expression

    def __init__(
        self, dynamic_system: DiscreteEventDynamicSystem, processing_time: Expression
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): factory where stations belongs.
            processing_time (Expression): time to process one part.
        """
        super().__init__(dynamic_system, state={"parts": 0, "remaining_time": -1})
        self._processing_time = processing_time

    def _internal_state_transition_function(self, state: StationState) -> StationState:
        """Removes one part from processing, and schedules and event to process a new one."""
        state["parts"] = max(state["parts"] - 1, 0)
        self.schedule(self.get_time())
        return state

    def _external_state_transition_function(
        self, state: StationState, inputs: Dict[str, int], event_time: Time
    ) -> StationState:
        """Removes one part from processing, and schedules and event to process a new one."""
        values = inputs.values()
        state["remaining_time"] = state["remaining_time"] - event_time
        for number_of_parts in values:
            if state["parts"] > 0:
                state["parts"] = state["parts"] + number_of_parts
            elif state["parts"] == 0:
                state["parts"] = number_of_parts
                self.schedule(self.get_time())
        return state

    def _time_advance_function(self, state: StationState) -> Time:
        """Obtains the time of the next processed entity."""
        if state["parts"] < 1:
            state["remaining_time"] = Time(-1)
        else:
            state["remaining_time"] = Time(self._processing_time.evaluate())
        return state["remaining_time"]

    def _output_function(self, state: StationState) -> int:
        """Returns a part."""
        if state["parts"] > 0:
            return 1
        return 0

    def __str__(self):
        return self.get_id()

    def get_properties(self) -> EntityProperties:
        pass
