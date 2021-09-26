import unittest
from typing import List

from gsf.core.entity.properties import Property, NumberProperty
from gsf.core.mathematics.distributions import (
    ExponentialDistribution,
    TriangularDistribution,
)
from gsf.core.mathematics.values import Value
from gsf.core.types import Time
from queue_simulator.queue_components.label.label import Label
from queue_simulator.queue_components.experiments import (
    SimulationExperiment,
)
from queue_simulator.queue_components.shared.nodes import NodeType


class SimulatorTest(unittest.TestCase):
    """Base dynamic system tests"""

    experiment: SimulationExperiment

    def setUp(self) -> None:
        """Sets up tests"""
        self.experiment = SimulationExperiment()
        self.expression_manager = self.experiment._expression_manager

    def test_basic_simulation(self):
        """1 source, 1 server, 1 arrival/second every second during 5 seconds"""
        emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
        source = self.experiment.add_node(NodeType.SOURCE)
        source.set_id("Source")
        source.entity_emitter = Property(emitter)
        source.inter_arrival_time = Value(Time(1))
        source.entities_per_arrival = Value(1)
        source.time_offset = Value(0)

        server = self.experiment.add_node(NodeType.SERVER)
        server.set_id("Server")
        server.processing_time = Value(1)

        sink = self.experiment.add_node(NodeType.SINK)
        sink.set_id("Sink")

        self.experiment.add_path(source.get_id(), server.get_id())
        self.experiment.add_path(server.get_id(), sink.get_id())

        label_source_out = Label("Source1.OutputBuffer.NumberEntered", self.expression_manager)
        label_server_in = Label("Server1.InputBuffer.NumberEntered", self.expression_manager)
        label_server_out = Label("Server1.OutputBuffer.NumberEntered", self.expression_manager)
        label_sink_in = Label("Sink1.InputBuffer.NumberEntered", self.expression_manager)

        self.experiment.start_simulation(stop_time=Time(5))
        self.experiment.simulation_control.wait()
        self.experiment.save()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))

        self.assertEqual("6", str(label_source_out))
        self.assertEqual("5", str(label_server_in))
        self.assertEqual("4", str(label_server_out))
        self.assertEqual("4", str(label_server_out))

    def test_simulation_server_delay(self):
        """Server process entities slowly than arrivals"""
        emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
        source = self.experiment.add_node(NodeType.SOURCE)
        source.set_id("Source")
        source.entity_emitter = Property(emitter)
        source.inter_arrival_time = Value(1)
        source.entities_per_arrival = Value(2)
        source.time_offset = Value(0)

        server = self.experiment.add_node(NodeType.SERVER)
        server.set_id("Server")
        server.processing_time = Value(2)
        server.initial_capacity = NumberProperty(1000)

        sink = self.experiment.add_node(NodeType.SINK)
        sink.set_id("Sink")

        source.add(server)
        server.add(sink)

        label_source_out = Label("Source1.OutputBuffer.NumberEntered", self.expression_manager)
        label_server_in = Label("Server1.InputBuffer.NumberEntered", self.expression_manager)
        label_server_out = Label("Server1.OutputBuffer.NumberEntered", self.expression_manager)
        label_sink_in = Label("Sink1.InputBuffer.NumberEntered", self.expression_manager)

        self.experiment.save()

        self.experiment.start_simulation(stop_time=Time(10))
        self.experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))

        self.assertEqual("22", str(label_source_out))
        self.assertEqual("20", str(label_server_in))
        self.assertEqual("16", str(label_server_out))
        self.assertEqual("16", str(label_server_out))

    def test_simulation_random(self):
        """Server process entities slowly than arrivals"""
        interarrival_time_seconds = ExponentialDistribution(
            0.25
        )  # 0.25 mean interarrival time
        entities_per_arrival = Value(1)  # 1 entity per arrival
        simulation_time_minutes = 60 * 2  # 2 hours
        processing_time = TriangularDistribution(0.1, 0.2, 0.3)  # 2 seconds

        emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
        source = self.experiment.add_node(NodeType.SOURCE)
        source.set_id("Source")
        source.entity_emitter = Property(emitter)
        source.inter_arrival_time = interarrival_time_seconds
        source.entities_per_arrival = entities_per_arrival

        server = self.experiment.add_node(NodeType.SERVER)
        server.set_id("Server")
        server.processing_time = processing_time
        server.initial_capacity = NumberProperty(1000)

        sink = self.experiment.add_node(NodeType.SINK)
        sink.set_id("Sink")

        source.add(server)
        server.add(sink)

        label_source_out = Label("Source1.OutputBuffer.NumberEntered", self.expression_manager)
        label_server_in = Label("Server1.InputBuffer.NumberEntered", self.expression_manager)
        label_server_out = Label("Server1.OutputBuffer.NumberEntered", self.expression_manager)
        label_sink_in = Label("Sink1.InputBuffer.NumberEntered", self.expression_manager)

        self.experiment.save()

        self.experiment.start_simulation(
            stop_time=Time(simulation_time_minutes)
        )
        self.experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))

        print(474)
        print(474)
        print(472)
        print(471)

    def test_simulation_server_double_delay(self):
        """Server process entities slowly than arrivals"""
        labels: List[List[Label]] = []
        for i in range(3):
            emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
            source = self.experiment.add_node(NodeType.SOURCE)
            source.entity_emitter = Property(emitter)
            source.inter_arrival_time = Value(1)
            source.entities_per_arrival = Value(2)
            source.time_offset = Value(0)

            server = self.experiment.add_node(NodeType.SERVER)
            server.processing_time = Value(2)
            server.initial_capacity = NumberProperty(1000)

            sink = self.experiment.add_node(NodeType.SINK)

            source.add(server)
            server.add(sink)

            label_source_out = Label("Source1.OutputBuffer.NumberEntered", self.expression_manager)
            label_server_in = Label("Server1.InputBuffer.NumberEntered", self.expression_manager)
            label_server_out = Label("Server1.OutputBuffer.NumberEntered", self.expression_manager)
            label_sink_in = Label("Sink1.InputBuffer.NumberEntered", self.expression_manager)

            labels.append(
                [label_source_out, label_server_in, label_server_out, label_sink_in]
            )

        self.experiment.start_simulation(stop_time=Time(10))
        self.experiment.simulation_control.wait()

        for label_list in labels:
            print("Generated: " + str(label_list[0]))
            print("Entered to server: " + str(label_list[1]))
            print("Processed by server: " + str(label_list[2]))
            print("Entered to sink: " + str(label_list[3]))
            self.assertEqual("22", str(label_list[0]))
            self.assertEqual("20", str(label_list[1]))
            self.assertEqual("16", str(label_list[2]))
            self.assertEqual("16", str(label_list[3]))


if __name__ == "__main__":
    unittest.main()
