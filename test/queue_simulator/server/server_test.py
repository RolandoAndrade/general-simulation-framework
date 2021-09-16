import unittest

from core.entity.properties import Property, ExpressionProperty, NumberProperty
from core.mathematics.values.value import Value
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import (
    DiscreteEventExperiment,
)
from queue_simulator.queue_components.server import Server
from queue_simulator.queue_components.source import Source
from test.mocks.mock_emitter import MockEmitter


class ServerTest(unittest.TestCase):
    source: Source
    server: Server
    experiment: DiscreteEventExperiment
    ds: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        """Setups the source, dynamic system and experiment"""
        self.ds = DiscreteEventDynamicSystem()
        self.source = Source(
            self.ds, name="Source1", entity_emitter=Property(MockEmitter())
        )
        self.server = Server(self.ds, name="Server")
        self.source.add(self.server)
        self.experiment = DiscreteEventExperiment(self.ds)

    def test_processing(self):
        """Should process entities"""
        inter_arrival_time = ExpressionProperty(Value(1))
        entities_per_arrival = ExpressionProperty(Value(5))
        self.source.inter_arrival_time = inter_arrival_time
        self.source.entities_per_arrival = entities_per_arrival

        processing_time = ExpressionProperty(Value(2))
        self.server.processing_time = processing_time
        self.server.get_state().process_buffer.capacity = NumberProperty(1)
        # simulate
        self.experiment.simulation_control.start(stop_time=120)
        self.experiment.simulation_control.wait()
        # results
        total = self.source.get_state().output_buffer.number_entered.get_value()
        self.assertEqual(121 * 5, total, "Wrong")
        total = self.server.get_state().input_buffer.number_entered.get_value()
        self.assertEqual(120 * 5, total, "Wrong")
        total = self.server.get_state().process_buffer.number_entered.get_value()
        self.assertEqual(60, total, "Wrong")
        total = self.server.get_state().output_buffer.number_entered.get_value()
        self.assertEqual(59, total, "Wrong")


if __name__ == "__main__":
    unittest.main()
