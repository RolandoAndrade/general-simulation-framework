import unittest

from core.entity.core import static_entity_manager
from core.entity.properties.property import Property
from core.mathematics.values.value import Value
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from dynamic_system.future_event_list import Scheduler
from queue_simulator.queue_components.source import Source
from test.mocks.mock_emitter import MockEmitter


class TestSource(unittest.TestCase):
    source: Source
    dynamic_system: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        """Sets up the source"""
        self.dynamic_system = DiscreteEventDynamicSystem(Scheduler())
        self.source = Source(
            self.dynamic_system, name="Source1", entity_emitter=Property(MockEmitter())
        )

    def tearDown(self) -> None:
        """Reset names"""
        static_entity_manager._saved_names = set()

    def test_interarrival_time(self):
        """Should set and get interarrival time"""
        self.source.inter_arrival_time = Value(1)
        self.assertEqual(1, self.source.inter_arrival_time.get_value().evaluate())

    def test_entities_per_arrival(self):
        """Should set and get entities per arrival"""
        self.source.entities_per_arrival = Value(1)
        self.assertEqual(1, self.source.entities_per_arrival.get_value().evaluate())

    def test_entity_emitter(self):
        """Should set and get entity entities"""
        e = MockEmitter()
        self.source.entity_emitter = e
        self.assertEqual(e, self.source.entity_emitter.get_value())

    def test_internal_state_transition_function(self):
        """Should set and get entity entities"""
        self.source.entities_per_arrival = Value(5)
        self.source.inter_arrival_time = Value(1)
        self.source.state_transition()
        self.assertEqual(
            5, self.source.get_state().output_buffer.current_number_of_entities
        )

    def test_get_time(self):
        """Should get the time"""
        self.source.inter_arrival_time = Value(1)
        self.assertEqual(1, self.source.get_time())

    def test_time_offset(self):
        """Should set and get time offset"""
        self.source.time_offset = Value(5)
        self.assertEqual(5, self.source.time_offset.get_value().evaluate())

    def test_get_properties(self):
        """Should have the expected properties"""
        expect_keys = {
            "Entities Per Arrival",
            "Time Offset",
            "Interarrival Time",
            "Entity Type",
        }
        actual_keys = set(self.source.get_properties().keys())
        self.assertEqual(expect_keys, actual_keys)

    def test_serialization(self):
        """Should have the expected properties"""
        properties = self.source.serialize()
        print(properties)

    def test_get_stats(self):
        """Should return the stats"""
        stats = self.source.get_stats()
        print(stats.serialize())


if __name__ == "__main__":
    unittest.main()
