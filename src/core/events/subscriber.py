from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.events.event_bus import EventBus


class Subscriber:
    _event_bus: EventBus

    def __init__(self, event_bus: EventBus):
        self._event_bus = event_bus

    def subscribe(self, event: str):
        self._event_bus.subscribe(event, self)
