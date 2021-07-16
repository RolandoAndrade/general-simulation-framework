import unittest

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from mathematics.distributions.exponential_distribution import ExponentialDistribution
from mathematics.distributions.poisson_distribution import PoissonDistribution
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
        arrivals_per_second = PoissonDistribution(5)  # 5 arrivals per second mean
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

        source.add(server)

        experiment = DiscreteEventExperiment(self.ds)
        experiment.simulationControl.start(stop_time=simulation_time_seconds)
        experiment.simulationControl.wait()
        print("Generated: " + str(source.getState().outputBuffer.numberEntered))
        print("Entered at server: " + str(server.getState().inputBuffer.numberEntered))
        print("Waiting at server: " + str(server.getState().inputBuffer.currentNumberOfEntities))
        print("Processing at server: " + str(server.getState().processBuffer.currentNumberOfEntities))
        print("Processed at server: " + str(server.getState().processBuffer.numberEntered))
        print("Finished: " + str(server.getState().outputBuffer.numberEntered))


if __name__ == '__main__':
    unittest.main()
