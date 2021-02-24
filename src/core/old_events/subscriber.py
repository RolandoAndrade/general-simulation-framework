from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict

if TYPE_CHECKING:
    from src.core.old_events.event_bus import EventBus


class Subscriber:
    _event_bus: EventBus
    _callbacks: Dict[str, Callable[[Any], Any]]

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._callbacks = {}

    "Subscribe to event messages"
    def subscribe(self, event: str):
        self._event_bus.subscribe(event, self)

    "Unsubscribe to event messages"
    def unsubscribe(self, event: str):
        self._event_bus.unsubscribe(event, self)

    "Call back methods defined for messages received from event bus"
    def on_message_received(self, event: str, message: Any):
        if event in self._callbacks:
            self._callbacks[event](message)

    "Listen for messages"
    def on(self, event: str, function: Callable[[Any], Any]):
        if not(event in self._callbacks):
            self.subscribe(event)
        self._callbacks[event] = function

    "Send a message to all subscribers for an event"
    def emit(self, event: str, message: Any):
        self._event_bus.emit(event, message)
