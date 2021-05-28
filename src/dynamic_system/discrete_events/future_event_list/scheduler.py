from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, List, Set


from dynamic_system.discrete_events.models.scheduled_model import ScheduledModel
from prettytable import PrettyTable

if TYPE_CHECKING:
    from dynamic_system.discrete_events.models.discrete_event_model import DiscreteEventModel


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event
    models
    """
    _futureEventList: List[ScheduledModel]

    def __init__(self):
        self._futureEventList = []

    def schedule(self, model: DiscreteEventModel, time: float):
        """Schedule an event at the specified time :param model
        Args:
            model (DiscreteEventModel): DiscreteEventModel with an autonomous event scheduled
            time (float): Time to execute an autonomous event
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

        Args:
            delta_time (float): Time that has passed since the last update
        """
        for i in range(len(self._futureEventList)):
            self._futureEventList[i].decreaseTime(delta_time)

    def getNextModels(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event"""
        s = set()
        i = 0
        while i < len(self._futureEventList) and self._futureEventList[i].getTime() == self.getTimeOfNextEvent():
            s.add(self._futureEventList[i].getModel())
            i = i + 1
        return s

    def popNextModels(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event and
        removes it from the heap
        """
        s = set()
        time = self.getTimeOfNextEvent()
        while len(self._futureEventList) > 0 and self._futureEventList[0].getTime() == time:
            s.add(heapq.heappop(self._futureEventList).getModel())
        return s

    def getFutureEventList(self) -> List[ScheduledModel]:
        """Returns the future event list"""
        return self._futureEventList

    def __str__(self):
        x = PrettyTable()
        x.title = "Future Event List (FEL)"
        x.field_names = ["Model ID", "Priority", "Time"]
        x.align["Priority"] = "r"
        x.align["Model ID"] = "l"
        x.align["Time"] = "r"
        priority = 0
        lastTime = 0
        if len(self._futureEventList) > 0:
            for event in self._futureEventList:
                if lastTime != event.getTime():
                    priority = priority + 1
                x.add_row([event.getModel().getID(), priority, str(event.getTime())])
                lastTime = event.getTime()
        return str(x)


static_scheduler = Scheduler()
