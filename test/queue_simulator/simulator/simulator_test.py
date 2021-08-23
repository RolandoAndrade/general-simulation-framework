import unittest

from core.entity.core import Entity
from core.entity.properties import Property
from core.mathematics.values.value import Value
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from queue_simulator.buffer.core import BufferProperty
from queue_simulator.label.label import Label
from queue_simulator.server.server import Server
from queue_simulator.source import Source
from test.mocks.dynamic_system_mock import DynamicSystemMock
from test.mocks.mock_emitter import MockEmitter


class SimulatorTest(unittest.TestCase):
    """Base dynamic system tests"""
    dynamic_system: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        """Sets up tests"""
        self.dynamic_system = DynamicSystemMock(Scheduler())

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_basic_simulation(self):
        """1 source, 1 server, 1 arrival/second every second during 60 seconds"""
        source = Source(self.dynamic_system,
                        name="Source",
                        entity_emitter=Property(MockEmitter()),
                        inter_arrival_time=Value(1),
                        entities_per_arrival=Value(1),
                        time_offset=Value(0))

        server = Server(self.dynamic_system,
                        name="Server",
                        processing_time=Value(1))
        source.add(server)
        source.init()

        label_source_out = Label(source.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_in = Label(server.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_out = Label(server.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)

        experiment = DiscreteEventExperiment(self.dynamic_system)
        experiment.simulation_control.start(stop_time=Time(5))
        experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print(experiment.simulation_report.generate_report())


if __name__ == '__main__':
    unittest.main()
