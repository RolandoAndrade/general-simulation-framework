import unittest
from decimal import Decimal

from core.entity.core import static_entity_manager
from core.entity.properties import NumberProperty
from core.mathematics.distributions import TriangularDistribution, ExponentialDistribution, PoissonDistribution
from core.mathematics.values.value import Value
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.entities import NameGenerator
from queue_simulator.server import Server
from queue_simulator.source import Source
from test.prototypes.prototype_4.assembly_line import AssemblyLine
from test.prototypes.prototype_6.simulator_dynamic_system import SimulatorDynamicSystem


class Prototype6Test(unittest.TestCase):
    vectors = {
        'test_1': {
            'time': Time(50),
            'inter_arrival_time': Value(1),
            'entities_per_arrival': Value(1),
            'time_offset': Value(0),
            'processing_time': Value(2),
            'initial_capacity': NumberProperty(1000),
            'expected': 48
        },
        'test_2': {
            'time': Time(50),
            'inter_arrival_time': Value(1),
            'entities_per_arrival': Value(2),
            'time_offset': Value(0),
            'processing_time': Value(2),
            'initial_capacity': NumberProperty(1),
            'expected': 24
        },
        'test_3': {
            'time': Time(50),
            'inter_arrival_time': Value(1),
            'entities_per_arrival': Value(1),
            'time_offset': Value(0),
            'processing_time': TriangularDistribution(2, 5, 10),
            'initial_capacity': NumberProperty(1000),
            'expected': 45
        },
        'test_4': {
            'time': Time(50),
            'inter_arrival_time': ExponentialDistribution(0.25),
            'entities_per_arrival': Value(1),
            'time_offset': Value(0),
            'processing_time': Value(2),
            'initial_capacity': NumberProperty(1000),
            'expected': 45
        },
        'test_5': {
            'time': Time(50),
            'inter_arrival_time': ExponentialDistribution(0.25),
            'entities_per_arrival': PoissonDistribution(5),
            'time_offset': Value(0),
            'processing_time': TriangularDistribution(2, 5, 10),
            'initial_capacity': NumberProperty(1000),
            'expected': 45
        },
    }

    def setUp(self) -> None:
        self.dynamic_system = SimulatorDynamicSystem()
        self.experiment = DiscreteEventExperiment(self.dynamic_system)
        self.entity_manager = NameGenerator()
        self.source = Source(self.dynamic_system, "Source", entity_manager=self.entity_manager)
        self.server = Server(self.dynamic_system, "Server", entity_manager=self.entity_manager)
        self.source.add(self.server)

    def tearDown(self) -> None:
        static_entity_manager._saved_names = set()

    def test_source_validation_1(self):
        test = 'test_1'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.server.processing_time = self.vectors[test]['processing_time']
        self.server.initial_capacity = self.vectors[test]['initial_capacity']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.server.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_2(self):
        test = 'test_2'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.server.processing_time = self.vectors[test]['processing_time']
        self.server.initial_capacity = self.vectors[test]['initial_capacity']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.server.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_3(self):
        test = 'test_3'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.server.processing_time = self.vectors[test]['processing_time']
        self.server.initial_capacity = self.vectors[test]['initial_capacity']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        print(self.server.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_4(self):
        test = 'test_4'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.server.processing_time = self.vectors[test]['processing_time']
        self.server.initial_capacity = self.vectors[test]['initial_capacity']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        print(self.server.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_5(self):
        test = 'test_5'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.server.processing_time = self.vectors[test]['processing_time']
        self.server.initial_capacity = self.vectors[test]['initial_capacity']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        print(self.server.get_state().output_buffer.number_entered.get_value())


if __name__ == "__main__":
    unittest.main()
