import unittest

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from mathematics.distributions.exponential_distribution import ExponentialDistribution
from mathematics.values.value import Value
from queue_simulator.server.server import Server
from queue_simulator.source.source import Source
from test.queue_simulator.e2e.mock.entity_by_type_emitter import EntityByTypeEmitter


class SimulationTest(unittest.TestCase):
    dynamicSystem: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        self.ds = DiscreteEventDynamicSystem()

    def test_simulation_1(self):
        """Source - server - sink"""
        interarrival_time_seconds = Value(1)  # 1 second
        arrivals_per_second = ExponentialDistribution(5)  # 5 arrivals per second mean
        simulation_time_seconds = 10 * 60  # 10 minutes
        processing_time = Value(2)  # 2 seconds

        source = Source(self.ds,
                        "Source1",
                        entity_emitter=EntityByTypeEmitter("A"),
                        entities_per_arrival=arrivals_per_second,
                        inter_arrival_time=interarrival_time_seconds)

        server = Server(self.ds,
                        "Server1",
                        processing_time=processing_time
                        )


if __name__ == '__main__':
    unittest.main()
