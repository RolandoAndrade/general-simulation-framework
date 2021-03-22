from __future__ import annotations
import heapq

from typing import TYPE_CHECKING, List, Optional
from dynamic_system.models.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from dynamic_system.models.state_model import StateModel


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event models"""
    _futureEventList: List[ScheduledModel]

    def __init__(self):
        self._futureEventList = []

    def schedule(self, model: StateModel, time: float):
        """Schedule an event at the specified time
        :param model Model with an autonomous event scheduled
        :param time Time to execute event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
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

    def getNextModel(self) -> Optional[StateModel]:
        """Gets the next model that will execute an autonomous event"""
        if len(self._futureEventList) > 0:
            return self._futureEventList[0].getModel()
        return None

    def popNextModel(self) -> Optional[StateModel]:
        """Gets the next model that will execute an autonomous event and removes it from the heap"""
        if len(self._futureEventList) > 0:
            return heapq.heappop(self._futureEventList).getModel()
        return None

    def getFutureEventList(self) -> List[ScheduledModel]:
        """Returns the future event list"""
        return self._futureEventList

    def __str__(self):
        s = "Future event list\n"
        if len(self._futureEventList) > 0:
            for event in self._futureEventList:
                s += event.getModel().getID() + " -> " + str(event.getTime()) + "\n"
        else:
            s += "empty\n"
        return s


static_scheduler = Scheduler()
