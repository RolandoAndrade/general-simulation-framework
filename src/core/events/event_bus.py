from __future__ import annotations
from typing import List, TYPE_CHECKING
from src.core.events.event import Event
if TYPE_CHECKING:
    from src.core.events.subscriber import Subscriber


class EventBus:
    _events: List[Event]

    def __init__(self):
        self._events = []

    def subscribe(self, event: str, subscriber: Subscriber):
        for e in self._events:
            if e.event == event:
                e.subscribers.append(subscriber)
                return
        self._events.append(Event(event, subscriber))
