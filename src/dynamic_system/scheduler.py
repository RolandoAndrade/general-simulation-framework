import heapq

from typing import TYPE_CHECKING, List
from dynamic_system.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from dynamic_system.model import Model


class Scheduler:
    _schedule: List[ScheduledModel]

    def __init__(self):
        self._schedule = []

    def schedule(self, model: Model, time: float):
        sm = ScheduledModel(model, time)
        heapq.heappush(self._schedule, sm)

    def next_time(self):
        return self._schedule[0].get_time()

    def update_time(self, time: float):
        for i in range(len(self._schedule)):
            self._schedule[i].decrease_time(time)

    def get_minimum(self) -> Model:
        if len(self._schedule) > 0:
            return heapq.heappop(self._schedule).get_model()