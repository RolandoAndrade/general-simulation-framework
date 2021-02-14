from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict

if TYPE_CHECKING:
    from src.core.events.event_bus import EventBus


class Subscriber:
    _event_bus: EventBus
    _callbacks: Dict[str, Callable[[Any], None]]

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus
        self._callbacks = {}

    def subscribe(self, event: str):
        self._event_bus.subscribe(event, self)

    def unsubscribe(self, event: str):
        self._event_bus.unsubscribe(event, self)

    def on_message_received(self, event: str, message: Any):
        if event in self._callbacks:
            self._callbacks[event](message)

    def on(self, event: str, function: Callable[[Any], None]):
        if not(event in self._callbacks):
            self.subscribe(event)
            self._callbacks[event] = function
