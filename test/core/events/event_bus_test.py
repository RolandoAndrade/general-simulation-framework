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
        self.assertEqual(len(self.event_bus._events), 3)
        self.assertEqual(len(self.event_bus._events[0].subscribers), 2)


if __name__ == '__main__':
    unittest.main()
