import unittest

from core.entity.core import Entity
from core.entity.properties import Property, NumberProperty
from core.mathematics.values.value import Value
from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from queue_simulator.buffer.core import BufferProperty
from queue_simulator.label.label import Label
from queue_simulator.server.server import Server
from queue_simulator.sink.sink import Sink
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
        """1 source, 1 server, 1 arrival/second every second during 5 seconds"""
        source = Source(self.dynamic_system,
                        name="Source",
                        entity_emitter=Property(MockEmitter()),
                        inter_arrival_time=Value(1),
                        entities_per_arrival=Value(1),
                        time_offset=Value(0))

        server = Server(self.dynamic_system,
                        name="Server",
                        processing_time=Value(1))

        sink = Sink(self.dynamic_system,
                    name="Sink")

        source.add(server)
        server.add(sink)

        source.init()

        label_source_out = Label(source.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_in = Label(server.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_out = Label(server.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_sink_in = Label(sink.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)

        experiment = DiscreteEventExperiment(self.dynamic_system)
        experiment.simulation_control.start(stop_time=Time(5))
        experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))

        print(experiment.simulation_report.generate_report())

        self.assertEqual("6", str(label_source_out))
        self.assertEqual("5", str(label_server_in))
        self.assertEqual("4", str(label_server_out))
        self.assertEqual("4", str(label_server_out))

    def test_simulation_server_delay(self):
        """Server process entities slowly than arrivals"""
        source = Source(self.dynamic_system,
                        name="Source",
                        entity_emitter=Property(MockEmitter()),
                        inter_arrival_time=Value(1),
                        entities_per_arrival=Value(2),
                        time_offset=Value(0))

        server = Server(self.dynamic_system,
                        name="Server",
                        processing_time=Value(2),
                        initial_capacity=NumberProperty(1000))

        sink = Sink(self.dynamic_system,
                    name="Sink")

        source.add(server)
        server.add(sink)

        source.init()

        label_source_out = Label(source.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_in = Label(server.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_out = Label(server.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_sink_in = Label(sink.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)

        experiment = DiscreteEventExperiment(self.dynamic_system)
        experiment.simulation_control.start(stop_time=Time(10))
        experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))
        print(experiment.simulation_report.generate_report())

        self.assertEqual("22", str(label_source_out))
        self.assertEqual("20", str(label_server_in))
        self.assertEqual("16", str(label_server_out))
        self.assertEqual("16", str(label_server_out))


if __name__ == '__main__':
    unittest.main()
