from __future__ import annotations

from typing import TYPE_CHECKING

from core.events.event_bus import event_bus
from dynamic_system.events.compute_output_event import ComputeOutputEvent
from dynamic_system.events.external_state_transition_event import ExternalStateTransitionEvent


if TYPE_CHECKING:
    from dynamic_system.control.scheduler import Scheduler


class SimulationEngine:
    _scheduler: Scheduler
    _is_output_up_to_date: bool
    _time_of_last_event: float

    def __init__(self, scheduler: Scheduler):
        self._scheduler = scheduler

    def compute_next_state(self, time: float, is_external=True):
        """Computes the next state with external, internal or confluent state transition function

        :param time: Time of the event
        :param is_external: Is an external event
        """
        if time < self._scheduler.next_event_time() and is_external:  # If this is an external event
            event_bus.emit(ExternalStateTransitionEvent(time - self._time_of_last_event))
        elif time == self._scheduler.next_event_time():  # Confluent with autonomous action
            self.compute_output()  # Compute the output at the time
            model = self._scheduler.get_minimum()
            if is_external:
                model.confluent_transition()
            else:
                model.internal_transition()

        self._time_of_last_event = time
        self._is_output_up_to_date = False

    def execute_next_event(self):
        """Computes the output and next state of the model at the next event time"""
        self.compute_next_state(self._scheduler.next_event_time(), False)

    def compute_output(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if not self._is_output_up_to_date:
            self._is_output_up_to_date = True
            event_bus.emit(ComputeOutputEvent)
