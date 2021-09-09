import unittest

from core.types import Time
from experiments.experiment_builders import DiscreteEventExperiment
from test.prototypes.prototype_4.assembly_line import AssemblyLine


class Prototype4Test(unittest.TestCase):
    def test_validation(self):
        assembly_line = AssemblyLine([1, 2])
        experiment = DiscreteEventExperiment(assembly_line)

        experiment.simulation_control.start(stop_time=Time(7))
        experiment.simulation_control.wait()
        print(experiment.simulation_report.generate_report())


if __name__ == '__main__':
    unittest.main()
