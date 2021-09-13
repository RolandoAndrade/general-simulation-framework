import unittest

from core.entity.core import static_entity_manager
from core.mathematics.values.value import Value
from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.entities import NameGenerator
from queue_simulator.source import Source
from test.prototypes.prototype_4.assembly_line import AssemblyLine
from test.prototypes.prototype_6.simulator_dynamic_system import SimulatorDynamicSystem


class Prototype6Test(unittest.TestCase):
    def setUp(self) -> None:
        self.dynamic_system = SimulatorDynamicSystem()
        self.experiment = DiscreteEventExperiment(self.dynamic_system)
        self.entity_manager = NameGenerator()
        self.source = Source(self.dynamic_system, "Source", entity_manager=self.entity_manager)

    def tearDown(self) -> None:
        static_entity_manager._saved_names = set()

    def test_source_validation_1(self):
        """Run 5 seconds, inter_arrival_time = 1, entities_per_arrival_2, time_offset = 0"""
        time = Time(5)
        self.source.inter_arrival_time = Value(1)
        self.source.entities_per_arrival = Value(2)
        self.source.time_offset = Value(0)
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(12, self.source.get_state().output_buffer.number_entered.get_value())

    def test_source_validation_2(self):
        """Run 10 seconds, inter_arrival_time = 2, entities_per_arrival = 1, time_offset = 2"""
        time = Time(10)
        self.source.inter_arrival_time = Value(1)
        self.source.entities_per_arrival = Value(1)
        self.source.time_offset = Value(2)
        self.experiment.simulation_control.start(stop_time=time)
        self.experiment.simulation_control.wait()
        self.assertEqual(9, self.source.get_state().output_buffer.number_entered.get_value())


if __name__ == "__main__":
    unittest.main()
