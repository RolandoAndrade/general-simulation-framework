import unittest
from test.discrete_time_model.atomic_model.discrete_time_atomic_model_test import DiscreteTimeAtomicModelTest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dtam = DiscreteTimeAtomicModelTest()

    def test_state_transition_function(self):
        y = [10, 15, 17.5, 8.75, 5]
        x = [1, 1, 0, 0.0625, 0]
        for t in range(len(x)):
            yt = self.dtam.getOutput()
            self.assertEqual(yt, y[t])
            self.dtam.stateTransition(x[t], )


if __name__ == '__main__':
    unittest.main()
