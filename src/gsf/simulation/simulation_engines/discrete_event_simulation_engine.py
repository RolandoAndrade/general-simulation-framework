from __future__ import annotations

from typing import TYPE_CHECKING

from gsf.core.events import EventBus
from gsf.reports.core.base_report import BaseReport
from gsf.simulation.core.base_simulator import BaseSimulator
from gsf.core.types import Time

if TYPE_CHECKING:
    from gsf.core.types import DynamicSystemInput
    from gsf.dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
        DiscreteEventDynamicSystem,
    )


class DiscreteEventSimulationEngine(BaseSimulator):
    """Simulation engine for discrete-event simulation"""

    _dynamic_system: DiscreteEventDynamicSystem
    """Dynamic system to be simulated."""

    _last_event_time: Time
    """Time of the last event recorded."""

    _is_output_up_to_update: bool
    """Indicates if the output was already computed for the current iteration."""

    def __init__(
        self,
        dynamic_system: DiscreteEventDynamicSystem,
        base_generator: BaseReport,
        event_bus: EventBus = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system to be simulated.
            base_generator (BaseReport): Report generator for saving the outputs.
        """
        super().__init__(dynamic_system, base_generator, event_bus)
        self._dynamic_system = dynamic_system
        self.init()

    def get_time_of_next_event(self) -> Time:
        """Get time of the next event"""
        return self._dynamic_system.get_time_of_next_events()

    def compute_next_state(
        self, inputs: DynamicSystemInput = None, time: Time = Time(0)
    ):
        """Compute the next state of the dynamic system

        Args:
            inputs (DynamicSystemInput): Input for the dynamic system.
            time (Time): Time of the event.
        """
        if (
            time - self._last_event_time - self.get_time_of_next_event() == 0
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

    def init(self):
        super(DiscreteEventSimulationEngine, self).init()
        self._last_event_time = Time(0)
