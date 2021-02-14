from __future__ import annotations
from typing import List, TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from src.core.events.subscriber import Subscriber


class EventBus:
    _events: Dict[str, List[Subscriber]]

    def __init__(self):
        self._events = {}

    "Subscribe an object to event."
    def subscribe(self, event: str, subscriber: Subscriber):
        if event in self._events:
            self._events[event].append(subscriber)
        else:
            self._events[event] = [subscriber]

    "Unsubscribe an object to event."
    def unsubscribe(self, event: str, subscriber: Subscriber):
        if event in self._events:
            self._events[event].remove(subscriber)
        else:
            raise Exception("Event is not defined")

    "Send a message to all subscribers for an event"
    def emit(self, event: str, message: Any):
        if event in self._events:
            for e in self._events[event]:
                e.on_message_received(event, message)
        else:
            raise Exception("Event is not defined")
