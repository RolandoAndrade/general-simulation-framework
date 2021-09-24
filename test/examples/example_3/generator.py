from typing import Any, List, Union

from core.expresions import Expression
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel

GeneratorState = Union[Expression, List[int]]


class Generator(DiscreteEventModel):
    """Generator of parts

    Creates parts given an interarrival time, and the number of pieces to create at that arrival

    Attributes:
        _interarrival_time (Expression): interarrival time of pieces.
    """
    _interarrival_time: Expression

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem, pieces: GeneratorState,
                 interarrival_time: Expression):
        """Args:
            dynamic_system(DiscreteEventDynamicSystem): factory where stations belongs.
            pieces(GeneratorState): number of pieces to create when there is an arrival.
            interarrival_time(Expression): interarrival time of pieces.
        """
        super().__init__(dynamic_system, state=pieces)
        self.schedule(Time(0))
        self._interarrival_time = interarrival_time

    def _internal_state_transition_function(
            self, state: GeneratorState) -> ModelState:
        """Generates a part"""
        if isinstance(state, list):
            state.pop(0)
        self.schedule(self.get_time())
        return state

    def _time_advance_function(self, state: GeneratorState) -> Time:
        """Calculates the time of the creation of next part"""
        if isinstance(state, list):
            return self._interarrival_time.evaluate() if len(state) > 0 else Time(-1)
        else:
            return self._interarrival_time.evaluate()

    def _output_function(self, state: GeneratorState):
        """Get the created part"""
        if isinstance(state, list):
            return state[0]
        else:
            return state.evaluate()

    def __str__(self):
        return "Generator"
