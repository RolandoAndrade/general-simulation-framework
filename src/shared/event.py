from typing import List

from src.shared.subscriber import Subscriber


class Event:
    event: str
    subscribers: List[Subscriber]
