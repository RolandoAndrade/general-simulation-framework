from __future__ import annotations

import unittest
from typing import TYPE_CHECKING, List, Dict


if TYPE_CHECKING:
    from core.old_events.subscriber import Subscriber

from core.old_events.event_bus import EventBus


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(isinstance(EventBus()._events, Dict))
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
