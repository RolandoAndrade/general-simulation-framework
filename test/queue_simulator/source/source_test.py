import unittest

from core.entity.properties.any_property import AnyProperty
from core.entity.properties.expression_property import ExpressionProperty
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from experiments.experiment_builders.discrete_event_experiment import DiscreteEventExperiment
from core.mathematics.distributions.poisson_distribution import PoissonDistribution
from core.mathematics.values.value import Value
from queue_simulator.source.source import Source
from test.queue_simulator.buffer.mocks.mock_emitter import MockEmitter


class TestSource(unittest.TestCase):
    source: Source
    experiment: DiscreteEventExperiment
    ds: DiscreteEventDynamicSystem

    def setUp(self) -> None:
        """Setups the source, dynamic system and experiment"""
        self.ds = DiscreteEventDynamicSystem()
        self.source = Source(self.ds,
                             name="Source1",
                             entity_emitter=AnyProperty(MockEmitter()))
        self.experiment = DiscreteEventExperiment(self.ds)

    def test_inter_arrival_time(self):
        """Should be able to create entities with a distribution expression as interarrival value"""
        # config
        interArrivalTime = ExpressionProperty(PoissonDistribution(5))
        entitiesPerArrival = ExpressionProperty(Value(1))
        self.source.interArrivalTime = interArrivalTime
        self.source.entitiesPerArrival = entitiesPerArrival
        # simulate
        self.experiment.simulation_control.start(stop_time=120)
        self.experiment.simulation_control.wait()
        # results
        total = self.source.get_state().outputBuffer.numberEntered
        self.assertTrue(0.15 < (total / 120) < 0.35, "Wrong")

    def test_entities_per_arrival(self):
        """Should be able to create entities with a distribution expression as entities per arrival value"""
        # config
        interArrivalTime = ExpressionProperty(Value(1))
        entitiesPerArrival = ExpressionProperty(PoissonDistribution(5))
        self.source.interArrivalTime = interArrivalTime
        self.source.entitiesPerArrival = entitiesPerArrival
        # simulate
        self.experiment.simulation_control.start(stop_time=120)
        self.experiment.simulation_control.wait()
        # results
        total = self.source.get_state().outputBuffer.numberEntered
        self.assertTrue(4 < (total / 120) < 6, "Wrong")


if __name__ == '__main__':
    unittest.main()
