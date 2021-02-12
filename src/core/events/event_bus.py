from typing import List

from src.core.events.event import Event


class EventBus:
    events: List[Event]
