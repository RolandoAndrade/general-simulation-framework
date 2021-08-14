from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, List, Set

from core.debug.domain.debug import debug
from core.debug.infrastructure.providers import TableProvider
from dynamic_system.future_event_list.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from models.models.discrete_event_model import (
        DiscreteEventModel,
    )


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event
    models
    """

    _future_event_list: List[ScheduledModel]

    def __init__(self):
        self._future_event_list = []

    @debug("Scheduling model")
    def schedule(self, model: DiscreteEventModel, time: float):
        """Schedule an event at the specified time
        Args:
            model (DiscreteEventModel): DiscreteEventModel with an autonomous event scheduled
            time (float): Time to execute an autonomous event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
            if sm not in self._future_event_list:
                heapq.heappush(self._future_event_list, sm)

    @debug("Getting time of next event")
    def get_time_of_next_event(self) -> float:
        """Gets the time of the next event"""
        if len(self._future_event_list) > 0:
            return self._future_event_list[0].get_time()
        return 0

    @debug("Updating time")
    def update_time(self, delta_time: float):
        """Updates the time of the events

        Args:
            delta_time (float): Time that has passed since the last update
        """
        for i in range(len(self._future_event_list)):
            self._future_event_list[i].decrease_time(delta_time)

    @debug("Getting next models")
    def get_next_models(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event"""
        s = set()
        fel = self._future_event_list.copy()
        time = self.get_time_of_next_event()
        while len(fel) > 0 and fel[0].get_time() == time:
            s.add(heapq.heappop(fel).get_model())
        return s

    @debug("Removing models from the heap")
    def pop_next_models(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event and
        removes it from the heap
        """
        s = set()
        time = self.get_time_of_next_event()
        while (
                len(self._future_event_list) > 0
                and self._future_event_list[0].get_time() == time
        ):
            s.add(heapq.heappop(self._future_event_list).get_model())
        return s

    @debug("Getting future event list")
    def get_future_event_list(self) -> List[ScheduledModel]:
        """Returns the future event list"""
        return self._future_event_list

    def __str__(self):
        x = TableProvider()
        x.set_title("Future Event List (FEL)").set_labels(
            ["Model ID", "Priority", "Time"]
        )
        x.set_alignment(["l", "r", "r"])
        priority = 0
        last_time = 0
        if len(self._future_event_list) > 0:
            for event in self._future_event_list:
                if last_time != event.get_time():
                    priority = priority + 1
                x.add_row([event.get_model().get_id(), priority, str(event.get_time())])
                last_time = event.get_time()
        return x.build()
