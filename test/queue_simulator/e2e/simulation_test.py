import unittest
from decimal import getcontext

from core.config import FLOATING_POINT_DIGITS
from core.mathematics.distributions import (
    ExponentialDistribution,
    TriangularDistribution,
)
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from experiments.experiment_builders.discrete_event_experiment import (
    DiscreteEventExperiment,
)
from core.mathematics.values.value import Value
from queue_simulator.buffer.core import BufferProperty
from queue_simulator.label.label import Label
from queue_simulator.server.server import Server
from queue_simulator.source.source import Source
from test.queue_simulator.e2e.mock.entity_by_type_emitter import EntityByTypeEmitter


class SimulationTest(unittest.TestCase):
    dynamicSystem: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        self.ds = DiscreteEventDynamicSystem()
        getcontext().prec = 12

    def test_simulation_1(self):
        """Source - server - sink"""
        getcontext().prec = FLOATING_POINT_DIGITS
        print(getcontext())
        interarrival_time_seconds = ExponentialDistribution(
            0.25
        )  # 0.25 mean interarrival time
        entities_per_arrival = Value(1)  # 1 entity per arrival
        simulation_time_minutes = 60 * 2  # 2 hours
        processing_time = TriangularDistribution(0.1, 0.2, 0.3)  # 2 seconds

        source = Source(
            self.ds,
            "Source1",
            entity_emitter=EntityByTypeEmitter("A"),
            entities_per_arrival=entities_per_arrival,
            inter_arrival_time=interarrival_time_seconds,
        )

        server = Server(self.ds, "Server1", processing_time=processing_time)

        source.add(server)
        label_source_out = Label(
            source.get_state().output_buffer.get_properties,
            BufferProperty.NUMBER_ENTERED,
        )
        label_server_in = Label(
            server.get_state().input_buffer.get_properties,
            BufferProperty.NUMBER_ENTERED,
        )
        label_server_out = Label(
            server.get_state().output_buffer.get_properties,
            BufferProperty.NUMBER_ENTERED,
        )

        experiment = DiscreteEventExperiment(self.ds)
        experiment.simulation_control.start(stop_time=simulation_time_minutes)
        experiment.simulation_control.wait()
        print("Generated: " + str(source.get_state().output_buffer.number_entered))
        print(
            "Entered at server: " + str(server.get_state().input_buffer.number_entered)
        )
        print(
            "Waiting at server: "
            + str(server.get_state().input_buffer.current_number_of_entities)
        )
        print(
            "Processing at server: "
            + str(server.get_state().process_buffer.current_number_of_entities)
        )
        print(
            "Processed at server: "
            + str(server.get_state().process_buffer.number_entered)
        )
        print("Finished: " + str(server.get_state().output_buffer.number_entered))
        print(label_source_out.get_value())
        print(label_server_in.get_value())
        print(label_server_out.get_value())
        print(474)
        print(474)
        print(472)
        print(471)


if __name__ == "__main__":
    unittest.main()
