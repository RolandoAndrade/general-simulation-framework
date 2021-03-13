from __future__ import annotations
import heapq

from typing import TYPE_CHECKING, List
from dynamic_system.models.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from dynamic_system.models.state_model import StateModel


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event models"""
    _schedule: List[ScheduledModel]

    def __init__(self):
        self._schedule = []

    def schedule(self, model: StateModel, time: float):
        """Schedule an event at the specified time
        :param model Model with an autonomous event scheduled
        :param time Time to execute event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
            heapq.heappush(self._schedule, sm)

    def getTimeOfNextEvent(self) -> float:
        """Get time of the next event"""
        return self._schedule[0].getTime()

    def updateTime(self, delta_time: float):
        """Update the time of the events
        :param delta_time Time that has passed since the last update"""
        for i in range(len(self._schedule)):
            self._schedule[i].decreaseTime(delta_time)

    def getNextModel(self) -> Model:
        """Get the next model that will execute an autonomous event"""
        if len(self._schedule) > 0:
            return heapq.heappop(self._schedule).getModel()


static_scheduler = Scheduler()
