from __future__ import annotations

import unittest

from dynamic_system.utils.bag_of_values import BagOfValues
from dynamic_system.utils.value import Value
from test.logic_gates.dynamic_system.input_layer import InputLayer

from test.logic_gates.dynamic_system.and_gate import AndGate


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.input_layer = InputLayer("Input")
        self.andModel = AndGate("Output")
        self.andModel.add(self.input_layer)

    def test_and_gate_output(self):
        bg = BagOfValues()
        bg['x'] = True
        bg['y'] = True
        self.input_layer.set_inputs(bg)
        self.input_layer.receiveInput()
        self.assertEqual(self.andModel.getOutput(), True, "Should be true")
        bg['y'] = False
        self.input_layer.set_inputs(bg)
        self.input_layer.receiveInput()
        self.assertEqual(self.andModel.getOutput(), False, "Should be false")
        bg['x'] = False
        bg['y'] = True
        self.input_layer.set_inputs(bg)
        self.input_layer.receiveInput()
        self.assertEqual(self.andModel.getOutput(), False, "Should be false")
        bg['x'] = False
        bg['y'] = False
        self.input_layer.set_inputs(bg)
        self.input_layer.receiveInput()
        self.assertEqual(self.andModel.getOutput(), False, "Should be false")


if __name__ == '__main__':
    unittest.main()
