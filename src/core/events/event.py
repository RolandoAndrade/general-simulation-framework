from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.events.subscriber import Subscriber


class Event:
    event: str
    subscribers: List[Subscriber]

    def __init__(self, event: str, subscriber: Subscriber):
        self.event = event
        self.subscribers = [subscriber]
