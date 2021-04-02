from __future__ import annotations

from typing import TYPE_CHECKING

from core.events.event_bus import event_bus
from dynamic_system.events.compute_output_event import ComputeOutputEvent
from dynamic_system.events.external_state_transition_event import ExternalStateTransitionEvent

if TYPE_CHECKING:
    from dynamic_system.control.scheduler import Scheduler


class SimulationEngine:
    _scheduler: Scheduler
    _isOutputUpToDate: bool
    _timeOfLastEvent: float

    def __init__(self, scheduler: Scheduler):
        self._scheduler = scheduler

    def computeNextState(self, time: float, is_external=True):
        """Computes the next state with external, internal or confluent state transition function

        :param time: Time of the event
        :param is_external: Is an external event
        """
        if time < self._scheduler.getTimeOfNextEvent() and is_external:  # If this is an external event
            event_bus.emit(ExternalStateTransitionEvent(time - self._timeOfLastEvent))
        elif time == self._scheduler.getTimeOfNextEvent():  # Confluent with autonomous action
            self.computeOutput()  # Compute the output at the time
            model = self._scheduler.getNextModels()
            if is_external:
                model.confluentTransition()
            else:
                model.internalTransition()

        self._timeOfLastEvent = time
        self._isOutputUpToDate = False

    def executeNextEvent(self):
        """Computes the output and next state of the model at the next event time"""
        self.computeNextState(self._scheduler.getTimeOfNextEvent(), False)

    def computeOutput(self):
        """Invokes the model's output function and inform to listeners of the consequent
        output values; it does not change the state of the model"""
        if not self._isOutputUpToDate:
            self._isOutputUpToDate = True
            event_bus.emit(ComputeOutputEvent)
