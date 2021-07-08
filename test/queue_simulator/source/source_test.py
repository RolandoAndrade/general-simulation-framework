import unittest

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from mathematics.distributions.poisson_distribution import PoissonDistribution
from test.queue_simulator.source.properties.source_entity_type import SourceEntityType
from test.queue_simulator.source.properties.source_inter_arrival_time import SourceInterArrivalTime
from test.queue_simulator.source.source import Source
from time import sleep
class MyTestCase(unittest.TestCase):
    def test_source_distribution(self):
        ds = DiscreteEventDynamicSystem()
        source = Source(ds,
                        "Source 1",
                        SourceEntityType("EntityA"),
                        SourceInterArrivalTime(PoissonDistribution(5)))
        experiment = DiscreteEventExperiment(ds)
        experiment.simulationControl.start(stop_time=100)
        sleep(1)
        print(experiment.simulationReport.generateReport())


if __name__ == '__main__':
    unittest.main()
