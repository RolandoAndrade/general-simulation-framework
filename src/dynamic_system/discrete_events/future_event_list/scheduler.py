from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, List, Set


from dynamic_system.discrete_events.models.scheduled_model import ScheduledModel
from tabulate import tabulate

if TYPE_CHECKING:
    from dynamic_system.discrete_events.models.model import Model


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event models"""
    _futureEventList: List[ScheduledModel]

    def __init__(self):
        self._futureEventList = []

    def schedule(self, model: Model, time: float):
        """Schedule an event at the specified time
        :param model Model with an autonomous event scheduled
        :param time Time to execute event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
            if sm not in self._futureEventList:
                heapq.heappush(self._futureEventList, sm)

    def getTimeOfNextEvent(self) -> float:
        """Gets the time of the next event"""
        if len(self._futureEventList) > 0:
            return self._futureEventList[0].getTime()
        return 0

    def updateTime(self, delta_time: float):
        """Updates the time of the events
        :param delta_time Time that has passed since the last update"""
        for i in range(len(self._futureEventList)):
            self._futureEventList[i].decreaseTime(delta_time)

    def getNextModels(self) -> Set[Model]:
        """Gets the next models that will execute an autonomous event"""
        s = set()
        i = 0
        while i < len(self._futureEventList) and self._futureEventList[i].getTime() == self.getTimeOfNextEvent():
            s.add(self._futureEventList[i].getModel())
            i = i + 1
        return s

    def popNextModels(self) -> Set[Model]:
        """Gets the next models that will execute an autonomous event and removes it from the heap"""
        s = set()
        time = self.getTimeOfNextEvent()
        while len(self._futureEventList) > 0 and self._futureEventList[0].getTime() == time:
            s.add(heapq.heappop(self._futureEventList).getModel())
        return s

    def getFutureEventList(self) -> List[ScheduledModel]:
        """Returns the future event list"""
        return self._futureEventList

    def __str__(self):
        data = []
        if len(self._futureEventList) > 0:
            for event in self._futureEventList:
                data += [[event.getModel().getID(), str(event.getTime())]]
        s = "FUTURE EVENT LIST (FEL)\n" + tabulate(data, headers=("MODEL", "TIME"), tablefmt="fancy_grid")
        return s


static_scheduler = Scheduler()
