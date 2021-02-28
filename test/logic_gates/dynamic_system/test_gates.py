from __future__ import annotations

import unittest


from dynamic_system.utils.bag_of_values import BagOfValues
from dynamic_system.utils.value import Value
from test.logic_gates.dynamic_system.input_layer import InputLayer

from test.logic_gates.dynamic_system.and_gate import AndGate


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.input_layer = InputLayer()
        self.andModel = AndGate()
        self.andModel.add(self.input_layer)

    def test_and_gate_output(self):
        self.input_layer.set_inputs(BagOfValues([Value("x", True), Value("y", True)]))
        self.input_layer.receive_input()
        self.assertEqual(self.andModel.get_output(), True, "Should be true")
        self.input_layer.set_inputs(BagOfValues([Value("x", True), Value("y", False)]))
        self.input_layer.receive_input()
        self.assertEqual(self.andModel.get_output(), False, "Should be false")
        self.input_layer.set_inputs(BagOfValues([Value("x", False), Value("y", True)]))
        self.input_layer.receive_input()
        self.assertEqual(self.andModel.get_output(), False, "Should be false")
        self.input_layer.set_inputs(BagOfValues([Value("x", False), Value("y", False)]))
        self.input_layer.receive_input()
        self.assertEqual(self.andModel.get_output(), False, "Should be false")


if __name__ == '__main__':
    unittest.main()
