import unittest

from core.entity.core import static_entity_manager
from core.entity.properties import NumberProperty
from core.mathematics.distributions import TriangularDistribution, ExponentialDistribution, PoissonDistribution
from core.mathematics.values.value import Value
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.queue_components.entities import NameGenerator
from queue_simulator.queue_components.experiments import SimulationExperiment
from queue_simulator.queue_components.server import Server, ServerProperty
from queue_simulator.queue_components.shared.models.node_property import NodeProperty
from queue_simulator.queue_components.shared.nodes import NodeType
from queue_simulator.queue_components.source import Source, SourceProperty
from test.prototypes.prototype_6.simulator_dynamic_system import SimulatorDynamicSystem


class Prototype8Test(unittest.TestCase):
    vectors = {
        'test_1': {
            'time': Time(20),
            'inter_arrival_time': 'Random.Exponential(7)',
            'entities_per_arrival': 'Random.Poisson(4)',
            'time_offset': Value(0),
            'processing_time': 'Random.Exponential(1)',
            'initial_capacity': '1000',
            'expected': 48
        },
    }

    def setUp(self) -> None:
        self.experiment = SimulationExperiment()
        self.entity_manager = NameGenerator()

    def tearDown(self) -> None:
        static_entity_manager._saved_names = set()

    def test_source_validation_1(self):
        test = 'test_1'
        time = self.vectors[test]['time']
        source = self.experiment.add_node(NodeType.SOURCE)
        server = self.experiment.add_node(NodeType.SERVER)
        sink = self.experiment.add_node(NodeType.SINK)
        self.experiment.add_path(source.get_id(), server.get_id())
        self.experiment.add_path(server.get_id(), sink.get_id())
        self.experiment.edit_property(source.get_id(), NodeProperty(SourceProperty.INTER_ARRIVAL_TIME,
                                                                    self.vectors[test]['inter_arrival_time'],
                                                                    'EXPRESSION', 'GENERIC'))
        self.experiment.edit_property(source.get_id(), NodeProperty(SourceProperty.ENTITIES_PER_ARRIVAL,
                                                                    self.vectors[test]['entities_per_arrival'],
                                                                    'EXPRESSION', 'GENERIC'))
        self.experiment.edit_property(server.get_id(), NodeProperty(ServerProperty.PROCESSING_TIME,
                                                                    self.vectors[test]['processing_time'], 'EXPRESSION',
                                                                    'GENERIC'))
        self.experiment.edit_property(server.get_id(), NodeProperty(ServerProperty.INITIAL_CAPACITY,
                                                                    self.vectors[test]['initial_capacity'], 'NUMBER',
                                                                    'GENERIC'))

        source_label_out = self.experiment.add_label()
        self.experiment.edit_label(source_label_out.get_id(),
                                   NodeProperty("Expression", "Source1.OutputBuffer.NumberEntered", 'EXPRESSION',
                                                'GENERIC'))

        server_label_out = self.experiment.add_label()
        self.experiment.edit_label(server_label_out.get_id(),
                                   NodeProperty("Expression", "Server1.OutputBuffer.NumberEntered", 'EXPRESSION',
                                                'GENERIC'))

        server_label_in = self.experiment.add_label()
        self.experiment.edit_label(server_label_in.get_id(),
                                   NodeProperty("Expression", "Server1.InputBuffer.NumberEntered", 'EXPRESSION',
                                                'GENERIC'))

        sink_label_in = self.experiment.add_label()
        self.experiment.edit_label(sink_label_in.get_id(),
                                   NodeProperty("Expression", "Sink1.InputBuffer.NumberEntered", 'EXPRESSION',
                                                'GENERIC'))

        results = []

        print(source.serialize())
        print(server.serialize())
        for i in range(15):
            self.experiment.start_simulation(stop_time=time)
            self.experiment.simulation_control.wait()
            results.append(sink.get_state().input_buffer.number_entered.get_value())
            print([str(source_label_out), str(server_label_in), str(server_label_out), str(sink_label_in)])

        print(results)


if __name__ == "__main__":
    unittest.main()
