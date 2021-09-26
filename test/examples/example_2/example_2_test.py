import unittest

from examples.example_2.board import Board
from gsf.experiments.experiment_builders import DiscreteEventExperiment


class Example2Test(unittest.TestCase):
    def test_something(self):
        board = Board(10, 10)
        experiment = DiscreteEventExperiment(board)
        print(board)
        experiment.simulation_control.start(stop_time=10)
        experiment.simulation_control.wait()
        print(board)


if __name__ == '__main__':
    unittest.main()
