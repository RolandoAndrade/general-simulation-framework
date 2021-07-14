import unittest

from core.components.entity.properties.any_property import AnyProperty
from core.components.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from mathematics.distributions.poisson_distribution import PoissonDistribution
from queue_simulator.source.source import Source
from test.queue_simulator.buffer.mocks.mock_emitter import MockEmitter


class MyTestCase(unittest.TestCase):
    def test_source_distribution(self):
        ds = DiscreteEventDynamicSystem()
        source = Source(ds,
                        name="Source1",
                        entityEmitter=AnyProperty(MockEmitter()),
                        interArrivalTime=ExpressionProperty(PoissonDistribution(5)))
        experiment = DiscreteEventExperiment(ds)
        experiment.simulationControl.start(stop_time=100)
        experiment.simulationControl.wait()
        print((source.getState().outputBuffer.numberEntered / 100))
        self.assertTrue(4 < (source.getState().outputBuffer.numberEntered / 100) < 6, "Wrong")

    def test_60_minutes(self):
        ds = DiscreteEventDynamicSystem()
        source = Source(ds,
                        name="Source1",
                        entityEmitter=AnyProperty(MockEmitter()),
                        interArrivalTime=ExpressionProperty(PoissonDistribution(6 / 60)))

        experiment = DiscreteEventExperiment(ds)
        experiment.simulationControl.start(stop_time=60 * 60)
        experiment.simulationControl.wait()
        print(source.getState().outputBuffer.numberEntered / 60)
        self.assertTrue(5 < source.getState().outputBuffer.numberEntered / 60 < 7, "Wrong")


if __name__ == '__main__':
    unittest.main()
