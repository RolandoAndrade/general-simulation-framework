from typing import List

from src.core.events.subscriber import Subscriber


class Event:
    event: str
    subscribers: List[Subscriber]
