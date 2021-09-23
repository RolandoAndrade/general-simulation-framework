import unittest

from examples.linear_automata import LinearAutomata
from experiments.experiment_builders import DiscreteEventExperiment


class Example1(unittest.TestCase):
    def test_with_classes(self):
        linear_automata = LinearAutomata(cells=10)
        experiment = DiscreteEventExperiment(linear_automata)
        print(linear_automata)
        experiment.simulation_control.start(stop_time=5)
        experiment.simulation_control.wait()
        print(linear_automata)
        self.assertEqual("--♥♥♥-♥♥♥-", str(linear_automata))



if __name__ == '__main__':
    unittest.main()
