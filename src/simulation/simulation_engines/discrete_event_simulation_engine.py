from __future__ import annotations

from typing import TYPE_CHECKING, Dict


from reports.core.base_report import BaseReport
from simulation.core.base_simulator import BaseSimulator

if TYPE_CHECKING:
    from core.types import DynamicSystemInput
    from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
        DiscreteEventDynamicSystem,
)


class DiscreteEventSimulationEngine(BaseSimulator):
    """Simulation engine for discrete-event simulation"""

    _dynamic_system: DiscreteEventDynamicSystem
    _last_event_time: int
    _is_output_up_to_update: bool

    def __init__(
        self, dynamic_system: DiscreteEventDynamicSystem, base_generator: BaseReport
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem):
        """
        super().__init__(dynamic_system, base_generator)
        self._dynamic_system = dynamic_system
        self._last_event_time = 0
        self._is_output_up_to_update = False

    def get_time_of_next_event(self) -> int:
        """Get time of the next event"""
        return self._dynamic_system.get_time_of_next_events()

    def compute_next_state(self, inputs: DynamicSystemInput = None, time: int = 0):
        """Compute the next state of the dynamic system

        Args:
            inputs: Input for the dynamic system
            time (float): time of the event.
        """
        if (
            time - self._last_event_time is self.get_time_of_next_event()
        ):  # Time to change the output
            out = self.compute_output()
            if out:
                self._report_generator.add_output(out, time)
        self._dynamic_system.state_transition(inputs, time - self._last_event_time)
        self._last_event_time = time
        self._is_output_up_to_update = False

    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        if not self._is_output_up_to_update:
            self._is_output_up_to_update = True
            return self._dynamic_system.get_output()
        return None
