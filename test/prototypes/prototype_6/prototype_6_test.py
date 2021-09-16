import unittest

from core.entity.core import static_entity_manager
from core.mathematics.values.value import Value
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.queue_components.entities import NameGenerator
from queue_simulator.queue_components.source import Source
from test.prototypes.prototype_6.simulator_dynamic_system import SimulatorDynamicSystem


class Prototype6Test(unittest.TestCase):
    vectors = {
        'test_1': {
            'time': Time(5),
            'inter_arrival_time': Value(1),
            'entities_per_arrival': Value(1),
            'time_offset': Value(0),
            'expected': 6
        },
        'test_2': {
            'time': Time(5),
            'inter_arrival_time': Value(1),
            'entities_per_arrival': Value(2),
            'time_offset': Value(0),
            'expected': 12
        },
        'test_3': {
            'time': Time(10),
            'inter_arrival_time': Value(2),
            'entities_per_arrival': Value(1),
            'time_offset': Value(3),
            'expected': 4
        },
        'test_4': {
            'time': Time(100),
            'inter_arrival_time': Value(5),
            'entities_per_arrival': Value(7),
            'time_offset': Value(10),
            'expected': 133
        },
        'test_5': {
            'time': Time(5),
            'inter_arrival_time': Value(10),
            'entities_per_arrival': Value(10),
            'time_offset': Value(10),
            'expected': 0
        },
    }

    def setUp(self) -> None:
        self.dynamic_system = SimulatorDynamicSystem()
        self.experiment = DiscreteEventExperiment(self.dynamic_system)
        self.entity_manager = NameGenerator()
        self.source = Source(self.dynamic_system, "Source", entity_manager=self.entity_manager)

    def tearDown(self) -> None:
        static_entity_manager._saved_names = set()

    def test_source_validation_1(self):
        test = 'test_1'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.source.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_2(self):
        test = 'test_2'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.source.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_3(self):
        test = 'test_3'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.source.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_4(self):
        test = 'test_4'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.source.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_5(self):
        test = 'test_5'
        time = self.vectors[test]['time']
        self.source.inter_arrival_time = self.vectors[test]['inter_arrival_time']
        self.source.entities_per_arrival = self.vectors[test]['entities_per_arrival']
        self.source.time_offset = self.vectors[test]['time_offset']
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(self.vectors[test]['expected'],
                         self.source.get_state().output_buffer.number_entered.get_value())


if __name__ == "__main__":
    unittest.main()
