from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, List, Set

from core.debug.domain.debug import debug
from core.debug.infrastructure.providers import TableProvider
from dynamic_system.models.scheduled_model import ScheduledModel

if TYPE_CHECKING:
    from dynamic_system.models.discrete_event_model import (
        DiscreteEventModel,
    )


class Scheduler:
    """Scheduler for execution of the autonomous events of discrete-event
    models
    """

    _futureEventList: List[ScheduledModel]

    def __init__(self):
        self._futureEventList = []

    @debug("Scheduling model")
    def schedule(self, model: DiscreteEventModel, time: float):
        """Schedule an event at the specified time
        Args:
            model (DiscreteEventModel): DiscreteEventModel with an autonomous event scheduled
            time (float): Time to execute an autonomous event
        """
        if time > 0:
            sm = ScheduledModel(model, time)
            if sm not in self._futureEventList:
                heapq.heappush(self._futureEventList, sm)

    @debug("Getting time of next event")
    def getTimeOfNextEvent(self) -> float:
        """Gets the time of the next event"""
        if len(self._futureEventList) > 0:
            return self._futureEventList[0].getTime()
        return 0

    @debug("Updating time")
    def updateTime(self, delta_time: float):
        """Updates the time of the events

        Args:
            delta_time (float): Time that has passed since the last update
        """
        for i in range(len(self._futureEventList)):
            self._futureEventList[i].decreaseTime(delta_time)

    @debug("Getting next models")
    def getNextModels(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event"""
        s = set()
        fel = self._futureEventList.copy()
        time = self.getTimeOfNextEvent()
        while len(fel) > 0 and fel[0].getTime() == time:
            s.add(heapq.heappop(fel).getModel())
        return s

    @debug("Removing models from the heap")
    def popNextModels(self) -> Set[DiscreteEventModel]:
        """Gets the next models that will execute an autonomous event and
        removes it from the heap
        """
        s = set()
        time = self.getTimeOfNextEvent()
        while (
            len(self._futureEventList) > 0
            and self._futureEventList[0].getTime() == time
        ):
            s.add(heapq.heappop(self._futureEventList).getModel())
        return s

    @debug("Getting future event list")
    def getFutureEventList(self) -> List[ScheduledModel]:
        """Returns the future event list"""
        return self._futureEventList

    def __str__(self):
        x = TableProvider()
        x.setTitle("Future Event List (FEL)").setLabels(
            ["Model ID", "Priority", "Time"]
        )
        x.setAlignment(["l", "r", "r"])
        priority = 0
        lastTime = 0
        if len(self._futureEventList) > 0:
            for event in self._futureEventList:
                if lastTime != event.getTime():
                    priority = priority + 1
                x.addRow([event.getModel().getID(), priority, str(event.getTime())])
                lastTime = event.getTime()
        return x.build()
