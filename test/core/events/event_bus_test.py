from __future__ import annotations
import unittest
from src.core.events.event_bus import EventBus
from src.core.events.subscriber import Subscriber


class EventBusTest(unittest.TestCase):
    event_bus: EventBus

    def setUp(self) -> None:
        self.event_bus = EventBus()

    def test_subscription(self):
        sub1 = Subscriber(self.event_bus)
        sub1.subscribe("test_1")
        sub1.subscribe("test_2")
        sub1.subscribe("test_3")
        sub2 = Subscriber(self.event_bus)
        sub2.subscribe("test_1")
        self.assertEqual(3, len(self.event_bus._events.keys()))
        self.assertEqual(2, len(self.event_bus._events["test_1"]))

    def test_unsubscription(self):
        sub1 = Subscriber(self.event_bus)
        sub2 = Subscriber(self.event_bus)
        sub3 = Subscriber(self.event_bus)
        sub1.subscribe("test_1")
        sub2.subscribe("test_1")
        sub3.subscribe("test_1")
        sub2.unsubscribe("test_1")
        self.assertEqual(2, len(self.event_bus._events["test_1"]))


if __name__ == '__main__':
    unittest.main()
