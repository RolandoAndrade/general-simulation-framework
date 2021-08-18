import unittest
from decimal import Decimal

from core.entity.core import Entity
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from models.models import DiscreteEventModel
from test.mocks.dynamic_system_mock import DynamicSystemMock
from test.mocks.model_mock import ModelMock


class DiscreteEventModelTest(unittest.TestCase):
    """Discrete event model tests"""
    dynamic_system: DiscreteEventDynamicSystem
    model: DiscreteEventModel

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock()
        self.model = ModelMock(self.dynamic_system, "model")

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_schedule(self):
        """Should schedule an event."""
        self.model.schedule(Decimal(5))
        self.assertEqual(5, self.dynamic_system.get_time_of_next_events())

    def test_get_time(self):
        """Should retrieve the time evaluating the time advance function"""
        self.model._time_advance_function = lambda s: 10
        self.assertEqual(10, self.model.get_time())

    def test_get_output(self):
        """Should retrieve the output evaluating the time output function"""
        self.model._output_function = lambda s: 42
        self.assertEqual(42, self.model.get_output())

    def test_internal_transition(self):
        """Should execute autonomous, external and confluent transitions."""
        self.model.set_up_state(0)
        self.model._time_advance_function = lambda s: 10
        self.model._external_state_transition_function = lambda s, i, t: 1
        self.model._internal_state_transition_function = lambda s:  s + 2
        self.model.state_transition(event_time=Decimal(0))
        self.assertEqual(2, self.model.get_state())

    def test_external_transition(self):
        """Should execute autonomous, external and confluent transitions."""
        self.model.set_up_state(0)
        self.model._time_advance_function = lambda s: 10
        self.model._external_state_transition_function = lambda s, i, t: s + i
        self.model._internal_state_transition_function = lambda s:  s + 2
        self.model.state_transition(inputs=19, event_time=Decimal(2))
        self.assertEqual(19, self.model.get_state())

    def test_confluent_transition(self):
        """Should execute autonomous, external and confluent transitions."""
        self.model.set_up_state(0)
        self.model._time_advance_function = lambda s: 10
        self.model._external_state_transition_function = lambda s, i, t: s + i
        self.model._internal_state_transition_function = lambda s:  s + 2
        self.model.state_transition(inputs=19, event_time=Decimal(0))
        self.assertEqual(21, self.model.get_state())

if __name__ == '__main__':
    unittest.main()
