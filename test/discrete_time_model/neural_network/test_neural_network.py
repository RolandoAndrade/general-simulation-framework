import unittest

from dynamic_system.models.dynamic_system import DynamicSystem
from test.discrete_time_model.neural_network.layer import Layer


class TestNN(unittest.TestCase):
    def test_nn(self):
        self.ds = DynamicSystem()
        self.l1 = Layer(self.ds, 2, 2)
        self.l2 = Layer(self.ds, 3, 2)
        self.l2.add(self.l1)
        print(self.ds.getOutput())
        self.ds.stateTransition({
            self.l1.getID(): [[1], [1]]
        })
        print(self.ds.getOutput())
        self.ds.stateTransition({
            self.l1.getID(): [[1], [1]]
        })
        print(self.ds.getOutput())

if __name__ == '__main__':
    unittest.main()
