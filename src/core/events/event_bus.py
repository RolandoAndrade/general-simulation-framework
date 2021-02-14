from __future__ import annotations
from typing import List, TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from src.core.events.subscriber import Subscriber


class EventBus:
    _events: Dict[str, List[Subscriber]]

    def __init__(self):
        self._events = {}

    def subscribe(self, event: str, subscriber: Subscriber):
        if event in self._events:
            self._events[event].append(subscriber)
        else:
            self._events[event] = [subscriber]

    def unsubscribe(self, event: str, subscriber: Subscriber):
        if event in self._events:
            self._events[event].remove(subscriber)