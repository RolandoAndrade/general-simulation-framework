import unittest

from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from mathematics.distributions.poisson_distribution import PoissonDistribution
from queue_simulator.source.properties.source_property import SourceProperty
from queue_simulator.source.source import Source


class MyTestCase(unittest.TestCase):
    def test_source_distribution(self):
        ds = DiscreteEventDynamicSystem()
        source = Source(ds,
                        "Source 1")

        source.setProperty(SourceProperty.ENTITY_TYPE, "Entity A")
        source.setProperty(SourceProperty.INTER_ARRIVAL_TIME, PoissonDistribution(5))
        experiment = DiscreteEventExperiment(ds)
        experiment.simulationControl.start(stop_time=100)
        experiment.simulationControl.wait()
        print((source.getState()['outputs'] / 100))
        self.assertTrue(4 < (source.getState()['outputs'] / 100) < 6, "Wrong")


if __name__ == '__main__':
    unittest.main()
