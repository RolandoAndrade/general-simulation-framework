from typing import Any, Dict

from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models import DiscreteEventModel


class Exit(DiscreteEventModel):
    """Exit

    Sink of a factory. Here come all the processed part of the factory.
    """

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
        """Args:
            dynamic_system(DiscreteEventDynamicSystem): factory where stations belongs.
        """
        super().__init__(dynamic_system, state=0)

    def _external_state_transition_function(self, state: int, inputs: Dict[str, int],
                                            event_time: Time) -> int:
        """Receives the parts"""
        return state + sum(inputs.values())

    def _time_advance_function(self, state: ModelState) -> Time:
        """Prevents to execute an autonomous event"""
        return Time(-1)

    def _output_function(self, state: ModelState) -> int:
        """Returns the number of parts processed."""
        return state

    def __str__(self):
        return "Exit"
