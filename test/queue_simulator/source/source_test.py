import unittest
from random import seed

from core.components.entity.properties.any_property import AnyProperty
from core.components.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from mathematics.distributions.poisson_distribution import PoissonDistribution
from mathematics.values.value import Value
from queue_simulator.source.source import Source
from test.queue_simulator.buffer.mocks.mock_emitter import MockEmitter


class TestSource(unittest.TestCase):
    source: Source
    experiment: DiscreteEventExperiment
    ds: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        self.ds = DiscreteEventDynamicSystem()
        self.source = Source(self.ds,
                             name="Source1",
                             entityEmitter=AnyProperty(MockEmitter()))
        self.experiment = DiscreteEventExperiment(self.ds)
        seed(42)

    def test_arrival_time(self):
        # config
        interArrivalTime = ExpressionProperty(PoissonDistribution(5))
        entitiesPerArrival = ExpressionProperty(Value(1))
        self.source.interArrivalTime = interArrivalTime
        self.entitiesPerArrival = entitiesPerArrival

        print(self.ds.getTimeOfNextEvent())
        # simulate
        self.experiment.simulationControl.start(stop_time=120)
        self.experiment.simulationControl.wait()
        # results
        total = self.source.getState().outputBuffer.numberEntered
        print(total)
        self.assertTrue(4 < (total / 120) < 6, "Wrong")


if __name__ == '__main__':
    unittest.main()
