import heapq

from typing import TYPE_CHECKING, List
from dynamic_system.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from dynamic_system.model import Model


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event models"""
    _schedule: List[ScheduledModel]

    def __init__(self):
        self._schedule = []

    def schedule(self, model: Model, time: float):
        """Schedule an event at the specified time
        :param model Model with an autonomous event scheduled
        :param time Time to execute event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
            heapq.heappush(self._schedule, sm)

    def next_event_time(self) -> float:
        """Get time of the next event"""
        return self._schedule[0].get_time()

    def update_time(self, delta_time: float):
        """Update the time of the events
        :param delta_time Time that has passed since the last update"""
        for i in range(len(self._schedule)):
            self._schedule[i].decrease_time(delta_time)

    def get_minimum(self) -> Model:
        """Get the next model that will execute an autonomous event"""
        if len(self._schedule) > 0:
            return heapq.heappop(self._schedule).get_model()
