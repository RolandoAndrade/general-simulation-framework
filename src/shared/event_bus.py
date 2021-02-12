from typing import List

from src.shared.event import Event


class EventBus:
    events: List[Event]
