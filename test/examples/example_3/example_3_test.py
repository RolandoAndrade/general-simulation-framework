import unittest

from gsf.core.mathematics.distributions import (
    PoissonDistribution,
    ExponentialDistribution,
    TriangularDistribution,
)
from gsf.core.mathematics.values import Value
from examples.example_3.factory_system import FactorySystem
from examples.example_3.station import Station
from gsf.experiments.experiment_builders import DiscreteEventExperiment


class Example3Test(unittest.TestCase):
    def test_basic(self):
        factory = FactorySystem([1, 2], Value(1))
        station_1 = Station(factory, Value(1))
        station_2 = Station(factory, Value(2))
        factory.generator.add(station_1)
        station_1.add(station_2)
        station_2.add(factory.exit)

        experiment = DiscreteEventExperiment(factory)
        experiment.simulation_control.start(stop_time=10)
        experiment.simulation_control.wait()

        print(factory.exit.get_output())
        print(experiment.simulation_report.generate_report())

    def test_expressions(self):
        factory = FactorySystem(PoissonDistribution(5), ExponentialDistribution(0.5))
        station_1 = Station(factory, TriangularDistribution(1, 2, 5))
        station_2 = Station(factory, TriangularDistribution(1, 4, 5))
        factory.generator.add(station_1)
        station_1.add(station_2)
        station_2.add(factory.exit)

        experiment = DiscreteEventExperiment(factory)
        experiment.simulation_control.start(stop_time=15)
        experiment.simulation_control.wait()

        print(factory.exit.get_output())
        print(experiment.simulation_report.generate_report())


if __name__ == "__main__":
    unittest.main()
